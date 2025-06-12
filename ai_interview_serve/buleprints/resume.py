import json
import os
import time
import traceback
from docx2pdf import convert
import tempfile
from flask import Blueprint, request, session, jsonify, current_app
from werkzeug.utils import secure_filename
import shutil
from exts import api
from result import R
from status import SUCCESS, ERROR, baseURL
import fitz  # PyMuPDF
from resume_sdk import resume_pdf_to_json, resume_json_to_markdown
from io import BytesIO
import requests
from werkzeug.datastructures import FileStorage
from generate_resume import generate_resume_from_text
from match_job import run_dify_workflow
import pythoncom

bp = Blueprint("resume", __name__, url_prefix="/resume")
api.init_app(bp)

ALLOWED_EXTENSIONS = {'.pdf'}


def convert_docx_to_pdf(docx_path, pdf_path=None):
    pythoncom.CoInitialize()

    try:
        # 自动生成输出路径
        if not pdf_path:
            tmp_dir = tempfile.mkdtemp()
            pdf_path = os.path.join(tmp_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")

        convert(docx_path, pdf_path)

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return pdf_bytes

    finally:
        pythoncom.CoUninitialize()


def allowed_file(filename):
    ext = os.path.splitext(filename)[-1].lower()
    return ext in ALLOWED_EXTENSIONS


def handle_resume_upload(file, email):
    if not file or not email:
        return R(400, '文件或邮箱不能为空', None)

    original_filename = file.filename
    ext = os.path.splitext(original_filename)[-1].lower()

    if ext != '.pdf':
        return R(400, '仅支持上传PDF文件', None)

    filename = original_filename
    static_dir = os.path.join(current_app.root_path, 'static')
    upload_dir = os.path.join(static_dir, email)
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, filename)

    try:
        file.save(save_path)

        resume_json = resume_pdf_to_json(save_path)
        job_tags = resume_json['tags']

        # ✅ 新增保存 job_tags 为 JSON 文件
        tags_filename = os.path.splitext(filename)[0] + ".json"
        tags_path = os.path.join(upload_dir, tags_filename)
        with open(tags_path, "w", encoding="utf-8") as f:
            json.dump(job_tags, f, ensure_ascii=False, indent=2)

        resume_markdown = resume_json_to_markdown(resume_json)

        if resume_markdown.startswith('```markdown') and resume_markdown.rstrip().endswith('```'):
            lines = resume_markdown.strip().splitlines()
            resume_markdown = '\n'.join(lines[1:-1]).strip()

        markdown_filename = os.path.splitext(filename)[0] + ".txt"
        markdown_path = os.path.join(upload_dir, markdown_filename)

        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(resume_markdown)

        return R(200, '简历上传并解析成功', {
            'pdfPath': f'static/{email}/{filename}',
            'markdownPath': f'static/{email}/{markdown_filename}',
            'jsonPath': f'static/{email}/{tags_filename}',
        })

    except Exception as e:
        return R(500, f'文件处理失败: {str(e)}', None)


@bp.route("/add_resume", methods=["POST"])
def add_resume():
    file = request.files.get('file')
    email = request.form.get('email') or session.get('email')
    return handle_resume_upload(file, email)


@bp.route("/get_resume", methods=["GET"])
def get_resume():
    email = request.args.get('email')

    if email is None:
        email = session.get('email')

    if not email:
        return R(400, '邮箱不能为空', None)

    # 构造目录路径
    static_dir = os.path.join(current_app.root_path, 'static')
    user_dir = os.path.join(static_dir, email)

    if not os.path.exists(user_dir):
        return R(404, '未找到对应邮箱的简历文件夹', [])

    resume_list = []
    for filename in os.listdir(user_dir):
        if filename.lower().endswith('.pdf'):
            file_path = f'{baseURL}/static/{email}/{filename}'

            # 构造 PNG 文件名
            png_filename = filename.rsplit('.', 1)[0] + '.png'
            png_path = os.path.join(user_dir, png_filename)
            png_url = f'{baseURL}/static/{email}/{png_filename}'

            # 构造 JSON 文件名
            json_filename = filename.rsplit('.', 1)[0] + '.json'
            json_path = os.path.join(user_dir, json_filename)
            job_tags = None

            # 读取 JSON 文件内容
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        job_tags = json.load(f)
                except Exception as e:
                    print(f"读取 JSON 失败：{json_filename}，错误：{e}")

            # 如果 PNG 不存在就生成
            if not os.path.exists(png_path):
                try:
                    doc = fitz.open(os.path.join(user_dir, filename))
                    page = doc.load_page(0)  # 获取第一页
                    pix = page.get_pixmap(dpi=150)
                    pix.save(png_path)
                except Exception as e:
                    print(f"转换 PDF 到 PNG 失败: {filename}，错误：{e}")
                    png_url = None

            resume_list.append({
                'name': filename,
                'url': file_path,
                'preview': png_url,
                'tags': job_tags
            })

    return R(200, '获取成功', resume_list)


@bp.route("/get_resume_txt", methods=["GET"])
def get_resume_txt():
    email = request.args.get('email')
    name = request.args.get('name')

    if not email or not name:
        return R(400, '邮箱或文件名不能为空', None)

    # 构造路径
    static_dir = os.path.join(current_app.root_path, 'static')
    txt_filename = name.replace('.pdf', '.txt')
    txt_path = os.path.join(static_dir, email, txt_filename)

    # 检查文件是否存在
    if not os.path.exists(txt_path):
        return R(404, f'文件不存在: {txt_filename}', None)

    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return R(200, '简历内容获取成功', content)
    except Exception as e:
        return R(500, f'读取文件失败: {str(e)}', None)


@bp.route('/generate_resume', methods=["POST"])
def generate_resume():
    try:
        data = request.get_json()
        text = data.get("text", "")

        print(text)

        # 参数校验
        if not text or len(text.strip()) < 10:
            return R(code=ERROR, message='请输入有效的简历文本（不少于10个字）', data=None)

        # 调用生成函数
        resume_img_and_word = json.loads(generate_resume_from_text(text).decode('utf-8'))
        # resume_img_and_word = json.loads(
        #     b'{"links":[{"img_url":"https://statics.zcmima.cn/uploads/resume/cover/20250610/b725fcf7-a0a4-47fb-8965-2915399b79ef.jpg","word_url":"https://file.duhuitech.com/o/acd7ca6439a0622dd689d9a1b49150f1d/17495388174331.docx"},{"img_url":"https://statics.zcmima.cn/uploads/resume/cover/20250610/8a45ac7a-d612-4d70-b3b4-1e8e0cbff248.jpg","word_url":"https://file.duhuitech.com/o/7b71ac60dd691b66850d5565a05ee2108/17495388102725.docx"},{"img_url":"https://statics.zcmima.cn/uploads/resume/cover/20250610/91ade3d3-9169-42e6-8a37-af56b439a1c5.jpg","word_url":"https://file.duhuitech.com/o/2453df000a346b1303875afef4aea2590/17495388174185.docx"}]}'.decode(
        #         'utf-8'))
        # 类型和内容校验
        if not resume_img_and_word:
            return R(code=500, message='生成简历失败，返回数据为空', data=None)
        if isinstance(resume_img_and_word, bytes):
            try:
                resume_json = json.loads(resume_img_and_word.decode('utf-8'))
            except Exception as e:
                return R(code=500, message=f'简历解析失败: {str(e)}', data=None)
        elif isinstance(resume_img_and_word, dict):
            resume_json = resume_img_and_word
        else:
            return R(code=500, message='未知的简历数据格式', data=None)

        return R(code=SUCCESS, message='简历生成成功', data=resume_json)

    except Exception as e:
        traceback.print_exc()
        return R(code=500, message=f'服务器错误: {str(e)}', data=None)


@bp.route('/download_resume', methods=["GET"])
def download_resume():
    resume_name = request.args.get('resume_name')
    word_url = request.args.get('word_url')
    email = request.args.get('email') or session.get('email')

    if not word_url or not resume_name or not email:
        return R(400, '缺少必要参数', None)

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}

        print("下载简历中...")
        start = time.time()

        response = requests.get(word_url, headers=headers, timeout=10, stream=False, verify=False)

        if response.status_code != 200:
            return R(500, '文件下载失败', None)

        print("下载成功，耗时：", time.time() - start)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(response.content)
            tmp_word_path = tmp.name

        pdf_bytes = convert_docx_to_pdf(tmp_word_path)
        pdf_filename = os.path.splitext(resume_name)[0] + ".pdf"

        file_storage = FileStorage(
            stream=BytesIO(pdf_bytes),
            filename=pdf_filename,
            content_type='application/pdf'
        )

        os.remove(tmp_word_path)

        return handle_resume_upload(file_storage, email)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return R(500, f'处理失败: {str(e)}', None)


@bp.route('/resume_match_job', methods=["POST"])
def resume_match_job():
    json_data = request.get_json()
    resume_tags = json_data.get("resume_tags")

    if not resume_tags:
        return R(code=ERROR, message="简历没有推荐标签", data=None)

    # 调用 Dify 工作流
    result = run_dify_workflow(resume_tags)

    if not result['success']:
        return R(code=ERROR, message="岗位匹配失败，请稍后再试", data=None)

    try:
        raw_text = result['data']['data']['outputs']['text']
        job_list = json.loads(raw_text)

        job_list.sort(key=lambda x: x.get("similarity", 0), reverse=True)

        return R(code=SUCCESS, message="岗位匹配成功", data=job_list)

    except (KeyError, json.JSONDecodeError) as e:
        return R(code=ERROR, message="岗位匹配结果解析失败", data=None)


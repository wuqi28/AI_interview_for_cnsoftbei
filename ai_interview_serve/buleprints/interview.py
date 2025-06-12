import json
import os
import requests
import threading
from datetime import datetime
from flask import Blueprint, request, session, jsonify, current_app
from werkzeug.utils import secure_filename
from ost import video_to_text
from exts import api, db
from result import R
from status import SUCCESS, ERROR, baseURL
from models import UserModel, InterviewRecordModel, InterviewTurnModel
from interviewer import chat_with_spark, parse_spark_stream, get_system_prompt, get_parsing_prompt, chat_with_qwen, \
    get_answer_prompt, optimize_speaker_answer
from generate_report import generate_interview_evaluation

bp = Blueprint("interview", __name__, url_prefix="/interview")
api.init_app(bp)


def to_bool(val):
    return str(val).lower() in ['true', '1', 'yes']


def async_task(app, audio_path, interview_id, ai_time, speaker_time, face_emotion, is_focused, ai_interviewer_text,
               speaker_text, average_bearing_degrees, average_gaze_strength, interview_round):
    with app.app_context():
        res = classify_voice_emotion(audio_path, speaker_text)
        voice_emotion = res.get('emotion')
        audio = res.get('audio')
        audio_avg_pitch = audio.get('avg_pitch')
        audio_speech_time = audio.get('speech_time')
        audio_pause_time = audio.get('pause_time')
        audio_pause_ratio = audio.get('pause_ratio')
        audio_pause_count = audio.get('pause_count')
        audio_words_per_minute = audio.get('words_per_minute')
        audio_path = local_path_to_url(audio_path)
        # print(audio_path, voice_emotion, interview_id, ai_time, speaker_time, face_emotion, is_focused, ai_interviewer_text, speaker_text, average_bearing_degrees,
        #       average_gaze_strength, audio_avg_pitch, audio_speech_time, audio_pause_time, audio_pause_ratio, audio_pause_count, audio_words_per_minute)

        new_turn = InterviewTurnModel(
            interview_id=interview_id,
            ai_time=ai_time,
            speaker_time=speaker_time,
            audio_path=audio_path,
            ai_interviewer_text=ai_interviewer_text,
            speaker_text=speaker_text,

            face_emotion=face_emotion,
            is_focused=is_focused,
            average_bearing_degrees=average_bearing_degrees,
            average_gaze_strength=average_gaze_strength,

            voice_emotion=voice_emotion,
            audio_avg_pitch=audio_avg_pitch,
            audio_speech_time=audio_speech_time,
            audio_pause_time=audio_pause_time,
            audio_pause_ratio=audio_pause_ratio,
            audio_pause_count=audio_pause_count,
            audio_words_per_minute=audio_words_per_minute,

            round=interview_round
        )
        db.session.add(new_turn)
        db.session.commit()


def get_user_id_by_email(email):
    user = UserModel.query.filter_by(email=email).first()
    return user.id if user else None


def get_interview_id_by_current_id(current_interview_id):
    interview = InterviewRecordModel.query.filter_by(current_interview_id=current_interview_id).first()
    return interview.id if interview else None


def local_path_to_url(local_path):
    # 替换 Windows 路径分隔符为 URL 中的斜杠
    web_path = local_path.replace("\\", "/")

    # 找到 static 之后的相对路径
    if 'static/' in web_path:
        static_index = web_path.index('static/')
        relative_path = web_path[static_index:]
        return f"http://127.0.0.1:5000/{relative_path}"
    else:
        raise ValueError("路径中不包含 static 目录")


def classify_voice_emotion(wav_file_path: str, speaker_text: str):
    """
    向 Flask 服务器的 /voice_classification 接口发送语音文件，
    获取情绪识别结果。

    参数:
        wav_file_path (str): 要上传的 .wav 文件的完整路径

    返回:
        dict: 成功返回包含情绪和置信度的 JSON 响应；
              失败返回包含错误信息的字典。
    """
    url = "http://127.0.0.1:5001/voice_classification"

    try:
        with open(wav_file_path, 'rb') as f:
            files = {'file': f}
            data = {'speaker_text': speaker_text}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            return R(code=ERROR, message=response.text, data=None)
    except Exception as e:
        return R(code=ERROR, message=str(e), data=None)


@bp.route("/start_interview", methods=["POST"])
def start_interview():
    res = request.get_json()
    # print(res)

    # 获取字段
    email = res.get("email")
    interviewer_name = res.get("interviewer_name")
    interview_style = res.get("interview_style")
    job = res.get("job", {})
    company = job.get("company", "").replace(" ", "_")
    title = job.get("title", "").replace(" ", "_")

    if not email or not company or not title:
        return R(code=400, message="缺少必要字段", data=None)

    # 当前时间戳
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # 构建保存路径
    current_interview_id = f"{company}-{title}-{timestamp}"
    save_path = os.path.join(current_app.root_path, "static", email, current_interview_id)
    os.makedirs(save_path, exist_ok=True)

    # 直接保存整个 JSON 数据
    data_json_path = os.path.join(save_path, "data.json")
    with open(data_json_path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    new_record = InterviewRecordModel(
        user_id=get_user_id_by_email(email),
        current_interview_id=current_interview_id,
        interviewer_name=interviewer_name,
        interview_style=interview_style
    )
    db.session.add(new_record)
    db.session.commit()

    return R(code=SUCCESS, message=None, data={
        "current_interview_id": current_interview_id,
        "interview_record": new_record.to_dict()
    })


@bp.route("/chat_with_interviewer", methods=["POST"])
def chat_with_interviewer():
    interview_round = request.form.get("round")
    email = request.form.get("email")
    current_interview_id = request.form.get("current_interview_id")
    question_type = request.form.get("question_type")
    # final_transcript = request.form.get("final_transcript")
    old_history = request.form.get("history")
    face_emotion = request.form.get("face_emotion")
    looking_at_screen = request.form.get("looking_at_screen")
    ai_time = request.form.get("ai_time")
    speaker_time = request.form.get("speaker_time")
    average_bearing_degrees = request.form.get("average_bearing_degrees")
    average_gaze_strength = request.form.get("average_gaze_strength")
    old_history = json.loads(old_history)

    # print(f"当前情绪:{face_emotion}")
    # print(f"当前情绪:{looking_at_screen}")

    file = request.files.get("file")
    if file is None or file.filename == '':
        return R(code=400, message="未上传音频文件", data=None)

    if not file.filename.lower().endswith(".wav"):
        return R(code=400, message="只支持 .wav 格式音频", data=None)

    # 构建保存路径
    save_path = os.path.join(current_app.root_path, "static", email, current_interview_id)
    os.makedirs(save_path, exist_ok=True)

    # 保存音频文件为 voice_{时间戳}.wav
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = secure_filename(f"voice_{timestamp}.wav")
    file_path = os.path.join(save_path, filename)
    file.save(file_path)

    # 构建 data.json 的路径
    data_path = os.path.join(current_app.root_path, "static", email, current_interview_id, "data.json")

    # 检查文件是否存在
    if not os.path.exists(data_path):
        return R(code=404, message="data.json 不存在", data=None)

    # 读取并解析 JSON 内容
    with open(data_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    prompt = get_system_prompt(json_data.get('interviewerConfig').get('interviewerName'),
                               json_data.get('job').get('company'),
                               json_data.get('job').get('title'),
                               json_data.get('resumeMarkdown'),
                               json_data.get('interviewerConfig').get('styleValue'),
                               json_data.get('job').get('description'),
                               question_type)

    final_transcript = video_to_text(file_path)

    # print(old_history)

    thread = threading.Thread(target=async_task, args=(current_app._get_current_object(),
                                                       file_path,
                                                       get_interview_id_by_current_id(current_interview_id),
                                                       ai_time,
                                                       speaker_time,
                                                       to_bool(face_emotion),
                                                       to_bool(looking_at_screen),
                                                       old_history[-1]["content"],
                                                       final_transcript,
                                                       average_bearing_degrees,
                                                       average_gaze_strength,
                                                       interview_round
                                                       ))
    thread.start()

    print(final_transcript)
    raw_response, new_history = chat_with_spark(prompt, final_transcript, old_history)
    assistant_reply = parse_spark_stream(raw_response)
    print(assistant_reply)
    new_history.append(assistant_reply)

    return R(code=SUCCESS, message=None, data={
        "current_interview_id": current_interview_id,
        "saved_voice_filename": filename,
        "history": new_history
    })


@bp.route('/intelligent_parsing', methods=['POST'])
def intelligent_parsing():
    data = request.get_json()

    question = data.get('question')
    email = data.get("email")
    current_interview_id = data.get("current_interview_id")
    data_path = os.path.join(current_app.root_path, "static", email, current_interview_id, "data.json")

    # 检查文件是否存在
    if not os.path.exists(data_path):
        return R(code=404, message="data.json 不存在", data=None)

    # 读取并解析 JSON 内容
    with open(data_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 参数解析与校验
    company = json_data.get('job').get('company')
    job_name = json_data.get('job').get('title')
    resume = json_data.get('resumeMarkdown')
    job_description = json_data.get('job').get('description')

    prompt = get_parsing_prompt(company, job_name, resume, job_description)
    res = chat_with_qwen(prompt, question)

    answer_prompt = get_answer_prompt(company, job_name, resume, job_description, res)
    raw_response, new_history = chat_with_spark(answer_prompt, question)
    assistant_reply = parse_spark_stream(raw_response)
    # answer = chat_with_qwen(answer_prompt, question)

    return R(code=SUCCESS, message=None, data={
        'answer_text': assistant_reply.get('content'),
        'parsing_text': res
        # 'history': new_history
    })


@bp.route('/finish_interview', methods=['GET'])
def finish_interview():
    email = request.args.get("email")
    current_interview_id = request.args.get("current_interview_id")

    # 查询 interview_id
    interview_id = get_interview_id_by_current_id(current_interview_id)

    # 查询面试轮次数据
    turns = InterviewTurnModel.query.filter_by(interview_id=interview_id).all()
    result = [turn.to_dict() for turn in turns]

    # 生成多模态评测报告数据
    interview_report_data = generate_interview_evaluation(str(result))

    # 构建保存路径
    save_dir = os.path.join(current_app.root_path, "static", email, current_interview_id)
    os.makedirs(save_dir, exist_ok=True)  # 确保目录存在

    report_path = os.path.join(save_dir, "interview_report.json")

    # 写入 JSON 文件
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(interview_report_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return R(code=ERROR, message=f'文件保存失败: {str(e)}', data=None)

    return R(code=SUCCESS, message='多模态面试数据报告生成成功', data=None)


@bp.route('/get_interview_report', methods=['GET'])
def get_interview_report():
    email = request.args.get("email")
    current_interview_id = request.args.get("current_interview_id")

    if not email or not current_interview_id:
        return R(code=400, message='缺少 email 或 current_interview_id 参数', data=None)

    # 查询 interview_id
    interview_id = get_interview_id_by_current_id(current_interview_id)

    # 查询所有轮次的原始数据
    turns = InterviewTurnModel.query.filter_by(interview_id=interview_id).all()
    result = [turn.to_dict() for turn in turns]

    # 构造评测报告文件路径
    report_path = os.path.join(current_app.root_path, "static", email, current_interview_id, "interview_report.json")

    if not os.path.isfile(report_path):
        return R(code=404, message='评测报告文件不存在', data=None)

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
    except Exception as e:
        return R(code=500, message=f"读取评测报告失败: {str(e)}", data=None)

    # 构建 round 对应的发言与音频映射
    turn_map = {
        i + 1: {
            "speaker_text": turn["speaker_text"],
            "ai_interviewer_text": turn["ai_interviewer_text"],
            "audio_path": turn["audio_path"]
        }
        for i, turn in enumerate(result)
    }

    # 合并信息到 round_analysis
    for round_item in report_data.get("round_analysis", []):
        round_number = round_item.get("round")
        if round_number in turn_map:
            round_item["speaker_text"] = turn_map[round_number]["speaker_text"]
            round_item["ai_interviewer_text"] = turn_map[round_number]["ai_interviewer_text"]
            round_item["audio_path"] = turn_map[round_number]["audio_path"]

    return R(code=SUCCESS, message='评测报告获取成功', data=report_data)


@bp.route('/optimize_answer', methods=['POST'])
def optimize_answer():
    try:
        # 获取 JSON 数据
        data = request.get_json(force=True, silent=True)

        if not data:
            return R(code=ERROR, message="请求体不能为空", data=None)

        answer = data.get('answer')
        if not answer or not isinstance(answer, str) or answer.strip() == "":
            return R(code=ERROR, message="参数 answer 缺失或无效", data=None)

        # 调用核心逻辑
        res = optimize_speaker_answer(answer)

        return R(code=SUCCESS, message="优化成功", data=res)

    except Exception as e:
        # 可选：写入日志
        current_app.logger.exception("优化答案接口异常：%s", str(e))
        return R(code=ERROR, message="服务器内部错误", data=None)

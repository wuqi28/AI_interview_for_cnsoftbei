# coding: utf-8

import base64
import requests
import json
from zhipuai import ZhipuAI
import urllib3


def resume_pdf_to_json(fname):
    # 读取文件内容
    cont = open(fname, 'rb').read()
    # base_cont = base64.b64encode(cont)  # python2
    base_cont = base64.b64encode(cont).decode('utf8')  # python3

    # 构造json请求
    data = {
        'file_name': fname,  # 简历文件名（需包含正确的后缀名）
        'file_cont': base_cont,  # 简历内容（base64编码的简历内容）
        'need_avatar': 0,  # 是否需要提取头像图片
        'ocr_type': 1,  # 1为高级ocr
    }

    appcode = '90ffd7b7c3d24bd3a3d94e93b18f7307'
    headers = {'Authorization': 'APPCODE ' + appcode,
               'Content-Type': 'application/json; charset=UTF-8',
               }
    # 发送请求
    data_js = json.dumps(data)
    res = requests.post(url='http://resumesdk.market.alicloudapi.com/ResumeParser', data=data_js, headers=headers)

    # 解析结果
    res_js = json.loads(res.text)
    # print(json.dumps(res_js, indent=4, ensure_ascii=False))  # 打印全部结果

    return res_js


def resume_json_to_markdown(json):
    client = ZhipuAI(api_key="7f7cf8fff20b6a3a7bf2946a4b5371d6.CqzDnnkzVZr3CYfw")

    response = client.chat.completions.create(
        model="glm-4-flash-250414",
        messages=[
            {
                "role": "system",
                "content": "我现在有一个简历json，现在需要你将json数据转换为markdown格式的文本。请不要出现```markdown```"
            },
            {
                "role": "user",
                "content": json
            }
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=8192,
        tools=[{"type": "web_search", "web_search": {"search_result": True, "search_engine": "search-std"}}]
    )

    return response.choices[0].message.content


def resume_draw(file_path: str, need_avatar: int = 0) -> dict:
    """
    调用阿里云简历解析API，返回解析结果

    参数：
        appcode (str): 你的阿里云AppCode
        file_path (str): 简历文件的路径，支持 .pdf, .doc, .docx 等
        need_avatar (int): 是否需要解析头像（0 不需要，1 需要）

    返回：
        dict: 接口返回的解析结果
    """
    host = 'https://aliprofile.market.alicloudapi.com'
    path = '/ResumeProfiler'
    url = host + path
    http = urllib3.PoolManager()

    # 读取简历并编码为 base64
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
    except Exception as e:
        return {"error": f"读取文件失败: {str(e)}"}

    # 构造请求体
    payload = {
        "file_name": file_path.split('/')[-1],
        "file_cont": encoded_content,
        "need_avatar": need_avatar
    }

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'APPCODE ' + '90ffd7b7c3d24bd3a3d94e93b18f7307'
    }

    # 发起请求
    try:
        response = http.request(
            'POST',
            url,
            body=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        if response.status != 200:
            return {"error": f"HTTP错误: {response.status}", "detail": response.data.decode('utf-8')}

        return json.loads(response.data.decode('utf-8'))
    except Exception as e:
        return {"error": f"请求失败: {str(e)}"}


if __name__ == '__main__':
    fname = u'D:\\Development\\cnsoftbei\\project\\ai_interview_serve\\static\\wuqi.stu@yangtzeu.edu.cn\\吴奇-后端开发.pdf'
    # resume_json = resume_pdf_to_json(fname)
    # print(resume_json['tags'])
    # resume_markdown = resume_json_to_markdown(resume_json)
    result = resume_draw(file_path=fname, need_avatar=0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
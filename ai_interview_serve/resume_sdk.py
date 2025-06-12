# coding: utf-8

import base64
import requests
import json
from zhipuai import ZhipuAI


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


if __name__ == '__main__':
    fname = u'D:\\Development\\cnsoftbei\\project\\ai_interview_serve\\static\\wuqi.stu@yangtzeu.edu.cn\\吴奇-后端开发.pdf'
    resume_json = resume_pdf_to_json(fname)
    print(resume_json['tags'])
    resume_markdown = resume_json_to_markdown(resume_json)

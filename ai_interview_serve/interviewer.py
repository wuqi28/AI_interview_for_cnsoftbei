import requests
import json
import re

from http import HTTPStatus
import dashscope
from dashscope import Generation
from zhipuai import ZhipuAI


def remove_blank_lines(text: str) -> str:
    # 拆分为行，过滤掉仅包含空白的行，再拼接为一个段落
    lines = text.splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)


def optimize_speaker_answer(answer):
    client = ZhipuAI(api_key="7f7cf8fff20b6a3a7bf2946a4b5371d6.CqzDnnkzVZr3CYfw")

    response = client.chat.completions.create(
        model="glm-4-flash-250414",
        messages=[
            {
                "role": "system",
                "content": "我现在有一个与AI面试官交互的回答，请你把我的回答润色多一点字，丰富我的回答内容。"
            },
            {
                "role": "user",
                "content": answer
            }
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=8192,
        tools=[{"type": "web_search", "web_search": {"search_result": True, "search_engine": "search-std"}}]
    )

    return remove_blank_lines(response.choices[0].message.content)


def chat_with_qwen(prompt, question):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": question}
    ]

    response = Generation.call(
        model="qwen-plus",
        api_key="sk-13766f6cab2d4e5286551bd52beaf097",
        messages=messages,
        stream=False,
        result_format='message',
        top_p=0.8,
        temperature=0.7,
        enable_search=True
    )

    if response.status_code == HTTPStatus.OK:
        content = response.output.choices[0].message['content']
        # print(content)
        return content
    else:
        # print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
        #     response.request_id, response.status_code,
        #     response.code, response.message
        # ))
        return None


def chat_with_spark(system_content, user_content, history=None):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer AosuiEXhADJYPTDpAosY:AXHracdHOqLUeWYodNwJ"
    }

    messages = history[:] if history else []

    if messages and messages[0]['role'] == 'system':
        messages[0]['content'] = system_content
    elif not any(msg['role'] == 'system' for msg in messages):
        messages.insert(0, {"role": "system", "content": system_content})

    messages.append({"role": "user", "content": user_content})

    payload = {
        "model": "4.0Ultra",
        "stream": True,
        "max_tokens": 8192,
        "top_k": 6,
        "temperature": 1,
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)
    response.encoding = "utf-8"

    result_text = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            result_text += line

    return result_text, messages


def parse_spark_stream(raw_text):
    pattern = r'data:\s*({.*?})(?=data:|\Z)'
    matches = re.findall(pattern, raw_text, re.DOTALL)

    content_parts = []
    for match in matches:
        try:
            data = json.loads(match)
            delta = data.get("choices", [{}])[0].get("delta", {})
            content = delta.get("content")
            if content:
                content_parts.append(content)
        except json.JSONDecodeError:
            continue

    full_content = "".join(content_parts)
    return {"role": "assistant", "content": full_content}


def get_system_prompt(interviewer_name, company, job_name, resume, interview_style, job_description, question_type):
    prompt = f'''
    你是一位来自 {company} 的面试官，岗位是 {job_name}，名字叫作 {interviewer_name}，面试风格是 {interview_style}，面试场合非常正式，不要开玩笑。你将以 {job_name} 岗位为目标，对应届高校毕业生进行结构化面试。
    
    请遵循以下要求：
    1. 不要在面试过程中要求同学进行自我介绍，只需按照当前类别提问即可；
    2. 当前面试环节中，你每次只提一个问题，不要一次性列出多个问题；
    3. 问题必须简洁明了，控制在50字以内；
    4. 不要输出 Markdown、数字编号、序号、列表格式，只输出一句清晰的问题；
    5. 问题语言应正式、专业，符合真实面试场景；
    
    本次提问属于以下四类中的某一类，当前类别是：【{question_type}】，你只按当前类别提一个问题：
    
    1. 专业技能测试：基于岗位要求提问理论性问题，考察候选人在该岗位上的核心知识储备，不需要提到简历内容；
    2. 简历深挖与项目分析：基于候选人简历中的项目、实习或科研经历，提问其实践参与情况，开场词：根据您的简历...；
    3. 情景模拟：设置与岗位相关的真实场景，引导候选人模拟决策或问题处理；
    4. 综合问答：提问职业规划、公司认知或团队协作等，考察动机与文化适配性。
    
    请只输出一个问题，不要输出任何解释说明。

    
    岗位要求:{job_description}

    面试者的简历:{resume}
    '''
    return prompt


def get_answer_prompt(company, job_name, resume, job_description, tip):
    prompt = f'''
    你是一位面试指导顾问，我正在参加 {company} 的 {job_name} 面试。
    
    请你严格参考岗位要求和我的简历 ，严格按照提示**{tip}**输出回答，若有必要可以举例说明，帮助我回应面试官的问题。
    
    要求如下：
    1. **禁止使用任何 HTML、Markdown、列表、编号、引号、解释、建议、补充说明等**；
    2. 请使用**中文**，语气正式专业，语言精炼，不要重复题目内容；
    
    【岗位要求】：
    {job_description}
    
    【我的简历】：
    {resume}
    
    请立即生成符合规范的一句话提示。
    '''
    return prompt


def get_parsing_prompt(company, job_name, resume, job_description):
    prompt = f'''
    你是一位面试指导顾问，我正在参加 {company} 的 {job_name} 面试。
    
    请你严格参考岗位要求和我的简历，输出一句简洁的**回答思路提示**，帮助我回应面试官的问题。
    
    要求如下：
    1. 只输出一句话，总长度控制在 50 字以内；
    2. **必须将提示中的关键术语使用 `<color>关键词</color>` 标签包裹**，用于高亮显示；
    3. 除 `<color>` 标签外，**禁止使用任何 HTML、Markdown、列表、编号、引号、解释、建议、补充说明等**；
    4. 请使用**中文**，语气正式专业，语言精炼，不要重复题目内容；
    5. 输出必须模仿以下示例格式，完全一致：
    
    示例输出（你必须模仿这种格式）：
    - 强调你在<color>微服务架构</color>与<color>接口优化</color>方面的实战经验。
    - 简要介绍你在<color>推荐系统</color>项目中的<color>技术职责</color>和核心成果。
    
    【岗位要求】：
    {job_description}
    
    【我的简历】：
    {resume}
    
    请立即生成符合规范的一句话提示。
    '''
    return prompt


if __name__ == '__main__':
    res = optimize_speaker_answer(
        "嗯面试官您好，我是长江职业学院软件技术专业的吴奇，拥有扎实的前端开发经验和丰富的数据，可视化项目经验，在校期间我专业成绩排名第一，荣获国家奖学金，并带领团队在第十届中国软件杯中斩获高职组二等奖。通过团队协作，我参与了在线数据可视化分析平台的开发，负责前端设计与实现运用GS及快瑞或者shop和一下子等技术，有效提升了用户体验和数据嗯交互效率。我具备良好的沟通能力和团队协作啊合作精神，期待在贵公司有所发挥，持续贡献前端开发与数据可视化领域的力量，谢谢。")
    print(res)

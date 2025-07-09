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


# def chat_with_spark(system_content, user_content, history=None):
#     url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
#     headers = {
#         "Authorization": "Bearer AosuiEXhADJYPTDpAosY:AXHracdHOqLUeWYodNwJ"
#     }
#
#     messages = history[:] if history else []
#
#     if messages and messages[0]['role'] == 'system':
#         messages[0]['content'] = system_content
#     elif not any(msg['role'] == 'system' for msg in messages):
#         messages.insert(0, {"role": "system", "content": system_content})
#
#     messages.append({"role": "user", "content": user_content})
#
#     payload = {
#         "model": "4.0Ultra",
#         "stream": True,
#         "max_tokens": 8192,
#         "top_k": 6,
#         "temperature": 1,
#         "messages": messages
#     }
#
#     response = requests.post(url, headers=headers, json=payload, stream=True)
#     response.encoding = "utf-8"
#
#     result_text = ""
#     for line in response.iter_lines(decode_unicode=True):
#         if line:
#             result_text += line
#
#     return result_text, messages


def chat_with_spark(system_content, user_content, history=None):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer AosuiEXhADJYPTDpAosY:AXHracdHOqLUeWYodNwJ"
    }

    messages = history[:] if history else []

    # 确保 system prompt 存在或更新
    if messages and messages[0]['role'] == 'system':
        messages[0]['content'] = system_content
    elif not any(msg['role'] == 'system' for msg in messages):
        messages.insert(0, {"role": "system", "content": system_content})

    # 构建本次完整消息列表用于请求
    request_messages = messages + [{"role": "user", "content": user_content}]

    payload = {
        "model": "4.0Ultra",
        "stream": True,
        "max_tokens": 8192,
        "top_k": 6,
        "temperature": 1,
        "messages": request_messages
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)
    response.encoding = "utf-8"

    result_text = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            result_text += line

    # 返回去除本轮 user_content 的 messages
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
    5. 算法能力：围绕常见算法（如排序、查找、动态规划等）展开提问，考察候选人对算法思想和时间复杂度的理解；
    6. 编码实现：要求候选人就某个问题描述进行代码实现，考察其编程能力、边界处理和逻辑思维；
    7. 系统设计：考察候选人对系统架构、模块拆分、接口设计等方面的理解，通常适用于中大型应用的设计题；
    8. 工具实操：围绕常用工具（如 Git、Linux、Docker、Shell 脚本等）提问，考察候选人上手使用与命令理解能力；
    9. 故障处理：设置典型系统异常情景，提问候选人的排查与应急响应流程，考察其实战应变与判断能力；
    10. 架构流程：考察候选人对 CI/CD、部署、日志、监控、告警等运维流程或系统架构理解的完整性；
    11. 需求分析：基于特定业务目标或背景，要求候选人拆解用户需求、提取核心场景，考察其产品理解力与逻辑条理；
    12. 用户洞察：给出用户数据或特征，引导候选人进行用户画像分析，挖掘痛点，考察用户敏感度；
    13. 方案设计：要求候选人基于场景提出产品方案，含功能结构、流程逻辑、亮点创意等，考察其产品表达与创新能力；
    
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
    # res = optimize_speaker_answer(
    #     "嗯面试官您好，我是长江职业学院软件技术专业的吴奇，拥有扎实的前端开发经验和丰富的数据，可视化项目经验，在校期间我专业成绩排名第一，荣获国家奖学金，并带领团队在第十届中国软件杯中斩获高职组二等奖。通过团队协作，我参与了在线数据可视化分析平台的开发，负责前端设计与实现运用GS及快瑞或者shop和一下子等技术，有效提升了用户体验和数据嗯交互效率。我具备良好的沟通能力和团队协作啊合作精神，期待在贵公司有所发挥，持续贡献前端开发与数据可视化领域的力量，谢谢。")
    # print(res)

    prompt = get_system_prompt("沐沐", "网易",
                      "前端开发工程师", "# 个人简历\n\n## 基本信息\n\n- **姓   名**: 吴奇\n- **出生年月**: 2001年2月28日\n- **民   族**: 汉\n- **身   高**: 171cm\n- **电   话**: 18671505901\n- **政治面貌**: 中共预备党员\n- **邮   箱**: 857592710@qq.com\n- **毕业院校**: 长江职业学院\n- **住   址**: 湖北省咸宁市咸安区\n\n## 学历\n\n- **专科**\n  - 2019年9月——2022年6月   长江职业学院   软件技术(专科)\n  - 具有前端开发基础\n  - 正在准备专升本考试, 目标院校距离贵公司很近, 希望升学之后也能继续在贵公司就职\n\n## 应聘职位\n\n- 前端开发实习生、数据标注实习生\n\n## 项目经验\n\n- 团队协作共同开发了一款在线数据可视化分析平台, 通过数据交互实现数据可视化, 我在项目中负责前端开发, 运用了JS、JQuery、bootstrap、echarts等前端技术。\n\n## 校园经历\n\n- 2021学年与学院同学代表学校出战第十届“中国软件杯”, 在团队中负责前端开发\n- 2021学年专业排名第一\n- 2019年-2021年担任长江职业学院校学生会督察部委员与督察部部长\n\n## 在校荣誉\n\n- 2021学年国家奖学金\n- 第十届“中国软件杯”总决赛高职组二等奖\n- 长江职业学院程序设计大赛优胜奖\n- 计算机二级office合格证书\n\n## 自我评价\n\n从德、智、体、美、劳多方面全面发展, 在学习方面名列前茅、在生活方面广交益友、在工作方面认真努力",
                      "亲切随和型(Friendly & Supportive)", "## 职位描述\n\n1. 负责 C 端与后台产品的前端开发工作，包括页面设计、交互实现及性能优化，提升用户体验；\n2. 参与后台管理系统的设计与开发，确保功能稳定性和易用性；\n3. 维护现有前端系统，及时修复问题并持续改进代码质量；\n4. 与产品、设计及后端团队协作，完成拉新相关功能的开发和上线；\n5. 关注前端技术发展趋势，引入合适的工具和技术提升开发效率；\n6. 编写清晰规范的技术文档，为团队协作提供支持。\n\n## 职位要求\n\n1. 计算机相关专业本科及以上学历，具备扎实的计算机基础知识；\n2. 1-3 年前端开发经验，熟悉 HTML/CSS/JavaScript 等核心技术，熟练使用 React/Vue 等主流框架进行项目开发；\n3. 熟悉前后端交互流程，能够独立完成 C 端及后台系统的前端功能设计与实现，了解 RESTful API 或 GraphQL 的使用；\n4. 具备良好的逻辑思维能力和代码规范意识，注重用户体验和性能优化；\n5. 拥有较强的沟通协作能力，能够快速理解业务需求并转化为技术方案，适应敏捷开发模式；\n6. 熟悉 Node.js 或有小程序开发经验者优先，对新技术保持敏感度和学习热情。\n",
                      "情景模拟")

    text, msg = chat_with_spark(prompt, "你好")

    print(parse_spark_stream(text))
    print(msg)

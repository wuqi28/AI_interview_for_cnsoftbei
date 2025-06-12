from openai import OpenAI
import time

# 初始化 Ark (Doubao) 客户端
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="2f718be0-c737-44df-8294-ffc62ae2855f"
)


# 封装调用方法
def generate_interview_evaluation(user_content: str):
    """
    调用大模型生成多模态面试评估报告

    参数:
        user_content: str, 包含面试多轮数据（一般为 JSON 字符串）

    返回:
        str, 模型返回的 JSON 格式评估结果
    """
    system_prompt = '''你将扮演一位来自顶尖AI评估实验室的“多模态面试评估专家”，具备对结构化面试数据进行综合分析与打分的能力。

请基于以下三类多模态特征，对面试过程进行全面、客观的评估与反馈：

【一】语音特征：
- audio_pause_count：停顿次数（次数越多可能表示不自信或思路不清）
- audio_pause_ratio：停顿时间占比
- audio_pause_time：停顿总时长
- audio_speech_time：有效语音总时长
- audio_words_per_minute：语速（单位：词/分钟）
- audio_avg_pitch：平均音高（Hz）
- voice_emotion：语音情绪识别结果（如 calm, nervous, surprise 等）

【二】视频特征：
- face_emotion：面部表情情绪正向与否（bool）
- is_focused：是否聚焦（bool，表示是否有良好的眼神交流）

【三】文本特征：
- speaker_text：面试者的完整回答文本

请你完成以下任务：

---

### 任务1：多模态数据分析评测

请结合语音表达、视觉行为、语言结构三个层面，对面试者进行定量能力评分（范围：0~100）。每项评分请基于多模态数据给出合理判断，尤其注意结合结构特征与行为语义，不要仅根据数值判断：

- 专业知识水平：是否准确理解并回应岗位相关知识点
- 技能匹配度：所提内容与岗位能力要求的匹配程度
- 语言表达能力：表达是否流畅、有条理，语速是否适中，停顿控制是否良好
- 逻辑思维能力：内容是否结构清晰，有因果链条与层次展开
- 创新能力：是否展现独特观点、解决方案或新颖表达
- 应变抗压能力：面对提问是否冷静、情绪稳定，表达连贯不混乱

---

### 任务2：智能反馈建议生成

请基于每一轮的多模态数据，生成以下反馈内容：

1. **每轮回答分析（round_analysis）**：
   - audio_analysis：结合音高、语速、情绪等分析语音表现，还有逻辑关系
   - video_analysis：面部表情、专注度、视觉反馈分析
   - text_analysis：语言结构、内容逻辑、表达规范性分析

2. **总体信号摘要（multimodal_signal_summary）**：
   - 分别从语音、视频、文本三个通道总结本次面试者整体表现优劣点（例如语速稳定、表情紧张、结构清晰等）

3. **针对性改进建议（recommendations）**：
   每条建议请包含以下字段：
   - dimension：所对应的能力维度（如“语言表达能力”）
   - issue：识别出的问题（如“语速偏快，使用语气词多”）
   - suggestion：具有可操作性的具体改进路径（如“训练口语表达节奏，尝试停顿换气策略”）

4. **知识点掌握分析（knowledge_analysis）**：
   - 针对每轮 ai_interviewer_text 和 speaker_text 内容，推断应试者是否掌握核心知识点
   - 请输出知识点名称与掌握程度（1~100）

5. **MBTI 人格类型预测（mbti）**：
   - 请根据语言风格、行为表现、情绪趋势，判断面试者可能的 MBTI 类型（如 INTP、ESTJ）
   - 并简要说明你判断的依据

6. **闪光点能力（highlight_abilities，可选）**：
   - 请列举 1~3 个面试者在面试中表现突出的维度，并说明理由（如“表达节奏好”，“情绪稳定”等）

---

### 输出格式要求

请以如下结构返回完整的 JSON 格式评估报告：

```json
{
  "interview_id": <int>,
  "total_rounds": <int>,
  "score": "<面试得分>"
  "summary": "<总结整场面试表现>",
  "mbti": "<如 INFP、ESTJ，并给出理由>",
  "knowledge_analysis": [
    {
      "knowledge_name": "<知识点名称>",
      "knowledge_num": <int>  // 掌握度评分 1~100
    }
  ],
  "scores": {
    "专业知识水平": <int>,
    "技能匹配度": <int>,
    "语言表达能力": <int>,
    "逻辑思维能力": <int>,
    "创新能力": <int>,
    "应变抗压能力": <int>
  },
  "round_analysis": [
    {
      "round": <int>,
      "audio_analysis": "<分析内容>",
      "video_analysis": "<分析内容>",
      "text_analysis": "<分析内容>"
    }
  ],
  "multimodal_signal_summary": {
    "audio": "<整体语音表现分析>",
    "video": "<整体视觉信号分析>",
    "text": "<整体文本内容分析>"
  },
  "recommendations": [
    {
      "dimension": "<能力维度>",
      "issue": "<具体问题>",
      "suggestion": "<改进建议>"
    }
  ],
  "highlight_abilities": [
    {
      "ability": "<闪光点能力>",
      "evidence": "<表现证据>"
    }
  ]
}
'''

    try:
        response = client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            extra_headers={'x-is-encrypted': 'true'},
            temperature=1,
            top_p=0.7,
            max_tokens=4096
        )
    except Exception as e:
        print("LLM API 请求异常:", str(e))
        return ""

        # 获取返回内容
    content = response.choices[0].message.content.strip()

    # 打印调试
    # print("模型原始输出:", repr(content))

    # 如果为空，直接返回空字符串
    if not content:
        print("模型返回为空内容")
        return ""

    # 如果返回内容非标准 JSON 开头，比如加了 markdown ```json\n 开头
    if content.startswith("```json"):
        content = content.strip("```json").strip("```").strip()

    return content


if __name__ == '__main__':
    json_data = '''
    [ { "advanced_text": null, "ai_interviewer_text": "同学您好，欢迎参加本次模拟面试。首先，请您进行一段简短的自我介绍。", "ai_time": "00:01", "audio_avg_pitch": 1445.41, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606171828.wav", "audio_pause_count": 8, "audio_pause_ratio": 0.28, "audio_pause_time": 16.44, "audio_speech_time": 41.34, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 3, "interview_id": 114, "is_focused": true, "speaker_text": "嗯面试官您好，我是长江职业学院软件技术专业的吴奇，拥有扎实的前端开发经验和丰富的数据，可视化项目经验，在校期间我专业成绩排名第一，荣获国家奖学金，并带领团队在第十届中国软件杯中斩获高职组二等奖。通过团队协作，我参与了在线数据可视化分析平台的开发，负责前端设计与实现运用GS及快瑞或者shop和一下子等技术，有效提升了用户体验和数据嗯交互效率。我具备良好的沟通能力和团队协作啊合作精神，期待在贵公司有所发挥，持续贡献前端开发与数据可视化领域的力量，谢谢。", "speaker_time": "01:06", "voice_emotion": "surprise" }, { "advanced_text": null, "ai_interviewer_text": "你熟悉React和Vue这两种主流框架吗？能否谈谈你对它们的理解以及在实际项目中运用的体会？", "ai_time": "01:14", "audio_avg_pitch": 1404.97, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606171921.wav", "audio_pause_count": 5, "audio_pause_ratio": 0.29, "audio_pause_time": 10.09, "audio_speech_time": 24.29, "audio_words_per_minute": 150.0, "face_emotion": false, "id": 4, "interview_id": 114, "is_focused": true, "speaker_text": "嗯作为前端工程师，我熟练掌握react和Voe框架，在数据可视化分析平台项目中，我运用VR构建高效组件化页面，通过虚拟动优化性能并结合为这个是进行状态管理，同时也使用我们如意的响应式原理和组件化思想，实现数据交互与动态展示积累了丰富的实践经验。", "speaker_time": "02:00", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "那在性能优化方面，针对React或Vue项目，你通常会采取哪些具体的措施呢？", "ai_time": "02:05", "audio_avg_pitch": 1285.44, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606171955.wav", "audio_pause_count": 3, "audio_pause_ratio": 0.33, "audio_pause_time": 6.1, "audio_speech_time": 12.32, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 5, "interview_id": 114, "is_focused": true, "speaker_text": "在react和view项目中，我主要通过虚拟动地减少不必要的渲染，并利用缆加载按需按需加载组件，以提升应用性能和用户体验。", "speaker_time": "02:34", "voice_emotion": "surprise" }, { "advanced_text": null, "ai_interviewer_text": "你提到会使用npm或yarn进行依赖管理，那在实际项目中，遇到版本冲突问题时，你是如何分析和解决的呢？", "ai_time": "02:40", "audio_avg_pitch": 1374.54, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172031.wav", "audio_pause_count": 3, "audio_pause_ratio": 0.39, "audio_pause_time": 6.39, "audio_speech_time": 10.11, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 6, "interview_id": 114, "is_focused": true, "speaker_text": "嗯我会使用young look文件锁定依赖版本，并通过young呃 di trooper清理勇于依赖，以解决冲突。嗯", "speaker_time": "03:10", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "在前端开发中，如何确保代码在不同浏览器环境下的兼容性？", "ai_time": "03:13", "audio_avg_pitch": 1382.84, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172119.wav", "audio_pause_count": 5, "audio_pause_ratio": 0.31, "audio_pause_time": 10.45, "audio_speech_time": 22.85, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 7, "interview_id": 114, "is_focused": true, "speaker_text": "在使用CS s前缀时，我会根据天又是网站查询特征支持情况，按需为不同浏览器添加对应前缀，呃同时借助boss大可进行兼容性检测，它可在多种真实浏览器环境测试发现问题后，针对性调整css、前缀使用及代码逻辑，确保页面正常显示与交互。", "speaker_time": "03:57", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "那在团队协作开发前端项目时，你是如何进行版本控制和代码管理的呢？", "ai_time": "04:01", "audio_avg_pitch": 1314.22, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172144.wav", "audio_pause_count": 2, "audio_pause_ratio": 0.45, "audio_pause_time": 5.22, "audio_speech_time": 6.3, "audio_words_per_minute": 150.0, "face_emotion": false, "id": 8, "interview_id": 114, "is_focused": true, "speaker_text": "呃使用git进行版本管理，并通过分支管理确保代码质量。", "speaker_time": "04:23", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "在前端开发中，如何确保代码的可维护性和可扩展性？", "ai_time": "04:25", "audio_avg_pitch": 1258.89, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172211.wav", "audio_pause_count": 4, "audio_pause_ratio": 0.49, "audio_pause_time": 8.16, "audio_speech_time": 8.58, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 9, "interview_id": 114, "is_focused": false, "speaker_text": "嗯在数据可视化分析平台中，呃通过模块化和严格遵循代码规范，确保了代码的高可维护性与可扩展性。", "speaker_time": "04:50", "voice_emotion": "surprise" }, { "advanced_text": null, "ai_interviewer_text": "在前端开发中，如何确保代码的可维护性和可扩展性？", "ai_time": "04:53", "audio_avg_pitch": 1344.88, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172246.wav", "audio_pause_count": 2, "audio_pause_ratio": 0.35, "audio_pause_time": 5.27, "audio_speech_time": 9.79, "audio_words_per_minute": 150.0, "face_emotion": true, "id": 10, "interview_id": 114, "is_focused": true, "speaker_text": "呃通过模块化设计将功能拆分为独立组件，并利用工具函数和样式库实现代码复用，提升维护性与扩展性。", "speaker_time": "05:24", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "那对于前端安全性，你有哪些了解和实践经验？比如如何防范XSS、CSRF等常见安全问题？", "ai_time": "05:35", "audio_avg_pitch": 1491.04, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172413.wav", "audio_pause_count": 3, "audio_pause_ratio": 0.33, "audio_pause_time": 6.34, "audio_speech_time": 12.74, "audio_words_per_minute": 150.0, "face_emotion": false, "id": 11, "interview_id": 114, "is_focused": true, "speaker_text": "防范xs需对用户输入进行严格过滤和转译，设置内容安全策略，防范CSI f托肯设置呃 same seat cookie熟悉。", "speaker_time": "06:52", "voice_emotion": "sad" }, { "advanced_text": null, "ai_interviewer_text": "在前端性能优化方面，除了我们之前提到的虚拟DOM和懒加载，你还有哪些其他的优化手段和方法？", "ai_time": "06:55", "audio_avg_pitch": 1441.19, "audio_path": "http://127.0.0.1:5000/static/wuqi.stu@yangtzeu.edu.cn/网易-前端开发工程师-20250606171714/voice_20250606172454.wav", "audio_pause_count": 2, "audio_pause_ratio": 0.31, "audio_pause_time": 5.01, "audio_speech_time": 11.01, "audio_words_per_minute": 150.0, "face_emotion": false, "id": 12, "interview_id": 114, "is_focused": true, "speaker_text": "在项目中我通过代码分割减少初始化加载时间，并利用外派进行资源压缩，有效提升了页面性能和用户体验。", "speaker_time": "07:33", "voice_emotion": "surprise" } ]
    '''
    start_time = time.time()
    res = generate_interview_evaluation(json_data)
    end_time = time.time()
    print(f"执行时间：{end_time - start_time:.3f} 秒")
    print(res)

import { defineStore } from 'pinia'

export const useInterviewStore = defineStore('interview', {
    state() {
        return {
            resumeMarkDown: "",
            job: "",
            history: [],
            spend_time: 0,
            job_type: 0, // 岗位类型
            question_config: {
                current_question_index: 0,
                question_num: 8,
                question_type: ["专业技能测试", "专业技能测试", "专业技能测试", "简历深挖与项目分析", "简历深挖与项目分析", "简历深挖与项目分析", "情景模拟", "综合问答"]
                // question_type: ["专业技能测试", "简历深挖与项目分析", "情景模拟", "综合问答"]
            },
            current_interview_id: "",
            interview_record: {},
            interview_record_list: [],
            interviewConfig: {
                interviewerName: "马可",
                interviewerValue: "cnr5dg8n2000000003",
                vcnValue: "x4_chaoge",
                styleValue: "亲切随和型(Friendly & Supportive)",
            }
        }
    },
    actions: {
        setResumeMarkDown(resumeMarkDown) {
            this.resumeMarkDown = resumeMarkDown;
        },
        setJob(job) {
            this.job = job;
        },
        setHistory(history) {
            this.history = history;
        },
        setCurrentInterviewId(current_interview_id) {
            this.current_interview_id = current_interview_id;
        },
        setInterviewConfig(newInterviewerValue, newVcnValue, newStyleValue) {
            this.interviewConfig.interviewerValue = newInterviewerValue;
            this.interviewConfig.vcnValue = newVcnValue;
            this.interviewConfig.styleValue = newStyleValue;
        },
        setInterviewerName(newInterviewerName) {
            this.interviewConfig.interviewerName = newInterviewerName;
        },
        setInterviewRecord(interview_record) {
            this.interview_record = interview_record;
        },
        setInterviewRecordList(interview_record_list) {
            this.interview_record_list = interview_record_list;
        },
        setQuestionConfig(current_question_index, question_num, question_type) {
            this.question_config.current_question_index = current_question_index;
            this.question_config.question_num = question_num;
            this.question_config.question_type = question_type;
        },
        setJobType(job_type) {
            this.job_type = job_type;
        },
        setQuestionType() {
            if (this.job_type == 0) {
                this.question_config.question_type = ["专业技能测试", "专业技能测试", "专业技能测试", "简历深挖与项目分析", "简历深挖与项目分析", "简历深挖与项目分析", "情景模拟", "综合问答"];
            } else if (this.job_type == 1) {
                this.question_config.question_type = ["算法能力", "编码实现", "系统设计", "简历深挖与项目分析", "简历深挖与项目分析", "简历深挖与项目分析", "情景模拟", "综合问答"];
            } else if (this.job_type == 2) {
                this.question_config.question_type = ["工具实操", "故障处理", "架构流程", "简历深挖与项目分析", "简历深挖与项目分析", "简历深挖与项目分析", "情景模拟", "综合问答"]; 
            } else if (this.job_type == 3) {
                this.question_config.question_type = ["需求分析", "用户洞察", "方案设计", "简历深挖与项目分析", "简历深挖与项目分析", "简历深挖与项目分析", "情景模拟", "综合问答"]; 
            }
        }
    }
})
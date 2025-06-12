import { defineStore } from 'pinia'

export const useResumeStore = defineStore('resume', {
    state(){
        return {
            resumeList: [],
            resumeMsg: "请登录后查看简历"
        }  
    },
    actions: {
        setResumeList(resumeList) {
            this.resumeList = resumeList;
        },
        setResumeMsg(resumeMsg) {
            this.resumeMsg = resumeMsg;
        }
    }

})
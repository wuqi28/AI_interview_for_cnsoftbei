import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './modules/router'
import pinia from './modules/pinia'
import TDesign from 'tdesign-vue-next';
import { useUserStore } from '@/stores/userStore';
import { useResumeStore } from '@/stores/resumeStore';
import { useInterviewStore } from '@/stores/interviewStore';
import axiosLocal from '@/modules/axiosLocal'

// 引入组件库的少量全局样式变量
import 'tdesign-vue-next/es/style/index.css';

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(TDesign);

const userStore = useUserStore()
const resumeStore = useResumeStore()
const interviewStore = useInterviewStore()

const user = localStorage.getItem('user')
let current_interview_id = localStorage.getItem('current_interview_id')

if (user) {
    console.log("user is exist", JSON.parse(user))
    userStore.setUser(JSON.parse(user))
    // console.log(userStore.user.email)

    axiosLocal.get('/resume/get_resume', { params: { email: userStore.user.email } })
        .then((res) => {
            // console.log(res.data);
            if (res.data.code == 200) {
                resumeStore.setResumeList(res.data.data);
            }
        })
}

current_interview_id = "网易-前端开发工程师-20250606171714"
if (current_interview_id) {
    console.log("current_interview_id is exist", current_interview_id)
    interviewStore.setCurrentInterviewId(current_interview_id)
}

app.mount('#app')

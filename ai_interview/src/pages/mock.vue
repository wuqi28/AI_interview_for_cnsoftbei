<script setup>
import { UserBusinessIcon, LightbulbIcon, VideoCameraMinusIcon, TimeIcon, AnalyticsIcon } from 'tdesign-icons-vue-next';
import axiosLocal from '../modules/axiosLocal';
import { useInterviewStore } from '../stores/interviewStore';
import { useUserStore } from '../stores/userStore';
import { initAvatar, speak, close } from '../modules/avatarInit.js'
import StreamText from '@/components/StreamText.vue';
import { useInterviewTimer } from '@/modules/interviewTimer.js'
import { useRouter } from 'vue-router'

const router = useRouter()

const interviewStore = useInterviewStore()
const userStore = useUserStore()

const question = ref('同学您好，欢迎参加本次模拟面试。首先，请您进行一段简短的自我介绍。')

const msgVisible = ref(false)
const interviewText = ref('')
const streamText = ref(null);

const parsingText = ref('')

const { startTimer, stopTimer, formattedTime } = useInterviewTimer()

const historyList = ref([])
const historyListTime = ref([])

const faceEmotionList = ref([])
const faceEmotion = ref(false)

const lookingAtScreenList = ref([])
const lookingAtScreen = ref(false)


const isAddingVideo = ref(false)
const bearingDegreesList = ref([])
const averageBearingDegrees = ref(0)
const gazeStrengthList = ref([])
const averageGazeStrength = ref(0)

const runStream = async () => {
    console.log('开始播放...')
    await streamText.value?.start()
    console.log('✅ 播放完毕，执行后续逻辑')
    startThinking()
}

const ai_time = ref('')
const speaker_time = ref('')

const msgOnClickConfirm = () => {
    // sendText(`同学您好，欢迎参加本次模拟面试。我是您的面试官${interviewStore.interviewConfig.interviewerName}，来自${interviewStore.job.company}的${interviewStore.job.title}，很高兴与您见面。请保持网络畅通。首先，请您进行一段简短的自我介绍。`)
    startTimer()
    sendText(question.value)
    msgVisible.value = false
    interviewText.value = question.value
    interviewStore.setHistory([{
        role: 'assistant',
        content: question.value
    }])
    setTimeout(() => {
        // text.value = `同学您好，欢迎参加本次模拟面试。我是您的面试官${interviewStore.interviewConfig.interviewerName}，来自${interviewStore.job.company}的${interviewStore.job.title}，很高兴与您见面。请保持网络畅通。首先，请您进行一段简短的自我介绍。`
        // streamText.value?.start();
        runStream()
        intelligent_parsing()
        historyList.value.push({ "role": "assistant", "content": question.value })
        historyListTime.value.push(formattedTime.value.toString())
        ai_time.value = formattedTime.value.toString()
    }, 1500)
}

const closeInterview = () => {
    shutdown()
    stopTimer()
    // router.push('/report')
}

const intelligent_parsing = () => {
    axiosLocal.post('/interview/intelligent_parsing', {
        current_interview_id: interviewStore.current_interview_id,
        email: userStore.user.email,
        question: question.value,
    }).then((resp) => {
        if (resp.data.code === 200) {
            parsingText.value = resp.data.data.parsing_text
            console.log('✅ 答案提示:', resp.data.data.answer_text)
            // interviewText.value = parsingText.value
            // setTimeout(() => {
            //     runStream()
            // }, 1500)
        }
    }).catch((err) => {
        console.error('❌ 智能解析失败:', err)
    })
}

const startFaceEmotionList = () => {
    faceEmotionList.value.push(isFaceEmotion.value)
}

const stopFaceEmotionList = () => {
    const relaxedCount = faceEmotionList.value.filter(item => item === true).length
    const tenseCount = faceEmotionList.value.length - relaxedCount
    faceEmotion.value = relaxedCount >= tenseCount
    faceEmotionList.value = []
}

const startLookingAtScreenList = () => {
    lookingAtScreenList.value.push(isLookingAtScreen.value)
}

const stopLookingAtScreenList = () => {
    const lookingCount = lookingAtScreenList.value.filter(item => item === true).length
    const notLookingCount = lookingAtScreenList.value.length - lookingCount
    lookingAtScreen.value = lookingCount >= notLookingCount
    lookingAtScreenList.value = []
}

const stopBearingDegreesList = () => {
    const total = bearingDegreesList.value.reduce((acc, val) => acc + val, 0)
    averageBearingDegrees.value = total / bearingDegreesList.value.length
    bearingDegreesList.value = []
}

const stopGazeStrengthList = () => {
    const total = gazeStrengthList.value.reduce((acc, val) => acc + val, 0)
    averageGazeStrength.value = total / gazeStrengthList.value.length
    gazeStrengthList.value = []
}

onMounted(() => {
    msgVisible.value = true
})
// -------------------------------------语音转写模块-----------------------------------------
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'

const transcript = ref('')
const finalTranscript = ref('')
const isRecognizing = ref(false)
const isTranscript = ref(false)
const isThinking = ref(false)

let recognition = null
let resolveFinal = null
let audioContext = null
let analyser = null
let microphone = null
let animationFrame = null
let mediaRecorder = null
let audioChunks = []

const canvasRef = ref(null)
const textRef = ref(null)

onMounted(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
        MessagePlugin.error('当前浏览器不支持语音识别')
        return
    }

    recognition = new SpeechRecognition()
    recognition.lang = 'zh-CN'
    recognition.continuous = true
    recognition.interimResults = true

    recognition.onresult = (event) => {
        let temp = ''
        for (let i = event.resultIndex; i < event.results.length; i++) {
            temp += event.results[i][0].transcript
        }
        transcript.value = temp

        if (event.results[event.results.length - 1].isFinal) {
            finalTranscript.value += temp
            resolveFinal?.()
            resolveFinal = null // 避免被 onend 重复调用
        }
    }

    recognition.onerror = () => stopRecognition()
    recognition.onend = () => {
        resolveFinal?.()
        resolveFinal = null
        stopRecognition()
    }
})

onUnmounted(() => stopRecognition())

watch(transcript, () => {
    if (textRef.value) {
        textRef.value.scrollLeft = textRef.value.scrollWidth
    }
})

async function toggleRecognition() {
    if (!recognition) return

    if (!isRecognizing.value) {
        isAddingVideo.value = true
        startLookingAtScreenList()
        startFaceEmotionList()
        if (thinking.value == true) {
            stopThinking()
        }
        recognition.start()
        finalTranscript.value = ''
        isRecognizing.value = true
        isTranscript.value = true
        startRecording()
    } else {
        parsingText.value = ''
        isAddingVideo.value = false
        stopBearingDegreesList()
        stopGazeStrengthList()
        stopLookingAtScreenList()
        stopFaceEmotionList()
        // ✅ 先等待 finalTranscript 准备好，再 stop
        await new Promise((resolve) => {
            resolveFinal = resolve
            setTimeout(resolve, 1500) // 最多等待 1.5 秒
        })
        streamText.value?.clear()
        transcript.value = ''
        isThinking.value = true
        resolveFinal = null
        recognition.stop()
        isRecognizing.value = false
        isTranscript.value = false
        stopRecording()
    }
}

function stopRecognition() {
    recognition?.stop()
    isRecognizing.value = false
    stopRecording()
}

function clearText() {
    transcript.value = ''
    finalTranscript.value = ''
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        audioContext = new AudioContext()
        analyser = audioContext.createAnalyser()
        microphone = audioContext.createMediaStreamSource(stream)
        microphone.connect(analyser)

        mediaRecorder = new MediaRecorder(stream)
        audioChunks = []

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data)
            }
        }

        mediaRecorder.onstop = () => {
            // console.log('🎙 最终文本:', finalTranscript.value)
            // if (!finalTranscript.value.trim()) {
            //     MessagePlugin.warning('识别结果为空，请重试！')
            //     return
            // }
            // console.log(interviewStore.question_config.question_type[interviewStore.question_config.current_question_index])

            console.log(averageBearingDegrees.value, averageGazeStrength.value)

            historyListTime.value.push(formattedTime.value.toString())
            speaker_time.value = formattedTime.value.toString()

            const blob = new Blob(audioChunks, { type: 'audio/wav' })
            const formData = new FormData()
            formData.append('current_interview_id', interviewStore.current_interview_id)
            formData.append('email', userStore.user.email)
            formData.append('file', blob, 'record.wav')
            formData.append('final_transcript', finalTranscript.value)
            formData.append('history', JSON.stringify(interviewStore.history))
            formData.append('round', interviewStore.question_config.current_question_index + 1)
            formData.append('question_type', interviewStore.question_config.question_type[interviewStore.question_config.current_question_index++])
            formData.append('face_emotion', faceEmotion.value)
            formData.append('looking_at_screen', lookingAtScreen.value)
            formData.append('ai_time', ai_time.value)
            formData.append('speaker_time', speaker_time.value)
            formData.append('average_bearing_degrees', averageBearingDegrees.value)
            formData.append('average_gaze_strength', averageGazeStrength.value)

            axiosLocal.post('/interview/chat_with_interviewer', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((resp) => {
                if (resp.data.code === 200) {
                    finalTranscript.value = ''
                    let resp_data = resp.data.data
                    console.log('✅ 上传成功:', resp_data)

                    if (resp_data.history.length == 3) {
                        const newMessage = {
                            content: interviewText.value,
                            role: 'assistant'
                        }
                        resp_data.history.splice(1, 0, newMessage)

                    }
                    nextStep()
                    historyList.value = resp_data.history
                    historyList.value = historyList.value.slice(1)
                    historyListTime.value.push(formattedTime.value.toString())
                    ai_time.value = formattedTime.value.toString()
                    interviewStore.setHistory(resp_data.history)
                    isThinking.value = false
                    question.value = resp_data.history[resp_data.history.length - 1].content
                    sendText(resp_data.history[resp_data.history.length - 1].content)
                    interviewText.value = resp_data.history[resp_data.history.length - 1].content
                    intelligent_parsing()
                    setTimeout(() => {
                        // streamText.value?.start();
                        runStream()
                    }, 1500)
                }
            }).catch((err) => {
                console.error('❌ 上传失败:', err)
            })
        }

        mediaRecorder.start()
        drawWave()
    })
}

function stopRecording() {
    mediaRecorder?.stop()
    cancelAnimationFrame(animationFrame)
    audioContext?.close()
    audioContext = null
}

function drawWave() {
    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)
    const canvas = canvasRef.value
    const ctx = canvas.getContext('2d')

    canvas.width = 600
    canvas.height = 80

    const draw = () => {
        animationFrame = requestAnimationFrame(draw)
        analyser.getByteFrequencyData(dataArray)

        ctx.fillStyle = '#f6fef8'
        ctx.fillRect(0, 0, canvas.width, canvas.height)

        const barWidth = (canvas.width / bufferLength) * 2.5
        let x = 0
        for (let i = 0; i < bufferLength; i++) {
            const barHeight = dataArray[i] / 2
            ctx.fillStyle = 'rgb(61, 214, 140)'
            ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
            x += barWidth + 1
        }
    }

    draw()
}

const thinking = ref(false)
const countdown = ref(30)
let timer = null

function startThinking() {
    thinking.value = true
    countdown.value = 30

    timer && clearInterval(timer)
    timer = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--
        } else {
            stopThinking()
            onThinkingFinished()
        }
    }, 1000)
}

function stopThinking() {
    clearInterval(timer)
    thinking.value = false
}

function onThinkingFinished() {
    console.log('✅ 倒计时结束，进入下一步逻辑')
}

onUnmounted(() => {
    clearInterval(timer)
})
//--------------------------------------------摄像头----------------------------------------------
import human from '@/modules/human'

const video = ref(null)
const canvas = ref(null)
const isLookingAtScreen = ref(false)
const isFaceEmotion = ref(false)

onMounted(async () => {
    await human.load()

    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream

    video.value.onloadedmetadata = () => {
        video.value.play()

        // ✅ 设置 canvas 的真实像素大小（不是 CSS 尺寸）
        canvas.value.width = video.value.videoWidth
        canvas.value.height = video.value.videoHeight

        runDetection()
    }
})

const runDetection = async () => {
    const ctx = canvas.value.getContext('2d')

    const detectLoop = async () => {
        const result = await human.detect(video.value)

        ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

        // ✅ 绘制人脸（确保 canvas 尺寸正确）
        await human.draw.face(canvas.value, result.face, {
            drawGaze: true,
            drawPolygons: true,
            drawPoints: false,
            drawBoxes: false,
            drawLabels: false
        })

        if (result.face.length > 0) {
            const face = result.face[0]
            // console.log(face)


            // 表情检测
            const positiveEmotions = ['neutral', 'happy', 'surprised']
            const topEmotion = face.emotion[0]
            if (face.emotion[0].score > 0.6) {
                // console.log('表情:', face.emotion[0])
                isFaceEmotion.value = positiveEmotions.includes(topEmotion.emotion) ? true : false
            }

            const rotation = face.rotation
            const bearingDegrees = rotation.gaze.bearing * (180 / Math.PI)
            const gazeStrength = rotation.gaze.strength

            if (isAddingVideo.value == true) {
                // 视线角度
                bearingDegreesList.value.push(bearingDegrees)
                // 视线强度
                gazeStrengthList.value.push(gazeStrength)
            }

            // console.log('视线角度:', bearingDegrees.toFixed(1))
            // console.log('视线强度:', gazeStrength.toFixed(3))

            // ✅ 判断是否专注于屏幕（视线直视 + 强度足够）
            isLookingAtScreen.value = gazeStrength <= 0.10

            // if (isLookingAtScreen) {
            //     // console.log('✅ 用户专注于屏幕')
            //     isLookingAtScreen.value = true
            // } else {
            //     // console.warn('⚠️ 用户未专注屏幕（可能看手机、走神）')
            //     isLookingAtScreen.value = false
            // }

        }

        requestAnimationFrame(detectLoop)
    }

    detectLoop()
}
// ------------------------------------------------数字人-----------------------------------------------
let avatar
let avatarid = interviewStore.interviewConfig.interviewerValue
let vcn = interviewStore.interviewConfig.vcnValue

onMounted(() => {
    avatar = initAvatar(avatarid, vcn)
})
const sendText = (text) => {
    speak(text)
}
const shutdown = () => {
    close()
}

const dynamicTop = computed(() => {
    switch (interviewStore.interviewConfig.interviewerValue) {
        case '110017006': return '30px'
        case '110332017': return '100px'
        default: return '50px'
    }
})
// ---------------------------------------------------进度条--------------------------------------------------
// ✅ 原始类型 → 显示颜色
const typeColorMap = {
    "专业技能测试": "#0052D9",
    "简历深挖与项目分析": "#FAAD14",
    "情景模拟": "#52C41A",
    "综合问答": "#722ED1"
}

// ✅ 原始类型 → 简化展示名
const typeAliasMap = {
    "专业技能测试": "专业技能",
    "简历深挖与项目分析": "简历深挖",
    "情景模拟": "情景模拟",
    "综合问答": "综合问答"
}

const rawTypes = interviewStore.question_config.question_type

// ✅ 生成步骤列表（含原始类型和映射后的 label）
const stepList = rawTypes.map(type => ({
    type,
    label: typeAliasMap[type] || type
}))

const currentStep = ref(-1)

const nextStep = () => {
    if (currentStep.value + 1 < stepList.length) {
        currentStep.value++
    } else {
        closeInterview()
    }
}
</script>

<template>
    <t-head-menu theme="light" style="width: 100%;">
        <template #logo>
            <img height="28" src="../../public/img/logo_chinese.png" alt="logo" />
        </template>
        <div style="
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            font-weight: 500;
            font-size: 16px;
        ">
            {{ interviewStore.job.company }}
            -
            {{ interviewStore.job.title }}
            时长:
            {{ formattedTime }}
        </div>
        <template #operations>
            <t-space>
                <t-button variant="outline" theme="danger" :disabled="false">
                    {{ thinking ? `请思考... (${countdown}s)` : '思考时间' }}
                </t-button>
                <t-button @click="msgVisible = true" variant="outline" theme="success" ghost>开始面试</t-button>
                <t-button @click="closeInterview" variant="outline" theme="primary" ghost>结束面试</t-button>
            </t-space>
        </template>
    </t-head-menu>
    <t-dialog width="600px" v-model:visible="msgVisible" theme="info" header="面试前提示" :cancel-btn="null"
        @confirm="msgOnClickConfirm">
        <template #body>
            <p>1. 本次面试由<span style="font-weight: bold;">数字人面试官</span>进行模拟。</p>
            <p>2. 系统将通过智能解析，对面试官提出的问题提供<span style="font-weight: bold;">实时引导</span>，辅助作答。</p>
            <p>3. 面试过程将采集<span style="font-weight: bold;">面部情绪</span>和<span
                    style="font-weight: bold;">视线追踪</span>信息，以评估作答情绪和专注度。</p>
            <p>4. 每个问题有<span style="font-weight: bold;">30 秒思考时间</span>，如准备就绪，可提前点击“开始回答”。</p>
            <p>5. 如需结束面试，可手动点击“结束面试”，系统将根据表现生成<span style="font-weight: bold;">面试评测报告</span>。</p>
            <p>6. <span style="font-weight: bold; color: #0052D9;">如您已准备好，点击“确认”即可开始面试。</span></p>
        </template>
    </t-dialog>


    <div class="mock-page">
        <div class="interview-progress">
            <t-steps :current="currentStep" layout="horizontal" style="width: 100%;">
                <t-step-item v-for="(step, index) in stepList" :key="index" :title="`第 ${index + 1} 轮 ${step.label}`">
                    <template #icon>
                        <div class="custom-dot" :style="{ backgroundColor: typeColorMap[step.type] || '#ccc' }"></div>
                    </template>
                </t-step-item>
            </t-steps>

            <!-- <div style="margin-top: 24px; text-align: center">
      <t-button theme="primary" @click="nextStep" :disabled="currentStep >= stepList.length">
        下一轮问答
      </t-button>
    </div> -->
        </div>
        <t-row :gutter="20">
            <t-col :span="4">
                <t-card header-bordered style="margin-bottom: 20px; height: 65vh;">
                    <template #title>
                        <t-icon name="user-business" style="margin-right: 4px; color: rgb(0, 82, 217);" />
                        面试官
                    </template>
                    <div id="video-container" style=" width: 500px; height: 400px; /* 显示一半高度 */
    overflow: hidden;
    position: relative;
  ">
                        <!-- 容器需要设置尺寸，否则视频不会显示 -->
                        <div class="wrapper" :style="{
                            width: '810px',
                            height: '600px',
                            transform: 'scale(1.5) translateX(-130px)',
                            position: 'absolute',
                            top: dynamicTop,
                            left: '40px'
                        }"></div>
                    </div>
                    <t-divider />
                    <el-scrollbar height="80px">
                        <StreamText ref="streamText" :text="interviewText" :auto-start="false" />
                        <Thinking v-if="isThinking" />
                    </el-scrollbar>
                </t-card>
                <t-card header-bordered style="height: 21vh;">
                    <template #title>
                        <t-icon name="analytics" style="margin-right: 4px; color: rgb(0, 82, 217);" />
                        智能解析
                    </template>
                    <el-scrollbar height="100px">
                        <div v-if="parsingText === ''">
                            <Thinking v-if="true" />
                        </div>
                        <div v-else>
                            <AnswerSuggestion :rawText="parsingText" />
                        </div>
                    </el-scrollbar>
                </t-card>
            </t-col>

            <t-col :span="4">
                <t-card header-bordered style="margin-bottom: 20px; height: 60vh;">
                    <template #title>
                        <t-icon name="video-camera-minus" style="margin-right: 4px; color: rgb(43, 164, 113);" />
                        摄像头
                    </template>
                    <div class="camera-wrapper">
                        <video ref="video" autoplay muted playsinline class="camera-video" />
                        <canvas ref="canvas" class="camera-canvas" />
                    </div>
                </t-card>
                <t-card style="height: 26vh;">
                    <!-- 波形 Canvas -->
                    <canvas ref="canvasRef" class="waveform"></canvas>

                    <!-- 单行转写显示区域 -->
                    <div class="transcript-line" ref="textRef">
                        {{ isTranscript ? transcript : "准备好了就点击开始回答吧!" }}
                    </div>

                    <!-- 控制按钮 -->
                    <t-space class="actions" size="medium">
                        <t-button @click="toggleRecognition" :theme="isRecognizing ? 'danger' : 'primary'">
                            {{ isRecognizing ? '回答完毕' : '开始回答' }}
                        </t-button>
                        <t-button variant="outline" theme="default" @click="clearText">清空</t-button>
                    </t-space>
                </t-card>
            </t-col>

            <t-col :span="4">
                <t-card header-bordered style="margin-bottom: 20px;">
                    <template #title>
                        <t-icon name="lightbulb" style="margin-right: 4px; color: rgb(255, 183, 0);" />
                        问题分析
                    </template>
                    <div v-if="isLookingAtScreen">
                        <p style="color: green;">✅ 用户专注于屏幕</p>
                    </div>
                    <div v-else>
                        <p style="color: red;">⚠️ 用户未专注于屏幕</p>
                    </div>

                    <div v-if="isFaceEmotion">
                        <p style="color: green;">😄 用户当前情绪放松</p>
                    </div>
                    <div v-else>
                        <p style="color: red;">😔 用户当前情绪紧张</p>
                    </div>

                </t-card>
                <t-card header-bordered style="height: 67vh;">
                    <template #title>
                        <t-icon name="time" style="margin-right: 4px; color: rgb(0, 82, 217);" />
                        对话历史
                    </template>

                    <InterviewHistory :messages="historyList" :mockDurations="historyListTime" />

                </t-card>
            </t-col>
        </t-row>
    </div>
</template>

<style scoped>
.mock-page {
    /* 设置背景色为 RGB 值 236, 245, 255 */
    background-color: rgb(238, 238, 238);
    /* 确保背景色覆盖整个视口高度 */
    min-height: 94vh;
    /* 添加内边距 */
    padding: 5px 20px 20px 20px;
    /* 设置盒模型为 border-box */
    box-sizing: border-box;
    /* 使用 flex 布局 */
    display: flex;
    flex-direction: column;
}

.actions {
    margin-top: 16px;
    display: flex;
    justify-content: center;
}

.waveform {
    width: 100%;
    height: 10vh;
    display: block;
    border-radius: 8px;
    margin-bottom: 12px;
    margin-top: 12px;
    background: rgb(226, 241, 229);
}

.transcript-line {
    height: 36px;
    line-height: 36px;
    background: #f9f9f9;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
    padding: 0 10px;
    font-size: 16px;
    color: #333;
    overflow-x: hidden;
    /* 禁止滚动条 */
    white-space: nowrap;
    margin-bottom: 12px;
    position: relative;
}

/* 滚动动画容器 */
.transcript-line::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 40px;
    height: 100%;
}

.camera-wrapper {
    position: relative;
    width: 100%;
    /* max-width: 480px; */
    aspect-ratio: 4 / 3;
    margin: 0 auto;
    border-radius: 5px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    height: 50vh;
}

.camera-video,
.camera-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.camera-canvas {
    z-index: 2;
    pointer-events: none;
}

.custom-dot {
    margin-top: 4px;
    width: 15px;
    height: 15px;
    border-radius: 50%;
}

.interview-progress {
    padding: 0px 10px 0px 20px;
    width: 100%;
    box-sizing: border-box;
}
</style>

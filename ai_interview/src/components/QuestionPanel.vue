<template>
  <t-card 
    theme="poster2" 
    bordered 
    hover-shadow
    class="question-card"
  >
    <!-- 题目标题和难度标签 -->
    <template #header>
      <div class="question-header">
        <div class="title-section">
          <t-tag theme="primary" size="small" class="question-number">
            第{{ questionNumber }}题
          </t-tag>
          <h3 class="question-title">{{ question.title }}</h3>
        </div>
        <div class="meta-section">
          <t-tag theme="warning" variant="light" size="small" class="position-tag">
            {{ question.position }}
          </t-tag>
          <t-tag 
            :theme="getDifficultyTheme(question.difficulty)"
            variant="light" 
            size="small"
            class="difficulty-tag"
          >
            {{ question.difficulty }}
          </t-tag>
        </div>
      </div>
    </template>

    <!-- 题目内容 -->
    <div class="question-content">
      <p class="content-text">{{ question.content }}</p>
      
      <!-- 知识点标签 -->
      <div class="knowledge-points">
        <span class="tags-label">知识点：</span>
        <t-space size="small">
          <t-tag 
            v-for="(point, index) in question.points"
            :key="index"
            size="small"
            variant="outline"
            theme="primary"
          >
            {{ point }}
          </t-tag>
        </t-space>
      </div>
    </div>

    <!-- 回答区域 -->
    <template #footer>
      <div class="answer-section">
        <t-divider>我的回答</t-divider>
        
        <!-- 回答方式选择 -->
        <div class="answer-mode">
          <t-radio-group v-model="answerMode" variant="default-filled">
            <t-radio value="text">文字回答</t-radio>
            <t-radio value="voice">语音回答</t-radio>
          </t-radio-group>
        </div>

        <!-- 文字回答 -->
        <div v-if="answerMode === 'text'" class="text-answer">
          <t-textarea
            v-model="textAnswer"
            placeholder="请输入您的答案..."
            :autosize="{ minRows: 4, maxRows: 8 }"
            class="answer-textarea"
          />
          <div class="answer-actions">
            <t-space>
              <t-button size="small" @click="clearTextAnswer">清空</t-button>
              <t-button theme="primary" size="small" @click="saveAnswer">
                保存答案
              </t-button>
            </t-space>
          </div>
        </div>

        <!-- 语音回答 -->
        <div v-else class="voice-answer">
          <div class="voice-controls">
            <t-button
              v-if="!isRecording"
              theme="primary"
              size="large"
              @click="startRecording"
              class="record-button"
            >
              <template #icon>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </template>
              开始录音
            </t-button>
            
            <t-button
              v-else
              theme="danger"
              size="large"
              @click="stopRecording"
              class="record-button recording"
            >
              <template #icon>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <rect x="6" y="6" width="12" height="12" rx="2"/>
                </svg>
              </template>
              停止录音
            </t-button>
          </div>

          <!-- 录音状态 -->
          <div v-if="isRecording" class="recording-status">
            <div class="recording-indicator">
              <div class="pulse"></div>
              <span>正在录音中...</span>
            </div>
            <div class="recording-time">{{ recordingTime }}s</div>
          </div>

          <!-- 语音转文字结果 -->
          <div v-if="voiceText" class="voice-result">
            <t-textarea
              v-model="voiceText"
              placeholder="语音识别结果..."
              :autosize="{ minRows: 3, maxRows: 6 }"
              readonly
            />
            <div class="voice-actions">
              <t-space>
                <t-button size="small" @click="clearVoiceAnswer">清空</t-button>
                <t-button size="small" @click="retryRecording">重新录音</t-button>
                <t-button theme="primary" size="small" @click="saveAnswer">
                  保存答案
                </t-button>
              </t-space>
            </div>
          </div>
        </div>

        <!-- 已保存的答案 -->
        <div v-if="savedAnswer" class="saved-answer">
          <t-alert theme="success" message="答案已保存" close>
            <div class="saved-content">{{ savedAnswer }}</div>
          </t-alert>
        </div>
      </div>
    </template>
  </t-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'

// 接收 Props
const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  questionNumber: {
    type: Number,
    required: true
  }
})

// 回答相关状态
const answerMode = ref('text')
const textAnswer = ref('')
const voiceText = ref('')
const savedAnswer = ref('')

// 语音识别状态
const isRecording = ref(false)
const recordingTime = ref(0)
const recognition = ref(null)
const recordingTimer = ref(null)

// 难度主题颜色
const getDifficultyTheme = (difficulty) => {
  const themeMap = {
    '初级': 'success',
    '中级': 'warning',
    '高级': 'danger'
  }
  return themeMap[difficulty] || 'default'
}

// 初始化语音识别
const initSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition.value = new SpeechRecognition()
    recognition.value.continuous = true
    recognition.value.interimResults = true
    recognition.value.lang = 'zh-CN'

    recognition.value.onresult = (event) => {
      let finalTranscript = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        }
      }
      if (finalTranscript) {
        voiceText.value = finalTranscript
      }
    }

    recognition.value.onerror = (event) => {
      MessagePlugin.error(`语音识别错误: ${event.error}`)
      stopRecording()
    }

    recognition.value.onend = () => {
      stopRecording()
    }
  } else {
    MessagePlugin.warning('您的浏览器不支持语音识别功能')
  }
}

// 开始录音
const startRecording = () => {
  if (!recognition.value) {
    MessagePlugin.error('语音识别未初始化')
    return
  }

  isRecording.value = true
  recordingTime.value = 0
  voiceText.value = ''

  recognition.value.start()

  recordingTimer.value = setInterval(() => {
    recordingTime.value++
  }, 1000)

  MessagePlugin.info('开始录音，请说话...')
}

// 停止录音
const stopRecording = () => {
  if (recognition.value && isRecording.value) {
    recognition.value.stop()
  }
  isRecording.value = false
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
    recordingTimer.value = null
  }
  if (voiceText.value) {
    MessagePlugin.success('录音完成，语音已转换为文字')
  }
}

// 重新录音
const retryRecording = () => {
  voiceText.value = ''
  startRecording()
}

// 清空文字答案
const clearTextAnswer = () => {
  textAnswer.value = ''
}

// 清空语音答案
const clearVoiceAnswer = () => {
  voiceText.value = ''
}

// 保存答案
const saveAnswer = () => {
  const answer = answerMode.value === 'text' ? textAnswer.value : voiceText.value
  if (!answer.trim()) {
    MessagePlugin.warning('请先输入或录制答案')
    return
  }
  savedAnswer.value = answer
  MessagePlugin.success('答案已保存')
}

// 初始化挂载/卸载
onMounted(() => {
  initSpeechRecognition()
})
onUnmounted(() => {
  if (recordingTimer.value) {
    clearInterval(recordingTimer.value)
  }
  if (recognition.value && isRecording.value) {
    recognition.value.stop()
  }
})
</script>


<style scoped>
.question-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.question-number {
  align-self: flex-start;
}

.question-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.4;
}

.meta-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.question-content {
  margin: 16px 0;
}

.content-text {
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  margin: 0 0 16px 0;
  white-space: pre-wrap;
}

.knowledge-points {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px;
  background-color: #f8fafc;
  border-radius: 8px;
}

.tags-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  flex-shrink: 0;
}

.answer-section {
  margin-top: 16px;
}

.answer-mode {
  margin-bottom: 16px;
}

.text-answer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-textarea {
  width: 100%;
}

.answer-actions {
  display: flex;
  justify-content: flex-end;
}

.voice-answer {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

.voice-controls {
  display: flex;
  justify-content: center;
}

.record-button {
  min-width: 120px;
  height: 48px;
}

.record-button.recording {
  animation: pulse 1.5s infinite;
}

.recording-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background-color: #fef3f2;
  border-radius: 8px;
  border: 1px solid #fecaca;
}

.recording-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #dc2626;
  font-weight: 500;
}

.pulse {
  width: 8px;
  height: 8px;
  background-color: #dc2626;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

.recording-time {
  font-size: 18px;
  font-weight: 600;
  color: #dc2626;
}

.voice-result {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.voice-actions {
  display: flex;
  justify-content: flex-end;
}

.saved-answer {
  margin-top: 16px;
}

.saved-content {
  margin-top: 8px;
  padding: 12px;
  background-color: #f0f9ff;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.5;
}

.answer-section {
  margin-top: -80px; /* 负值越大，上移距离越远 */
}
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .question-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .meta-section {
    flex-direction: row;
    align-items: flex-start;
    align-self: stretch;
    justify-content: flex-start;
  }
  
  .question-title {
    font-size: 16px;
  }
  
  .knowledge-points {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .record-button {
    min-width: 100px;
    height: 44px;
  }
}
</style>

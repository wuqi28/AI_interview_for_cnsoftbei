<template>
  <t-card title="实时语音转写" class="card">
    <!-- 波形 Canvas -->
    <canvas ref="canvasRef" class="waveform"></canvas>

    <!-- 单行转写显示区域 -->
    <div class="transcript-line" ref="textRef">{{ transcript }}</div>

    <!-- 控制按钮 -->
    <t-space class="actions" size="medium">
      <t-button @click="toggleRecognition" :theme="isRecognizing ? 'danger' : 'primary'">
        {{ isRecognizing ? '回答完毕' : '开始回答' }}
      </t-button>
      <t-button variant="outline" theme="default" @click="clearText">清空</t-button>
      <t-button theme="success" @click="submitText">提交</t-button>
    </t-space>
  </t-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'

const transcript = ref('')
const isRecognizing = ref(false)

let recognition = null
let audioContext = null
let analyser = null
let microphone = null
let animationFrame = null
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
  }

  recognition.onerror = () => stopRecognition()
  recognition.onend = () => stopRecognition()
})

onUnmounted(() => {
  stopRecognition()
})

watch(transcript, () => {
  if (textRef.value) {
    textRef.value.scrollLeft = textRef.value.scrollWidth
  }
})

function toggleRecognition() {
  if (!recognition) return
  if (!isRecognizing.value) {
    recognition.start()
    isRecognizing.value = true
    startWave()
  } else {
    stopRecognition()
  }
}

function stopRecognition() {
  recognition?.stop()
  isRecognizing.value = false
  stopWave()
}

function clearText() {
  transcript.value = ''
}

function submitText() {
  MessagePlugin.success(`提交内容：${transcript.value}`)
}

function startWave() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    audioContext = new AudioContext()
    analyser = audioContext.createAnalyser()
    microphone = audioContext.createMediaStreamSource(stream)
    microphone.connect(analyser)

    analyser.fftSize = 256
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
        ctx.fillStyle = `rgb(61, 214, 140)`
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
        x += barWidth + 1
      }
    }

    draw()
  })
}

function stopWave() {
  cancelAnimationFrame(animationFrame)
  audioContext?.close()
  audioContext = null
}
</script>

<style scoped>
.card {
  max-width: 640px;
  margin: 40px auto;
  padding: 16px;
}

.actions {
  margin-top: 16px;
}

.waveform {
  width: 100%;
  height: 50px;
  display: block;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #f6fef8;
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
  overflow-x: hidden;         /* 禁止滚动条 */
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

</style>

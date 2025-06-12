import { ref, computed, onUnmounted } from 'vue'
import { useInterviewStore } from '@/stores/interviewStore';

export function useInterviewTimer() {
  const totalSeconds = ref(0)
  let timer = null

  const interviewStore = useInterviewStore()

  // 开始从 00:00 计时
  const startTimer = () => {
    totalSeconds.value = 0
    clearInterval(timer)
    timer = setInterval(() => {
      totalSeconds.value++
    }, 1000)
  }

  // 停止计时并记录到 interviewStore（单位：秒）
  const stopTimer = () => {
    clearInterval(timer)
    interviewStore.spend_time = totalSeconds.value
  }

  // 可选：显示为 00:00 格式
  const formattedTime = computed(() => {
    const min = String(Math.floor(totalSeconds.value / 60)).padStart(2, '0')
    const sec = String(totalSeconds.value % 60).padStart(2, '0')
    return `${min}:${sec}`
  })

  onUnmounted(() => {
    clearInterval(timer)
  })

  return {
    startTimer,
    stopTimer,
    formattedTime,
    totalSeconds
  }
} 

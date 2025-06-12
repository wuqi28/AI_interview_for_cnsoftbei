<template>
  <transition name="fade">
    <div v-if="actualVisible" class="analyzing-overlay">
      <div class="overlay-content">
        <!-- 背景装饰 -->
        <div class="bg-decoration"></div>

        <!-- 机器人头部 -->
        <div class="robot-container">
          <!-- 思考气泡 -->
          <div class="thought-bubbles">
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
          </div>

          <!-- 机器人图标容器 -->
          <div class="robot-icon-container">
            <t-icon name="robot" class="robot-icon" />

            <!-- 眼睛闪烁效果 -->
            <div class="eye eye-left"></div>
            <div class="eye eye-right"></div>
          </div>

          <!-- 光环效果 -->
          <div class="robot-halo"></div>
        </div>

        <!-- 大脑图标 -->
        <div class="brain-container">
          <t-icon name="view-module" class="brain-icon" />
          <t-icon name="star" class="sparkle-icon" />
        </div>

        <!-- 加载文本和进度 -->
        <div class="loading-text-container">
          <p class="loading-text">
            智能体正在分析模拟面试多模态数据
            <span class="dots">{{ dots }}</span>
          </p>
          
          <!-- 进度百分比 -->
          <div class="progress-percentage">{{ progress }}%</div>
          
          <!-- 进度条 -->
          <div class="progress-container">
            <div 
              class="progress-bar" 
              :style="{ width: progress + '%' }"
              :class="{ 'progress-completing': isCompleting }"
            ></div>
          </div>
        </div>

        <!-- 浮动粒子效果 -->
        <div class="particles-container">
          <div
            v-for="(particle, index) in particles"
            :key="index"
            class="particle"
            :style="{
              left: particle.left,
              top: particle.top,
              animationDelay: particle.delay,
              animationDuration: particle.duration
            }"
          ></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

// 定义组件属性
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
})

// 响应式数据
const dots = ref('')
const progress = ref(0)
const actualVisible = ref(false)
const isCompleting = ref(false)

let dotsInterval = null
let progressInterval = null
let hideTimeout = null

// 浮动粒子数据
const particles = computed(() => {
  return Array.from({ length: 6 }, (_, i) => ({
    left: `${20 + i * 15}%`,
    top: `${30 + (i % 2) * 40}%`,
    delay: `${i * 0.3}s`,
    duration: `${2 + i * 0.5}s`
  }))
})

// 点点动画
const startDotsAnimation = () => {
  dotsInterval = setInterval(() => {
    dots.value = dots.value === '...' ? '' : dots.value + '.'
  }, 500)
}

const stopDotsAnimation = () => {
  if (dotsInterval) {
    clearInterval(dotsInterval)
    dotsInterval = null
  }
}

// 进度条动画
const startProgressAnimation = () => {
  progress.value = 0
  let currentProgress = 0
  
  progressInterval = setInterval(() => {
    if (currentProgress < 30) {
      // 前30%快速增长
      currentProgress += Math.random() * 3 + 1
    } else if (currentProgress < 60) {
      // 30%-60%中等速度
      currentProgress += Math.random() * 2 + 0.5
    } else if (currentProgress < 85) {
      // 60%-85%较慢
      currentProgress += Math.random() * 1 + 0.3
    } else if (currentProgress < 95) {
      // 85%-95%很慢
      currentProgress += Math.random() * 0.5 + 0.1
    } else {
      // 95%后基本不动，偶尔微调
      currentProgress += Math.random() * 0.1
      if (currentProgress > 95) {
        currentProgress = 95
      }
    }
    
    progress.value = Math.min(Math.floor(currentProgress), 95)
  }, 200)
}

const stopProgressAnimation = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
}

// 完成进度条动画
const completeProgress = () => {
  return new Promise((resolve) => {
    isCompleting.value = true
    
    // 快速跳到100%
    const completeInterval = setInterval(() => {
      if (progress.value < 100) {
        progress.value += 2
      } else {
        progress.value = 100
        clearInterval(completeInterval)
        
        // 在100%停留一小段时间
        setTimeout(() => {
          isCompleting.value = false
          resolve()
        }, 300)
      }
    }, 20)
  })
}

// 重置所有状态
const resetState = () => {
  progress.value = 0
  dots.value = ''
  isCompleting.value = false
}

// 清理所有定时器
const clearAllTimers = () => {
  stopDotsAnimation()
  stopProgressAnimation()
  if (hideTimeout) {
    clearTimeout(hideTimeout)
    hideTimeout = null
  }
}

// 监听 visible 属性变化
watch(() => props.visible, async (newVal, oldVal) => {
  if (newVal && !oldVal) {
    // 显示组件
    clearAllTimers()
    resetState()
    actualVisible.value = true
    
    await nextTick()
    startDotsAnimation()
    startProgressAnimation()
  } else if (!newVal && oldVal) {
    // 隐藏组件
    stopDotsAnimation()
    stopProgressAnimation()
    
    // 先完成进度条到100%
    await completeProgress()
    
    // 然后隐藏组件
    hideTimeout = setTimeout(() => {
      actualVisible.value = false
      resetState()
    }, 200)
  }
})

// 组件挂载时
onMounted(() => {
  if (props.visible) {
    actualVisible.value = true
    nextTick(() => {
      startDotsAnimation()
      startProgressAnimation()
    })
  }
})

// 组件卸载时清理
onUnmounted(() => {
  clearAllTimers()
})
</script>

<style scoped>
/* 主容器 */
.analyzing-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.4), rgba(30, 58, 138, 0.3), rgba(88, 28, 135, 0.4));
  backdrop-filter: blur(4px);
}

/* 内容容器 */
.overlay-content {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 32px;
  border-radius: 16px;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 机器人容器 */
.robot-container {
  position: relative;
  margin-bottom: 8px;
}

/* 思考气泡 */
.thought-bubbles {
  position: absolute;
  top: -32px;
  right: -16px;
  display: flex;
  gap: 4px;
}

.bubble {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: bounce 1s infinite;
}

.bubble-1 {
  background-color: #60a5fa;
  animation-delay: 0ms;
}

.bubble-2 {
  background-color: #c084fc;
  animation-delay: 150ms;
}

.bubble-3 {
  background-color: #f472b6;
  animation-delay: 300ms;
}

/* 机器人图标容器 */
.robot-icon-container {
  position: relative;
  padding: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.robot-icon {
  font-size: 48px;
  color: white;
  animation: pulse 2s infinite;
}

/* 眼睛闪烁效果 */
.eye {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: white;
  border-radius: 50%;
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.eye-left {
  top: 24px;
  left: 24px;
}

.eye-right {
  top: 24px;
  right: 24px;
  animation-delay: 1s;
}

/* 光环效果 */
.robot-halo {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(to right, #60a5fa, #8b5cf6);
  opacity: 0.2;
  animation: spin 3s linear infinite;
}

/* 大脑图标 */
.brain-container {
  position: relative;
  margin-top: -8px;
}

.brain-icon {
  font-size: 32px;
  color: #93c5fd;
  animation: pulse 2s infinite;
}

.sparkle-icon {
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 16px;
  color: #fcd34d;
  animation: spin 1s linear infinite;
}

/* 加载文本容器 */
.loading-text-container {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.dots {
  display: inline-block;
  width: 24px;
  text-align: left;
  color: rgba(255, 255, 255, 0.9);
}

/* 进度百分比 */
.progress-percentage {
  font-size: 24px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
  min-width: 60px;
}

/* 进度条容器 */
.progress-container {
  width: 280px;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(to right, #60a5fa, #8b5cf6);
  border-radius: 9999px;
  transition: width 0.3s ease-out;
  position: relative;
}

.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 20px;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3));
  animation: shimmer 1.5s ease-in-out infinite;
}

.progress-completing {
  transition: width 0.1s linear !important;
}

.progress-completing::after {
  animation: shimmer-fast 0.5s ease-in-out infinite;
}

/* 浮动粒子 */
.particles-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background-color: #93c5fd;
  border-radius: 50%;
  opacity: 0.6;
  animation: float ease-in-out infinite;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 动画关键帧 */
@keyframes bounce {
  0%, 100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: none;
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

@keyframes pulse {
  50% {
    opacity: .5;
  }
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px) rotate(0deg); 
  }
  50% { 
    transform: translateY(-10px) rotate(180deg); 
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-20px);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(20px);
    opacity: 0;
  }
}

@keyframes shimmer-fast {
  0% {
    transform: translateX(-20px);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(20px);
    opacity: 0;
  }
}
</style>
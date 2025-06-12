<template>
  <div class="thinking-container">
    <t-loading size="small" text="思考中" class="loading-icon" />
    <span class="thinking-text">请稍等，智能体正在思考</span>
    <span class="dot one">.</span>
    <span class="dot two">.</span>
    <span class="dot three">.</span>
  </div>
</template>

<script setup>
// 无需额外逻辑，仅用于展示动画
</script>

<style scoped>
.thinking-container {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #0052d9; /* TDesign 主色 */
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #f0faff;
}

.thinking-text {
  margin-left: 8px;
  margin-right: 4px;
}

.dot {
  font-weight: bold;
  font-size: 20px;
  opacity: 0;
  animation: blink 1.5s infinite;
}

.dot.one {
  animation-delay: 0s;
}
.dot.two {
  animation-delay: 0.3s;
}
.dot.three {
  animation-delay: 0.6s;
}

@keyframes blink {
  0%, 20% { opacity: 0; }
  30%, 80% { opacity: 1; }
  100% { opacity: 0; }
}
</style>

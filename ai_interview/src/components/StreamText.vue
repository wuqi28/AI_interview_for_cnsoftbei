<template>
  <div class="stream-text">{{ displayedText }}</div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
  speed: { type: Number, default: 150 },
  autoStart: { type: Boolean, default: true }
})

const displayedText = ref('')
let index = 0
let timer = null
let resolveFn = null

const stream = () => {
  if (index < props.text.length) {
    displayedText.value += props.text[index++]
    timer = setTimeout(stream, props.speed)
  } else {
    resolveFn?.() // ✅ 播放完成，触发 then()
  }
}

const start = () => {
  displayedText.value = ''
  index = 0

  return new Promise((resolve) => {
    resolveFn = resolve
    stream()
  })
}

const clear = () => {
  displayedText.value = ''
  index = 0
  clearTimeout(timer)
}


defineExpose({ start, clear })

if (props.autoStart) {
  start()
}
</script>

<style scoped>
.stream-text {
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 16px;
  font-family: inherit;
}
</style>

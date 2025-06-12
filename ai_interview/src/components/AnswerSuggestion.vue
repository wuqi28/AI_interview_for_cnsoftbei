<template>
  <div class="answer-text" v-html="styledText" />
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  rawText: {
    type: String,
    required: true
  }
})

const styledText = ref('')

// 将 <color>标签转换为带样式的 span
const transformColorTags = (text) => {
  return text.replace(
    /<color>(.*?)<\/color>/g,
    '<span style="color: rgb(0, 82, 217); font-weight: 500;">$1</span>'
  )
}

// 监听 rawText 变化
watch(
  () => props.rawText,
  (newVal) => {
    styledText.value = transformColorTags(newVal)
  },
  { immediate: true }
)
</script>

<style scoped>
.answer-text {
  font-size: 16px;
  line-height: 24px;
  color: #1a1a1a;
  padding: 12px 0;
}
</style>

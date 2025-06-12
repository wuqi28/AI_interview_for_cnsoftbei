<template>
  <div class="p-4">
    <test-component ref="textRef" :text="testText" :auto-start="false" />

    <t-button class="mt-4" type="primary" @click="runTest">
      开始流式播放
    </t-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TestComponent from '@/components/testComponent.vue'

const textRef = ref(null)
const testText = ref('你好，这是一个逐字显示的测试文本。你好，这是一个逐字显示的测试文本。你好，这是一个逐字显示的测试文本。你好，这是一个逐字显示的测试文本。你好，这是一个逐字显示的测试文本。你好，这是一个逐字显示的测试文本。')

const runTest = async () => {
  console.log('开始播放...')
  await textRef.value?.start()
  console.log('✅ 播放完毕，执行后续逻辑')
  alert('流式播放完毕！')
}
</script>

<style scoped>
.p-4 {
  padding: 1rem;
}
.mt-4 {
  margin-top: 1rem;
}
</style>

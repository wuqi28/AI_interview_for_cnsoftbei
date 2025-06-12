<template>
    <!-- 使用组件 -->
    <AnalyzingOverlay :visible="showAnalyzing" />
</template>

<script setup>
import { ref } from 'vue'

const showAnalyzing = ref(false)

setTimeout(() => {
    showAnalyzing.value = false
}, 30000)
</script>

<style scoped>

</style>
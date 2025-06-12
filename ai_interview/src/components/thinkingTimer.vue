<template>
  <t-card v-if="visible" class="max-w-sm mx-auto p-4 rounded-2xl shadow-md">
    <div class="text-center text-xl font-bold">请思考...</div>
    <div class="text-center text-base text-gray-500 mt-2">倒计时：{{ countdown }} 秒</div>
    <t-progress
      :percentage="progress"
      theme="circle"
      size="large"
      :label="false"
      class="mt-4 mx-auto"
    />
    <!-- <t-loading size="small" text="思考中..." :indicator="true" class="mt-4" /> -->
  </t-card>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useEventBus } from '@vueuse/core'

const props = defineProps({
  duration: {
    type: Number,
    default: 30, // 默认30秒
  },
  autoStart: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['finished'])

const visible = ref(false)
const countdown = ref(props.duration)
let timer = null

const progress = computed(() => {
  return ((props.duration - countdown.value) / props.duration) * 100
})

function start() {
  visible.value = true
  countdown.value = props.duration

  timer && clearInterval(timer)
  timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(timer)
      visible.value = false
      emit('finished')
    }
  }, 1000)
}

function stop() {
  clearInterval(timer)
  visible.value = false
}

onUnmounted(() => {
  clearInterval(timer)
})

// 外部可以通过 ref 控制 start()
defineExpose({ start, stop })

if (props.autoStart) {
  start()
}
</script>

<style scoped>
.t-card {
  transition: all 0.3s ease;
}
</style>

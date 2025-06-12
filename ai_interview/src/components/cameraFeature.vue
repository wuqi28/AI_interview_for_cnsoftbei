<template>
  <div class="camera-wrapper">
    <video ref="video" autoplay muted playsinline class="camera-video" />
    <canvas ref="canvas" class="camera-canvas" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import human from '@/modules/human'

const video = ref(null)
const canvas = ref(null)

onMounted(async () => {
  await human.load()

  const stream = await navigator.mediaDevices.getUserMedia({ video: true })
  video.value.srcObject = stream

  video.value.onloadedmetadata = () => {
    video.value.play()

    // ✅ 设置 canvas 的真实像素大小（不是 CSS 尺寸）
    canvas.value.width = video.value.videoWidth
    canvas.value.height = video.value.videoHeight

    runDetection()
  }
})

const runDetection = async () => {
  const ctx = canvas.value.getContext('2d')

  const detectLoop = async () => {
    const result = await human.detect(video.value)

    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

    // ✅ 绘制人脸（确保 canvas 尺寸正确）
    await human.draw.face(canvas.value, result.face, {
      drawGaze: true,
      drawPoints: false,
      drawPolygons: true,
      drawBoxes: false,
      drawLabels: false
    })

    if (result.face.length > 0) {
      const face = result.face[0]
    //   console.log('表情:', face.emotion)

      const rotation = face.rotation
      const bearingDegrees = rotation.gaze.bearing * (180 / Math.PI)
    //   console.log('视线角度:', bearingDegrees)
    //   console.log('视线长度:', rotation.gaze.strength)
    }

    requestAnimationFrame(detectLoop)
  }

  detectLoop()
}
</script>

<style scoped>
.camera-wrapper {
  position: relative;
  width: 100%;
  max-width: 480px;
  aspect-ratio: 4 / 3;
  margin: 0 auto;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.camera-video,
.camera-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-canvas {
  z-index: 2;
  pointer-events: none;
}
</style>

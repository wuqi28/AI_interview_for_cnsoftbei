<script setup>
import { ref, onMounted } from 'vue'
import AvatarPlatform, {
  PlayerEvents,
  SDKEvents,
} from '../avatar-sdk-web_3.1.2.1002/index.js'

const avatarPlatform = new AvatarPlatform()
let player = null

// 用户点击后触发 resume 恢复播放
const clickPlayer = () => {
  if (player) {
    player.resume()
    console.log('✅ user clicked, resume playback')
  }
}

onMounted(() => {
  avatarPlatform
    .on(SDKEvents.connected, (initResp) => {
      console.log('sdk event: connected', initResp)
    })
    .on(SDKEvents.playNotAllowed, () => {
      console.log('⚠️ sdk event: play not allowed')
    })
    .on(SDKEvents.asr, (asrData) => {
     console.log('识别内容:', asrData)
  })
  .on(SDKEvents.nlp, (nlpData) => {
    console.log('语义理解:', nlpData)
  })
  .on(SDKEvents.tts_duration, (ttsInfo) => {
    console.log('语音合成时长:', ttsInfo)
  })

  player = avatarPlatform.player || avatarPlatform.createPlayer()

  player
    .on(PlayerEvents.play, () => {
      console.log('sdk event: player play')
    })
    .on(PlayerEvents.playNotAllowed, () => {
      console.log('⚠️ player play not allowed — wait for user interaction!')
    })

  avatarPlatform.setApiInfo({
    appId: 'a120861d',
    apiKey: '2f6b3094dc2174bb8f4fffde5350703b',
    apiSecret: 'YWMzNDMxYWMwYzc4YWVlYzkzOTMzYTFi',
    sceneId: '180580224336007168',
    serverUrl: 'wss://avatar.cn-huadong-1.xf-yun.com/v1/interact'
  })

  avatarPlatform.setGlobalParams({
    stream: {
      protocol: 'xrtc',
      alpha: 1,
    },
    avatar: {
      avatar_id: '110017006',
    },
    tts: {
      vcn: 'x4_xiaozhong',
    },
    driver: {
    enable_rec: true,     // 开启语音驱动
    enable_nlp: true      // 开启语义理解（如大模型问答）
  }
   
  })

  avatarPlatform
    .start({
      wrapper: document.querySelector('.wrapper')
    })
    .then(() => {
      console.log('✅ connected & stream ready (waiting for resume...)')
    })
    
    setTimeout(() => {
  avatarPlatform
  .writeText("你好，我是小度，很高兴为你服务。",{append: true})
  .then(() => {
    console.log('✅ writeText success')
  })
  .catch((err) => {
    console.error('❌ writeText failed', err)
  })
}, 3000)
})

const recorder = avatarPlatform.recorder || avatarPlatform.createRecorder()

// 必须在用户交互后调用，比如点击按钮
function startRecord() {
  recorder.startRecord(60 * 1000).then(() => {
    console.log('开始录音')
  })
}

function stopRecord() {
  recorder.stopRecord() // 停止录音并触发语音交互流程
  console.log('停止录音')
}



</script>

<template>

  <div id="video-container" style=" width: 320px;height: 270px; /* 显示一半高度 */
    overflow: hidden;
    /* background: #000; */
    position: relative;
  "> 
  <!-- 容器需要设置尺寸，否则视频不会显示 -->
   <div class="wrapper" 
  style="width: 640px; height: 480px; 
  /* background: #000;  */
  transform: translateX(-160px); /* 左移裁掉左右各160px，使中间部分正好居中显示 */
  position: absolute; 
  top: 0;
  left: 0;"></div>
</div>

  <!-- 用户交互按钮 -->
  <button @click="clickPlayer" style="margin-top: 16px">
    ▶️ 点击恢复播放声音
  </button>


<button @click="startRecord">🎙️ 开始说话</button>
<button @click="stopRecord">🛑 停止并回答</button>

</template>

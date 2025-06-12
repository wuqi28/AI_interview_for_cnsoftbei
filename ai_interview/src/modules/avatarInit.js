import AvatarPlatform, { PlayerEvents, SDKEvents } from '../avatar-sdk-web_3.1.2.1002/index.js'

let avatarPlatform = null
let player = null

// ✅ 初始化虚拟人
export function initAvatar(
  avatar_id = '110017006',
  vcn = 'x4_xiaozhong'
) {
  if (avatarPlatform) {
    console.warn('⚠️ 虚拟人已初始化')
    return
  }
  avatarPlatform = new AvatarPlatform()
  avatarPlatform
    .on(SDKEvents.connected, (initResp) => {
      console.log('✅ SDK connected', initResp)
    })
    .on(SDKEvents.playNotAllowed, () => {
      console.warn('⚠️ 播放未授权，需要用户点击')
    })

  player = avatarPlatform.createPlayer()
  player
    .on(PlayerEvents.play, () => {
      console.log('▶️ 播放开始')
    })
    .on(PlayerEvents.playNotAllowed, () => {
      console.warn('⚠️ 播放未授权，需要用户点击')
    })


  avatarPlatform.setApiInfo({
    appId: 'f6184f6e',
    apiKey: '1675cbfee491eeb7756db5186d203e44',
    apiSecret: 'ODFjZGRhNjM0MmI3NWRkYWQ3OWJlYzE3',
    sceneId: '186736211287740416',
    serverUrl: 'wss://avatar.cn-huadong-1.xf-yun.com/v1/interact',
  })

  avatarPlatform.setGlobalParams({
    stream: {
      protocol: 'xrtc',
      alpha: 1,
    },
    avatar: {
      avatar_id: avatar_id,
    },
    tts: {
      vcn: vcn,
    },
    driver: {
      enable_rec: true,
      enable_nlp: true,
    },
  })

  avatarPlatform
    .start({
      wrapper: document.querySelector('.wrapper'),
    })
    .then(() => {
      console.log('✅ 虚拟人启动完成')
    })
    .catch((err) => {
      console.error('❌ 启动失败', err)
    })
}

// ✅ 发送文本，让虚拟人说话
export function speak(text) {
  if (!avatarPlatform) {
    console.warn('⚠️ 请先初始化虚拟人 initAvatar()')
    return
  }
// setTimeout(() => {
  avatarPlatform
    .writeText(text, { append: true })
    .then(() => {
      console.log('✅ 虚拟人说话成功')
    })
    .catch((err) => {
      console.error('❌ 说话失败', err)
    }) 
// }, 3000)

}

// ✅ 停止虚拟人
export function close() {
  if (!avatarPlatform) {
    console.warn('⚠️ 虚拟人尚未启动')
    return
  }
  avatarPlatform.stop()
  avatarPlatform = null
  player = null
  console.log('🛑 虚拟人已关闭')
}


import { defineStore } from 'pinia'

export const useAvatarStore = defineStore('avatar', {
  state: () => ({
    isAvatarInitialized: false, // 虚拟人是否已初始化
    isAvatarStarted: false, // 虚拟人是否已启动
  }),

})
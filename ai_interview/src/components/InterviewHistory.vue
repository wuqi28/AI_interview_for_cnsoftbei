<template>
    <div class="history-wrapper">
        <div class="card-grid">
            <el-scrollbar height="510px" ref="scrollRef">
                <t-card v-for="(item, index) in messages" :key="index" @click="showDialog(item.content, item.role)"
                    class="dialog-card">
                    <template #title>
                        <div class="card-title">
                            <div class="card-header-left">
                                <t-avatar :image="item.role === 'assistant' ? assistantAvatar : userAvatar"
                                    shape="circle" size="medium" />
                                <span class="sender-name">{{ item.role === 'assistant' ? '面试官' : '面试者' }}</span>
                            </div>
                            <span class="duration-tag">{{ mockDurations[index] || '00:00' }}</span>
                        </div>
                    </template>


                    <div class="message-preview">
                        {{ truncate(item.content, 60) }}
                    </div>
                </t-card>
            </el-scrollbar>
        </div>

        <t-dialog v-model:visible="visible" header="对话内容" :footer="false" width="500px">
            <p class="dialog-text">{{ selectedContent }}</p>
        </t-dialog>
    </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
    messages: {
        type: Array,
        required: true
    },
    mockDurations: {
        type: Array,
        required: true
    }
})

const visible = ref(false)
const selectedContent = ref('')

const assistantAvatar = '../../public/img/robot.png'
const userAvatar = '../../public/img/people3.png'

const scrollRef = ref(null)

// 当 messages 更新时滚动到底
watch(() => props.messages, async () => {
  await nextTick()
  const scrollEl = scrollRef.value
  if (scrollEl?.wrapRef) {
    scrollEl.wrapRef.scrollTop = scrollEl.wrapRef.scrollHeight
  }
}, { deep: true })

// 模拟的每条对话持续时长
// const mockDurations = [
//     '00:23', '01:05', '00:42', '00:58', '01:12', '00:36'
// ]

function truncate(text, maxLength) {
    return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
}

function showDialog(content, role) {
    selectedContent.value = `${role === 'assistant' ? '面试官' : '你'}：\n\n` + content
    visible.value = true
}
</script>

<style scoped>
.history-wrapper {
    max-height: 100%;
    overflow-y: auto;
    padding: 12px;
    background-color: #f7f9fb;
    border-radius: 8px;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
}

.dialog-card {
    margin-bottom: 10px;
    cursor: pointer;
    transition: box-shadow 0.2s ease;
    border-radius: 8px;
    position: relative;
}

.dialog-card:hover {
    box-shadow: 0 0 0 2px #0052d9 inset;
}

.card-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.card-header-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-header-right {
    margin-left: auto;
    display: flex;
    align-items: center;
}

.sender-name {
    font-weight: 600;
    color: #1a1a1a;
}

.duration-tag {
    margin-left: 110px;
    font-size: 12px;
    color: #999;
    font-weight: 500;
}

.message-preview {
    margin-top: -20px;
    color: #444;
    font-size: 14px;
    line-height: 1.6;
    min-height: 48px;
}

.dialog-text {
    white-space: pre-line;
    font-size: 15px;
    line-height: 1.6;
    color: #333;
}
</style>
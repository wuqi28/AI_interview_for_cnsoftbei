<template>
  <div class="interview-config-container">
    <t-row :gutter="24">
      <!-- 题库区域 -->
      <t-col :span="9">
        <t-card class="question-bank-card">
          <template #header>
            <div class="bank-header">
              <t-icon name="layers" size="18px" />
              <span class="bank-title">问题类型库</span>
              <!-- <t-badge :count="questionBank.length" /> -->
            </div>
          </template>
          
          <div class="bank-content">
            <div class="bank-description">
              拖拽下方问题类型到右侧配置区域
            </div>
            <div class="bank-items" ref="bankRef">
              <div
                v-for="(type, index) in questionBank"
                :key="`bank-${index}`"
                class="bank-item-wrapper"
                :class="{ 'dragging': draggedSource === 'bank' && draggedBankIndex === index }"
                :data-type="type"
                :data-index="index"
                draggable="true"
                @dragstart="onBankDragStart($event, index)"
                @dragend="onDragEnd"
              >
                <div class="bank-item">
                  <t-icon name="drag" class="drag-icon" />
                  <span class="item-text">{{ type }}</span>
                  <t-icon name="add-circle" class="add-icon" />
                </div>
              </div>
            </div>
          </div>
        </t-card>
      </t-col>

      <!-- 当前配置区域 -->
      <t-col :span="3">
        <t-card class="current-config-card">
          <template #header>
            <div class="config-header">
              <div class="config-title-section">
                <t-icon name="setting" size="18px" />
                <span class="config-title">当前问题配置</span>
                <!-- <t-badge :count="currentConfig.length" theme="success" /> -->
              </div>
              <t-button theme="danger" variant="text" size="small" @click="clearAll">
                <t-icon name="delete" />
                清空全部
              </t-button>
            </div>
          </template>
          
          <div class="config-content">
            <div 
              class="config-drop-zone" 
              ref="configRef"
              :class="{ 'drag-over': isDragOverZone }"
              @dragover.prevent="onConfigDragOver"
              @drop="onConfigDrop"
              @dragenter.prevent="onConfigDragEnter"
              @dragleave.prevent="onConfigDragLeave"
            >
              <div v-if="currentConfig.length === 0" class="empty-state">
                <t-icon name="inbox" size="64px" />
                <h3>暂无配置</h3>
                <p>从左侧题库拖拽问题类型到此处开始配置</p>
              </div>

              <div v-else class="config-items-container">
                <div class="config-items">
                  <transition-group name="config-list" tag="div">
                    <div
                      v-for="(type, index) in currentConfig"
                      :key="`config-${type}-${index}`"
                      class="config-item"
                      :class="{ 
                        'dragging': draggedSource === 'config' && draggedConfigIndex === index,
                        'drag-over': dragOverIndex === index && draggedConfigIndex !== index
                      }"
                      :data-index="index"
                      draggable="true"
                      @dragstart="onConfigDragStart($event, index)"
                      @dragover.prevent="onItemDragOver($event, index)"
                      @dragenter.prevent="onItemDragEnter($event, index)"
                      @dragleave.prevent="onItemDragLeave($event, index)"
                      @drop="onItemDrop($event, index)"
                      @dragend="onDragEnd"
                    >
                      <div class="config-item-content">
                        <div class="item-left">
                          <div class="item-number">{{ index + 1 }}</div>
                          <t-icon name="drag" class="drag-handle" />
                        </div>
                        <div class="item-center">
                          <span class="config-item-text" :title="type">{{ type }}</span>
                        </div>
                        <div class="item-right">
                          <t-button 
                            theme="danger" 
                            variant="text" 
                            size="small"
                            @click="removeItem(index)"
                            class="remove-btn"
                          >
                            <t-icon name="close" />
                          </t-button>
                        </div>
                      </div>
                      <div 
                        v-if="dragOverIndex === index && draggedConfigIndex !== index" 
                        class="drag-indicator"
                      ></div>
                    </div>
                  </transition-group>
                </div>
              </div>
            </div>
          </div>
        </t-card>
      </t-col>
    </t-row>

    <!-- 操作按钮 -->
    <div class="actions">
      <t-space size="large">
        <t-button theme="primary" size="large" @click="saveConfig">
          <t-icon name="check" />
          保存配置
        </t-button>
        <t-button theme="default" size="large" @click="resetConfig">
          <t-icon name="refresh" />
          重置配置
        </t-button>
      </t-space>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { MessagePlugin } from 'tdesign-vue-next';
import { useInterviewStore } from '@/stores/interviewStore';

const interviewStore = useInterviewStore();

// 题库数据
const questionBank = [
  "专业技能测试",
  "简历深挖与项目分析", 
  "情景模拟", 
  "综合问答",
  "算法能力", 
  "编码实现", 
  "系统设计",
  "工具实操", 
  "故障处理", 
  "架构流程",
  "需求分析", 
  "用户洞察", 
  "方案设计"
];

// 当前配置
const currentConfig = ref([...interviewStore.question_config.question_type]);

// 拖拽相关状态
const draggedSource = ref(null); // 'bank' 或 'config'
const draggedBankIndex = ref(null);
const draggedConfigIndex = ref(null);
const dragOverIndex = ref(null);
const isDragOverZone = ref(false);

const bankRef = ref(null);
const configRef = ref(null);

// 从题库拖拽开始
const onBankDragStart = (event, index) => {
  draggedSource.value = 'bank';
  draggedBankIndex.value = index;
  event.dataTransfer.effectAllowed = 'copy';
  event.dataTransfer.setData('text/plain', questionBank[index]);
};

// 从配置区拖拽开始
const onConfigDragStart = (event, index) => {
  draggedSource.value = 'config';
  draggedConfigIndex.value = index;
  event.dataTransfer.effectAllowed = 'move';
  event.dataTransfer.setData('text/plain', currentConfig.value[index]);
};

// 配置区域拖拽悬停
const onConfigDragOver = (event) => {
  event.dataTransfer.dropEffect = draggedSource.value === 'bank' ? 'copy' : 'move';
};

// 配置区域拖拽进入
const onConfigDragEnter = (event) => {
  isDragOverZone.value = true;
};

// 配置区域拖拽离开
const onConfigDragLeave = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  const x = event.clientX;
  const y = event.clientY;
  if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
    isDragOverZone.value = false;
  }
};

// 配置区域拖拽放置
const onConfigDrop = (event) => {
  event.preventDefault();
  isDragOverZone.value = false;
  
  if (draggedSource.value === 'bank') {
    const draggedItem = questionBank[draggedBankIndex.value];
    currentConfig.value.push(draggedItem);
    MessagePlugin.success(`已添加"${draggedItem}"`);
  }
  
  resetDragState();
};

// 配置项拖拽悬停
const onItemDragOver = (event, index) => {
  if (draggedSource.value === 'config' && draggedConfigIndex.value !== index) {
    event.dataTransfer.dropEffect = 'move';
  }
};

// 配置项拖拽进入
const onItemDragEnter = (event, index) => {
  if (draggedSource.value === 'config' && draggedConfigIndex.value !== index) {
    dragOverIndex.value = index;
  }
};

// 配置项拖拽离开
const onItemDragLeave = (event, index) => {
  const rect = event.currentTarget.getBoundingClientRect();
  const x = event.clientX;
  const y = event.clientY;
  if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
    if (dragOverIndex.value === index) {
      dragOverIndex.value = null;
    }
  }
};

// 配置项拖拽放置
const onItemDrop = (event, dropIndex) => {
  event.preventDefault();
  
  if (draggedSource.value === 'bank') {
    const draggedItem = questionBank[draggedBankIndex.value];
    currentConfig.value.splice(dropIndex, 0, draggedItem);
    MessagePlugin.success(`已添加"${draggedItem}"到位置 ${dropIndex + 1}`);
  } else if (draggedSource.value === 'config') {
    if (draggedConfigIndex.value !== dropIndex) {
      const draggedItem = currentConfig.value[draggedConfigIndex.value];
      currentConfig.value.splice(draggedConfigIndex.value, 1);
      currentConfig.value.splice(dropIndex, 0, draggedItem);
      MessagePlugin.success(`已移动"${draggedItem}"到位置 ${dropIndex + 1}`);
    }
  }
  
  resetDragState();
};

// 拖拽结束
const onDragEnd = () => {
  resetDragState();
};

// 重置拖拽状态
const resetDragState = () => {
  draggedSource.value = null;
  draggedBankIndex.value = null;
  draggedConfigIndex.value = null;
  dragOverIndex.value = null;
  isDragOverZone.value = false;
};

// 移除配置项
const removeItem = (index) => {
  const removedItem = currentConfig.value[index];
  currentConfig.value.splice(index, 1);
  MessagePlugin.success(`已移除"${removedItem}"`);
};

// 清空全部
const clearAll = () => {
  currentConfig.value = [];
  MessagePlugin.success('已清空全部配置');
};

// 保存配置
const saveConfig = () => {
  interviewStore.question_config.question_type = [...currentConfig.value];
  MessagePlugin.success('配置已保存');
  console.log('当前配置已保存：', interviewStore.question_config.question_type);
};

// 重置配置
const resetConfig = () => {
  currentConfig.value = [...interviewStore.question_config.question_type];
  MessagePlugin.info('配置已重置');
};
</script>

<style scoped>
.interview-config-container {
  /* padding: 24px; */
  /* background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); */
  min-height: 70vh;
}

/* 题库卡片样式 */
.question-bank-card {
  height: 60vh;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  border: none;
  overflow: hidden;
}

.bank-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1f2937;
}

.bank-title {
  font-size: 16px;
}

.bank-content {
  height: 580px;
  display: flex;
  flex-direction: column;
}

.bank-description {
  background: linear-gradient(135deg, #667eea 0%, #99a7e9 100%);
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.bank-items {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.bank-items::-webkit-scrollbar {
  width: 6px;
}

.bank-items::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.bank-items::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.bank-items::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.bank-item-wrapper {
  margin-bottom: 12px;
  cursor: grab;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.bank-item-wrapper:hover {
  /* transform: translateX(8px) scale(1.02); */
}

.bank-item-wrapper:active {
  cursor: grabbing;
}

.bank-item-wrapper.dragging {
  opacity: 0.7;
  transform: rotate(3deg) scale(1.02);
  z-index: 1000;
}

.bank-item {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.bank-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.bank-item-wrapper:hover .bank-item::before {
  transform: scaleX(1);
}

.bank-item-wrapper:hover .bank-item {
  border-color: #3b82f6;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
}

.drag-icon {
  color: #94a3b8;
  transition: color 0.2s ease;
}

.bank-item-wrapper:hover .drag-icon {
  color: #3b82f6;
}

.item-text {
  flex: 1;
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.add-icon {
  color: #10b981;
  transition: all 0.2s ease;
}

.bank-item-wrapper:hover .add-icon {
  color: #059669;
  transform: scale(1.1);
}

/* 配置卡片样式 */
.current-config-card {
  height: 60vh;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  border: none;
  overflow: hidden;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.config-title-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.config-content {
  height: 45vh;
}

.config-drop-zone {
  height: 100%;
  border: 3px dashed #d1d5db;
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  background: #fafbfc;
}

.config-drop-zone.drag-over {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  box-shadow: inset 0 0 20px rgba(59, 130, 246, 0.1);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  text-align: center;
}

.empty-state h3 {
  margin: 16px 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #374151;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
  opacity: 0.8;
}

.config-items-container {
  height: 100%;
  overflow: hidden;
}

.config-items {
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.config-items::-webkit-scrollbar {
  width: 8px;
}

.config-items::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.config-items::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.config-items::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
}

.config-item {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 12px;
  cursor: grab;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  height: 60px; /* 固定高度 */
  flex-shrink: 0;
}

.config-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.config-item:hover::before {
  transform: scaleX(1);
}

.config-item:hover {
  border-color: #10b981;
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(16, 185, 129, 0.15);
}

.config-item:active {
  cursor: grabbing;
}

.config-item.dragging {
  opacity: 0.6;
  transform: rotate(3deg) scale(0.98);
  z-index: 1000;
}

.config-item.drag-over {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  border-color: #3b82f6;
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
}

.config-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0px 20px 16px 20px;
  width: 100%;
  height: 100%;
}

.item-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.item-center {
  flex: 1;
  min-width: 0;
  margin: 0 12px;
}

.item-right {
  flex-shrink: 0;
}

.item-number {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.drag-handle {
  color: #9ca3af;
  transition: color 0.2s ease;
  cursor: grab;
}

.config-item:hover .drag-handle {
  color: #10b981;
}

.config-item-text {
  font-weight: 500;
  color: #374151;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.remove-btn {
  opacity: 0;
  transition: all 0.2s ease;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.config-item:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

.drag-indicator {
  position: absolute;
  top: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #3b82f6;
  border-radius: 1px;
  animation: dragIndicator 0.3s ease-in-out;
}

@keyframes dragIndicator {
  0% {
    transform: scaleX(0);
  }
  100% {
    transform: scaleX(1);
  }
}

/* 操作按钮区域 */
.actions {
  margin-top: 32px;
  display: flex;
  justify-content: center;
  padding: 24px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* 配置列表动画 */
.config-list-move,
.config-list-enter-active,
.config-list-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.config-list-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

.config-list-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.config-list-leave-active {
  position: absolute;
  width: calc(100% - 40px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .interview-config-container {
    padding: 16px;
  }
  
  .question-bank-card,
  .current-config-card {
    height: 500px;
  }
  
  .bank-content,
  .config-content {
    height: 420px;
  }
}

@media (max-width: 768px) {
  .interview-config-container {
    padding: 12px;
  }
  
  .question-bank-card,
  .current-config-card {
    height: 400px;
    margin-bottom: 16px;
  }
  
  .bank-content,
  .config-content {
    height: 320px;
  }
  
  .config-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .config-item {
    height: 50px;
  }
  
  .config-item-content {
    padding: 12px 16px;
  }
  
  .actions {
    margin-top: 16px;
    padding: 16px;
  }
}
</style>

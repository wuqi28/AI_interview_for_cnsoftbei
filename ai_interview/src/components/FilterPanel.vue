<template>
  <t-card class="filter-panel" hover-shadow>
    <div class="description">
      <t-alert theme="info" message="智能体支持两种个性化习题推荐模式：" style="background-color: transparent; border: none;" />

      <ul style="margin-top: 12px; line-height: 1.6; font-size: 14px; color: #555;">
        <li>
          <strong>自主设定模式：</strong>
          用户可自主选择岗位、难度、知识点和题目数量，智能体将根据设定生成个性化面试题，适合日常练习与自主复盘。
        </li>
        <li>
          <strong>面试驱动模式：</strong>
          用户选择一次历史面试记录，智能体将基于多模态评测报告智能分析表现，从能力短板中推送更具针对性的题目，助力快速提升。
        </li>
      </ul>
    </div>

    <template #header>
      <div class="filter-header">
        <span class="filter-title">题目生成设置</span>
        <t-space>
          <t-button theme="default" size="small" @click="resetFilters" :disabled="isLoading">
            重置
          </t-button>
          <t-button theme="primary" size="small" @click="generateQuestions" :loading="isLoading">
            生成题目
          </t-button>
        </t-space>
      </div>
    </template>

    <div class="filter-content">
      <!-- 模式选择 -->
      <div class="mode-selection">
        <label class="filter-label">选择模式</label>
        <t-radio-group v-model="localFilters.mode" @change="handleModeChange" :disabled="isLoading"
          style="padding-left: 20px;">
          <t-radio value="self-directed">自主设定模式</t-radio>
          <t-radio value="interview-driven">面试驱动模式</t-radio>
        </t-radio-group>
      </div>

      <t-divider />

      <!-- 面试驱动模式 - 选择历史面试记录 -->
      <div v-if="localFilters.mode === 'interview-driven'" class="interview-selection">
        <div class="filter-item">
          <label class="filter-label">选择历史面试记录</label>
          <t-select v-model="localFilters.selectedInterviewId" placeholder="请选择一次面试记录" :disabled="isLoading"
            @change="handleInterviewRecordChange" style="width: 100%;">
            <t-option v-for="record in interviewRecords" :key="record.id" :value="record.current_interview_id"
              :label="formatInterviewLabel(record)">
              <div class="interview-option">
                <div class="interview-main">
                  <span class="company">{{ parseInterviewId(record.current_interview_id).company }}</span>
                  <span class="position">{{ parseInterviewId(record.current_interview_id).position }}</span>
                  <span class="time">{{ formatTime(record.start_time) }}</span>
                  <span class="duration">{{ parseFloat((record.spend_time / 60).toFixed(1))
                  }}分钟</span>
                  <span class="interviewer">面试官: {{ record.interviewer_name }}</span>
                </div>
              </div>
            </t-option>
          </t-select>
        </div>

        <div v-if="localFilters.knowledgePoints.length > 0" class="selected-knowledge-points">
          <t-divider>已选择的知识点</t-divider>
          <t-space size="small" class="knowledge-tags">
            <t-tag v-for="point in localFilters.knowledgePoints" :key="point" theme="primary" variant="light" closable
              :disabled="isLoading" @close="removeKnowledgePoint(point)">
              {{ point }}
            </t-tag>
          </t-space>
        </div>

        <!-- 显示选中的面试记录详情 -->
        <div v-if="selectedInterviewRecord" class="selected-interview-info">
          <t-divider>选中的面试记录</t-divider>
          <div class="interview-detail-card">
            <div class="detail-row">
              <span class="detail-label">公司:</span>
              <span class="detail-value">{{ parseInterviewId(selectedInterviewRecord.current_interview_id).company
              }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">岗位:</span>
              <span class="detail-value">{{ parseInterviewId(selectedInterviewRecord.current_interview_id).position
              }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">面试时间:</span>
              <span class="detail-value">{{ formatTime(selectedInterviewRecord.start_time) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">面试时长:</span>
              <span class="detail-value">{{ parseFloat((selectedInterviewRecord.spend_time / 60).toFixed(1)) }}分钟</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">面试官:</span>
              <span class="detail-value">{{ selectedInterviewRecord.interviewer_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">面试风格:</span>
              <span class="detail-value">{{ selectedInterviewRecord.interview_style }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 自主设定模式 - 原有的筛选条件 -->
      <div v-if="localFilters.mode === 'self-directed'">
        <t-row :gutter="[16, 16]">
          <!-- 题目数量 -->
          <t-col :xs="12" :sm="6" :md="3">
            <div class="filter-item">
              <label class="filter-label">题目数量</label>
              <t-select v-model="localFilters.questionCount" placeholder="选择数量" :disabled="isLoading"
                @change="emitUpdate">
                <t-option :value="5" label="5题" />
                <t-option :value="10" label="10题" />
                <t-option :value="15" label="15题" />
                <t-option :value="20" label="20题" />
                <t-option :value="30" label="30题" />
                <t-option :value="50" label="50题" />
              </t-select>
            </div>
          </t-col>

          <!-- 难度 -->
          <t-col :xs="12" :sm="6" :md="3">
            <div class="filter-item">
              <label class="filter-label">题目难度</label>
              <t-select v-model="localFilters.difficulty" placeholder="选择难度" clearable :disabled="isLoading"
                @change="emitUpdate">
                <t-option value="初级" label="初级" />
                <t-option value="中级" label="中级" />
                <t-option value="高级" label="高级" />
                <t-option value="随机" label="随机" />
              </t-select>
            </div>
          </t-col>

          <!-- 选择岗位 -->
          <t-col :xs="12" :sm="6" :md="3">
            <div class="filter-item">
              <label class="filter-label">岗位</label>
              <t-select v-model="localFilters.position" placeholder="选择岗位" clearable :disabled="isLoading"
                @change="handlePositionChange">
                <t-option value="前端工程师" label="前端工程师" />
                <t-option value="后端工程师" label="后端工程师" />
                <t-option value="人工智能-算法工程师" label="人工智能 - 算法工程师" />
                <t-option value="人工智能-计算机视觉工程师" label="人工智能 - 计算机视觉工程师" />
                <t-option value="人工智能-NLP工程师" label="人工智能 - NLP工程师" />
                <t-option value="大数据-数据开发工程师" label="大数据 - 数据开发工程师" />
                <t-option value="大数据-数据分析师" label="大数据 - 数据分析师" />
                <t-option value="物联网-嵌入式工程师" label="物联网 - 嵌入式工程师" />
                <t-option value="物联网-物联网平台开发工程师" label="物联网 - 物联网平台开发工程师" />
                <t-option value="智能系统-智能制造工程师" label="智能系统 - 智能制造工程师" />
                <t-option value="智能系统-智能家居工程师" label="智能系统 - 智能家居工程师" />
                <t-option value="运维测试岗" label="运维测试岗" />
                <t-option value="产品岗" label="产品岗" />
              </t-select>
            </div>
          </t-col>

          <!-- 知识点 - 级联依岗位 -->
          <t-col :xs="12" :sm="6" :md="3">
            <div class="filter-item">
              <label class="filter-label">知识点</label>
              <t-select v-model="localFilters.knowledgePoints" placeholder="选择知识点" multiple clearable :max="8"
                :disabled="isLoading" @change="emitUpdate">
                <t-option v-for="point in availableKnowledgePoints" :key="point" :value="point" :label="point" />
              </t-select>
            </div>
          </t-col>
        </t-row>

        <!-- 已选择的知识点展示 -->
        <div v-if="localFilters.knowledgePoints.length > 0" class="selected-knowledge-points">
          <t-divider>已选择的知识点</t-divider>
          <t-space size="small" class="knowledge-tags">
            <t-tag v-for="point in localFilters.knowledgePoints" :key="point" theme="primary" variant="light" closable
              :disabled="isLoading" @close="removeKnowledgePoint(point)">
              {{ point }}
            </t-tag>
          </t-space>
        </div>
      </div>
    </div>
  </t-card>
</template>

<script setup>
import { reactive, watch, computed, ref } from 'vue'
import { useInterviewStore } from '@/stores/interviewStore'
import { useUserStore } from '@/stores/userStore'
import axiosLocal from '@/modules/axiosLocal'

const interviewStore = useInterviewStore()
const userStore = useUserStore()

const props = defineProps({
  filters: Object,
  isLoading: Boolean
})
const emit = defineEmits(['update-filters', 'generate-questions'])

const localFilters = reactive({
  mode: 'self-directed', // 默认自主设定模式
  selectedInterviewId: '',
  ...props.filters,
  knowledgePoints: [...props.filters.knowledgePoints]
})

// 计算属性：获取面试记录列表
const interviewRecords = computed(() => {
  return interviewStore.interview_record_list || []
})

// 计算属性：获取选中的面试记录详情
const selectedInterviewRecord = computed(() => {
  if (!localFilters.selectedInterviewId) return null
  return interviewRecords.value.find(record =>
    record.current_interview_id === localFilters.selectedInterviewId
  )
})

watch(() => props.filters, (newFilters) => {
  Object.assign(localFilters, {
    ...newFilters,
    knowledgePoints: [...newFilters.knowledgePoints]
  })
}, { deep: true })

const emitUpdate = () => {
  emit('update-filters', {
    ...localFilters,
    knowledgePoints: [...localFilters.knowledgePoints]
  })
}

// 解析面试ID，提取公司、岗位和时间
const parseInterviewId = (interviewId) => {
  const parts = interviewId.split('-')
  if (parts.length >= 3) {
    const company = parts[0]
    const position = parts[1]
    const timestamp = parts[2]
    return { company, position, timestamp }
  }
  return { company: '', position: '', timestamp: '' }
}

// 格式化面试记录标签
const formatInterviewLabel = (record) => {
  const parsed = parseInterviewId(record.current_interview_id)
  return `${parsed.company} - ${parsed.position} (${formatTime(record.start_time)})`
}

// 格式化时间显示
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理模式切换
const handleModeChange = () => {
  // 切换模式时重置相关字段
  if (localFilters.mode === 'interview-driven') {
    localFilters.selectedInterviewId = ''
  } else {
    localFilters.position = ''
    localFilters.difficulty = ''
    localFilters.knowledgePoints = []
  }
  emitUpdate()
}

// 处理面试记录选择
const handleInterviewRecordChange = () => {
  const selectedRecord = selectedInterviewRecord.value
  const current_interview_id = selectedRecord.current_interview_id

  axiosLocal.get('/interview/get_interview_report', {
    params: {
      email: userStore.user.email,
      current_interview_id: current_interview_id
    }
  }).then((res) => {
    if (res.data.code === 200) {
      // console.log(res.data.data)
      const knowledgeNames = res.data.data.knowledge_analysis.map(item => item.knowledge_name)
      localFilters.position = current_interview_id.split('-')[1]
      localFilters.knowledgePoints = knowledgeNames
      emitUpdate()
    }
  })

  axiosLocal.get('/resume/get_resume_md', {
    params: {
      email: userStore.user.email,
      current_interview_id: current_interview_id
    }
  }).then((res) => {
    if (res.data.code === 200) {
      // console.log(res.data.data)
      localFilters.resume = res.data.data
      localFilters.difficulty = '随机'
      emitUpdate()
    }
  })
}

const removeKnowledgePoint = (point) => {
  const index = localFilters.knowledgePoints.indexOf(point)
  if (index > -1) {
    localFilters.knowledgePoints.splice(index, 1)
    emitUpdate()
  }
}

const resetFilters = () => {
  localFilters.mode = 'self-directed'
  localFilters.selectedInterviewId = ''
  localFilters.questionCount = 10
  localFilters.position = ''
  localFilters.difficulty = ''
  localFilters.knowledgePoints = []
  emitUpdate()
}

const generateQuestions = () => {
  emit('generate-questions')
}

const knowledgeMap = {
  '前端工程师': ['HTML', 'CSS', 'JavaScript', 'Vue.js', 'React', '前端工程化', '性能优化'],
  '后端工程师': ['Java', 'Python', 'Go', '数据库', 'Redis', '微服务', '消息队列'],
  '人工智能-算法工程师': [
    '机器学习',
    '深度学习',
    '卷积神经网络',
    '自然语言处理',
    '推荐系统',
    '模型优化',
    'TensorFlow',
    'PyTorch',
    '数据标注'
  ],
  '人工智能-计算机视觉工程师': [
    '图像处理',
    '目标检测',
    'OpenCV',
    'YOLO',
    '图像分割',
    'GAN',
    '卷积神经网络'
  ],
  '人工智能-NLP工程师': [
    '自然语言处理',
    '文本分类',
    '序列标注',
    'BERT',
    'Transformer',
    '情感分析',
    '信息抽取'
  ],

  // 大数据领域
  '大数据-数据开发工程师': [
    'Hadoop',
    'Spark',
    'Flink',
    'Hive',
    'Kafka',
    '数据仓库',
    'ETL',
    'SQL调优'
  ],
  '大数据-数据分析师': [
    '数据可视化',
    '数据挖掘',
    '统计分析',
    'Python',
    'R',
    'Tableau',
    'PowerBI'
  ],

  // 物联网领域
  '物联网-嵌入式工程师': [
    'C语言',
    '嵌入式开发',
    'ARM架构',
    'RTOS',
    '硬件调试',
    '物联网协议',
    '传感器技术'
  ],
  '物联网-物联网平台开发工程师': [
    'MQTT',
    'CoAP',
    '物联网平台架构',
    '设备管理',
    '数据采集',
    '云平台对接'
  ],

  // 智能系统领域
  '智能系统-智能制造工程师': [
    'PLC',
    'SCADA',
    '工业机器人',
    '自动化控制',
    '工业以太网',
    '工业大数据'
  ],
  '智能系统-智能家居工程师': [
    '智能硬件',
    '智能控制',
    'ZigBee',
    '蓝牙',
    'HomeKit',
    '智能场景设计'
  ],

  // 通用岗位示例
  '运维测试岗': [
    'Linux',
    'Shell脚本',
    '网络基础',
    'Docker',
    'Kubernetes',
    'CI/CD',
    '性能测试',
    '安全测试'
  ],
  '产品岗': [
    '需求分析',
    '产品设计',
    'Axure',
    '竞品分析',
    '用户调研',
    '数据驱动设计'
  ]
}

const availableKnowledgePoints = computed(() => {
  return knowledgeMap[localFilters.position] || []
})

const handlePositionChange = () => {
  localFilters.knowledgePoints = []
  emitUpdate()
}
</script>

<style scoped>
.filter-panel {
  border-radius: 12px;
  border: 1px solid #e7e7e7;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.filter-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.filter-content {
  padding-top: 8px;
}

.mode-selection {
  margin-bottom: 16px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.interview-selection {
  margin-bottom: 16px;
}

.interview-option {
  padding: 8px 0;
}

.interview-main {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.company {
  font-weight: 600;
  color: #1f2937;
  background: #e3f2fd;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 13px;
}

.position {
  font-weight: 500;
  color: #0052d9;
  font-size: 14px;
}

.interview-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #666;
}

.time {
  color: #666;
}

.duration {
  background: #f0f0f0;
  padding: 1px 6px;
  border-radius: 3px;
}

.interviewer {
  color: #888;
}

.selected-interview-info {
  margin-top: 16px;
}

.interview-detail-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
}

.detail-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-weight: 500;
  color: #495057;
  width: 80px;
  flex-shrink: 0;
}

.detail-value {
  color: #212529;
  flex: 1;
}

.selected-knowledge-points {
  margin-top: 16px;
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
}

.generation-hint {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .interview-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .interview-meta {
    flex-wrap: wrap;
    gap: 8px;
  }
}

.description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
  padding: 12px;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
  border-radius: 6px;
  border-left: 3px solid #0052D9;
}
</style>

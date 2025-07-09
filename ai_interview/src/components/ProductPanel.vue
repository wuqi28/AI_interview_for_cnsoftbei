<template>
  <div class="interview-system">
    <t-layout class="layout-container">
      <!-- 左侧导航栏 -->
      <t-aside class="sidebar" width="280px">
        <div class="sidebar-header">
          <div class="logo">
            <t-icon name="layers" size="24px" />
            <span class="logo-text">产品岗位面试题</span>
          </div>
        </div>
        
        <div class="sidebar-content">
          <!-- 题目列表 -->
          <div class="question-nav">
            <h3 class="nav-title">
              <t-icon name="queue" />
              题目列表
            </h3>
            <div class="question-list">
              <div 
                v-for="(question, index) in questionList" 
                :key="question.id"
                class="question-item"
                :class="{ active: currentQuestionId === question.id }"
                @click="switchQuestion(question.id)"
              >
                <div class="question-number">{{ index + 1 }}</div>
                <div class="question-info">
                  <div class="question-title">{{ question.title }}</div>
                  <div class="question-meta">
                    <t-tag 
                      size="small" 
                      :theme="getDifficultyTheme(question.difficulty)"
                      variant="light"
                    >
                      {{ question.difficulty }}
                    </t-tag>
                    <span class="question-time">{{ question.timeLimit }}min</span>
                  </div>
                </div>
                <div class="question-status">
                  <t-icon 
                    :name="getQuestionStatusIcon(question.id)" 
                    :class="getQuestionStatusClass(question.id)"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 进度统计 -->
          <div class="progress-section">
            <h3 class="nav-title">
              <t-icon name="chart-pie" />
              答题进度
            </h3>
            <div class="progress-stats">
              <div class="stat-item">
                <div class="stat-number">{{ completedCount }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ questionList.length - completedCount }}</div>
                <div class="stat-label">待完成</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ Math.round((completedCount / questionList.length) * 100) }}%</div>
                <div class="stat-label">完成率</div>
              </div>
            </div>
          </div>
        </div>
      </t-aside>

      <!-- 主内容区域 -->
      <t-layout class="main-layout">
        <!-- 顶部状态栏 -->
        <t-header class="top-header">
          <div class="header-content">
            <div class="current-question">
              <t-breadcrumb>
                <t-breadcrumb-item>产品面试</t-breadcrumb-item>
                <t-breadcrumb-item>{{ currentQuestion.title }}</t-breadcrumb-item>
              </t-breadcrumb>
            </div>
            <div class="header-actions">
              <div class="timer-display">
                <t-icon name="time" />
                <span class="timer-text">{{ formatTime(timeLeft) }}</span>
              </div>
              <t-tag 
                :theme="getDifficultyTheme(currentQuestion.difficulty)" 
                variant="light"
                size="large"
              >
                {{ currentQuestion.difficulty }}
              </t-tag>
            </div>
          </div>
        </t-header>

        <!-- 主体内容 -->
        <t-content class="main-content">
          <div class="content-wrapper">
            <!-- 题目描述卡片 -->
            <t-card class="question-card" hover-shadow>
              <template #header>
                <div class="card-header">
                  <t-icon name="help-circle" />
                  <span>题目描述</span>
                </div>
              </template>
              <div class="question-description">
                {{ currentQuestion.description }}
              </div>
              
              <t-divider />
              
              <t-row :gutter="24">
                <t-col :span="12">
                  <h4><t-icon name="lightbulb" /> 参考示例</h4>
                  <ul class="example-list">
                    <li v-for="example in currentQuestion.examples" :key="example">
                      {{ example }}
                    </li>
                  </ul>
                </t-col>
                <t-col :span="12">
                  <h4><t-icon name="alert-circle" /> 约束条件</h4>
                  <ul class="constraints-list">
                    <li v-for="constraint in currentQuestion.constraints" :key="constraint">
                      {{ constraint }}
                    </li>
                  </ul>
                </t-col>
              </t-row>
            </t-card>

            <!-- 答题区域 -->
            <div class="answer-sections">
              <!-- 方案描述 -->
              <t-card class="answer-card" hover-shadow>
                <template #header>
                  <div class="card-header">
                    <t-icon name="edit" />
                    <span>方案描述</span>
                    <t-button 
                      size="small" 
                      variant="text" 
                      @click="toggleSection('editor')"
                    >
                      <t-icon :name="sectionExpanded.editor ? 'chevron-up' : 'chevron-down'" />
                    </t-button>
                  </div>
                </template>
                <div v-show="sectionExpanded.editor" class="card-content">
                  <div class="rich-editor">
                    <div class="editor-toolbar">
                      <div class="toolbar-group">
                        <button 
                          type="button"
                          class="toolbar-btn"
                          :class="{ active: isFormatActive('bold') }"
                          @click="formatText('bold')"
                          title="加粗"
                        >
                          <strong>B</strong>
                        </button>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          :class="{ active: isFormatActive('italic') }"
                          @click="formatText('italic')"
                          title="斜体"
                        >
                          <em>I</em>
                        </button>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          :class="{ active: isFormatActive('underline') }"
                          @click="formatText('underline')"
                          title="下划线"
                        >
                          <u>U</u>
                        </button>
                        <div class="toolbar-divider"></div>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          @click="formatText('insertUnorderedList')"
                          title="无序列表"
                        >
                          • 列表
                        </button>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          @click="formatText('insertOrderedList')"
                          title="有序列表"
                        >
                          1. 列表
                        </button>
                        <div class="toolbar-divider"></div>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          @click="insertHeading"
                          title="标题"
                        >
                          H1
                        </button>
                        <button 
                          type="button"
                          class="toolbar-btn"
                          @click="clearFormat"
                          title="清除格式"
                        >
                          清除
                        </button>
                      </div>
                    </div>
                    <div 
                      ref="richEditor"
                      class="editor-content"
                      contenteditable="true"
                      @input="onEditorInput"
                      @keydown="onEditorKeydown"
                      @paste="onEditorPaste"
                    >
                      <p>请详细描述您的产品方案...</p>
                    </div>
                  </div>
                </div>
              </t-card>

              <!-- 功能列表 -->
              <t-card class="answer-card" hover-shadow>
                <template #header>
                  <div class="card-header">
                    <t-icon name="view-list" />
                    <span>功能列表</span>
                    <div class="header-actions">
                      <t-button size="small" theme="primary" @click="addTableRow">
                        <t-icon name="add" />
                        添加
                      </t-button>
                      <t-button 
                        size="small" 
                        variant="text" 
                        @click="toggleSection('table')"
                      >
                        <t-icon :name="sectionExpanded.table ? 'chevron-up' : 'chevron-down'" />
                      </t-button>
                    </div>
                  </div>
                </template>
                <div v-show="sectionExpanded.table" class="card-content">
                  <t-table
                    :data="tableData"
                    :columns="tableColumns"
                    row-key="id"
                    stripe
                    hover
                    class="feature-table"
                  >
                    <template #feature="{ row }">
                      <t-input 
                        v-model="row.feature" 
                        placeholder="功能名称"
                        variant="text"
                        @change="updateTableData"
                      />
                    </template>
                    <template #priority="{ row }">
                      <t-select 
                        v-model="row.priority" 
                        :options="priorityOptions"
                        placeholder="选择优先级"
                        @change="updateTableData"
                      />
                    </template>
                    <template #owner="{ row }">
                      <t-input 
                        v-model="row.owner" 
                        placeholder="负责人"
                        variant="text"
                        @change="updateTableData"
                      />
                    </template>
                    <template #description="{ row }">
                      <t-input 
                        v-model="row.description" 
                        placeholder="功能描述"
                        variant="text"
                        @change="updateTableData"
                      />
                    </template>
                    <template #actions="{ rowIndex }">
                      <t-button 
                        size="small" 
                        theme="danger" 
                        variant="text"
                        @click="removeTableRow(rowIndex)"
                      >
                        <t-icon name="delete" />
                      </t-button>
                    </template>
                  </t-table>
                </div>
              </t-card>

              <!-- 流程图设计 -->
              <t-card class="answer-card" hover-shadow>
                <template #header>
                  <div class="card-header">
                    <t-icon name="flow" />
                    <span>流程图设计</span>
                    <div class="header-actions">
                      <t-button size="small" variant="outline" @click="refreshMermaid">
                        <t-icon name="refresh" />
                        刷新
                      </t-button>
                      <t-button 
                        size="small" 
                        variant="text" 
                        @click="toggleSection('mermaid')"
                      >
                        <t-icon :name="sectionExpanded.mermaid ? 'chevron-up' : 'chevron-down'" />
                      </t-button>
                    </div>
                  </div>
                </template>
                <div v-show="sectionExpanded.mermaid" class="card-content">
                  <t-row :gutter="16">
                    <t-col :span="12">
                      <div class="mermaid-editor">
                        <div class="editor-header">
                          <span>Mermaid 代码</span>
                          <t-button-group size="small" variant="outline">
                            <t-button @click="insertMermaidTemplate('flowchart')">
                              <t-icon name="flow" />
                              流程图
                            </t-button>
                            <t-button @click="insertMermaidTemplate('sequence')">
                              <t-icon name="swap-horiz" />
                              时序图
                            </t-button>
                            <t-button @click="insertMermaidTemplate('gantt')">
                              <t-icon name="calendar" />
                              甘特图
                            </t-button>
                          </t-button-group>
                        </div>
                        <t-textarea
                          v-model="mermaidCode"
                          placeholder="请输入Mermaid代码..."
                          :autosize="{ minRows: 12, maxRows: 20 }"
                          @input="debouncedUpdateMermaid"
                          class="mermaid-textarea"
                        />
                      </div>
                    </t-col>
                    <t-col :span="12">
                      <div class="mermaid-preview">
                        <div class="preview-header">
                          <span>实时预览</span>
                          <t-tag size="small" theme="success" v-if="mermaidValid">
                            <t-icon name="check-circle" />
                            语法正确
                          </t-tag>
                          <t-tag size="small" theme="danger" v-else>
                            <t-icon name="close-circle" />
                            语法错误
                          </t-tag>
                        </div>
                        <div class="mermaid-container">
                          <div 
                            ref="mermaidPreview" 
                            class="mermaid-chart"
                            v-html="mermaidHtml"
                          ></div>
                          <div v-if="mermaidError" class="mermaid-error">
                            <t-icon name="error-circle" />
                            <span>{{ mermaidError }}</span>
                          </div>
                        </div>
                      </div>
                    </t-col>
                  </t-row>
                </div>
              </t-card>
            </div>

            <!-- 操作按钮 -->
            <div class="action-section">
              <t-card class="action-card">
                <div class="action-buttons">
                  <t-button 
                    theme="primary" 
                    size="large"
                    @click="submitAnswer"
                    :loading="submitting"
                  >
                    <t-icon name="check" />
                    提交答案
                  </t-button>
                  <t-button 
                    theme="default" 
                    size="large"
                    @click="resetAnswer"
                  >
                    <t-icon name="refresh" />
                    重置答题
                  </t-button>
                  <t-button 
                    theme="success" 
                    size="large"
                    @click="exportPDF"
                  >
                    <t-icon name="download" />
                    导出PDF
                  </t-button>
                  <t-button 
                    variant="outline" 
                    size="large"
                    @click="saveProgress"
                  >
                    <t-icon name="save" />
                    保存草稿
                  </t-button>
                </div>
              </t-card>
            </div>
          </div>
        </t-content>
      </t-layout>
    </t-layout>

    <!-- AI点评弹窗 -->
    <t-dialog
      v-model:visible="showReview"
      header="AI 智能点评"
      width="700px"
      :footer="false"
      class="review-dialog"
    >
      <div class="ai-review">
        <t-loading :loading="reviewLoading" size="large">
          <div v-if="!reviewLoading" class="review-content">
            <t-alert theme="success" message="答案提交成功！" close />
            
            <div class="review-score-section">
              <div class="score-display">
                <div class="score-number">{{ reviewScore }}</div>
                <div class="score-label">综合评分</div>
              </div>
              <div class="score-breakdown">
                <div class="score-item">
                  <span>方案完整性</span>
                  <t-progress :percentage="85" size="small" />
                </div>
                <div class="score-item">
                  <span>逻辑清晰度</span>
                  <t-progress :percentage="90" size="small" />
                </div>
                <div class="score-item">
                  <span>创新性</span>
                  <t-progress :percentage="75" size="small" />
                </div>
              </div>
            </div>

            <t-divider />
            
            <div class="review-text">
              <h4><t-icon name="chat" /> AI 点评建议</h4>
              <p>{{ aiReview }}</p>
            </div>

            <div class="review-actions">
              <t-button theme="primary" :loading="isLoading" @click="goToReportPage">
                确认
              </t-button>
              <t-button variant="outline" @click="exportReview">
                导出点评
              </t-button>
            </div>
          </div>
        </t-loading>
      </div>
    </t-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { useDebounceFn } from '@vueuse/core'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLoading = ref(false)

const goToReportPage = () => {
  isLoading.value = true
  setTimeout(() => {
    router.push('/report')
  }, 2000)
}



// 面试题目库（适合面试时长）
const questionBank = [
  {
    id: 1,
    title: '外卖平台用户留存优化',
    difficulty: '中等',
    timeLimit: 20,
    description: '某外卖平台发现新用户7天留存率只有35%，请分析可能的原因并提出3个核心优化方案。',
    examples: [
      '从用户首次体验的关键节点分析',
      '考虑激励机制和用户习惯培养',
      '重点关注前3次下单体验'
    ],
    constraints: [
      '答题时间：20分钟',
      '至少提出3个具体方案',
      '需要简单的优先级排序',
      '画出用户留存关键路径'
    ]
  },
  {
    id: 2,
    title: '智能音箱儿童模式设计',
    difficulty: '简单',
    timeLimit: 15,
    description: '为智能音箱设计一个儿童模式，确保内容安全且具有教育价值，请设计核心功能和交互方式。',
    examples: [
      '考虑3-12岁儿童的使用特点',
      '内容筛选和家长控制功能',
      '寓教于乐的交互设计'
    ],
    constraints: [
      '答题时间：15分钟',
      '重点设计2-3个核心功能',
      '考虑安全性和教育性',
      '简单描述交互流程'
    ]
  },
  {
    id: 3,
    title: '共享单车停车治理方案',
    difficulty: '困难',
    timeLimit: 25,
    description: '共享单车乱停放问题严重影响城市管理，请从产品角度设计一套停车治理方案，平衡用户体验和城市管理需求。',
    examples: [
      '技术手段结合运营策略',
      '用户激励与约束机制',
      '与政府部门的协作模式'
    ],
    constraints: [
      '答题时间：25分钟',
      '需要考虑多方利益平衡',
      '提供可行的技术实现思路',
      '设计完整的治理流程'
    ]
  },
  {
    id: 4,
    title: '在线会议疲劳缓解功能',
    difficulty: '中等',
    timeLimit: 18,
    description: '疫情后在线会议成为常态，但"会议疲劳"问题突出。请为在线会议产品设计缓解疲劳的功能。',
    examples: [
      '从会议节奏和互动方式入手',
      '利用AI技术辅助会议管理',
      '考虑用户的身心健康'
    ],
    constraints: [
      '答题时间：18分钟',
      '设计2-3个创新功能',
      '考虑技术可行性',
      '绘制功能使用流程'
    ]
  },
  {
    id: 5,
    title: '老年人健康管理App',
    difficulty: '中等',
    timeLimit: 22,
    description: '设计一款面向60+老年人的健康管理App，需要考虑老年人的使用习惯和健康管理需求。',
    examples: [
      '简化操作界面和交互方式',
      '结合家庭成员的参与',
      '整合线上线下健康服务'
    ],
    constraints: [
      '答题时间：22分钟',
      '重点考虑易用性设计',
      '包含核心健康管理功能',
      '设计家庭互动机制'
    ]
  }
]

// 随机选择一道题作为当前题目
const getRandomQuestion = () => {
  const randomIndex = Math.floor(Math.random() * questionBank.length)
  return questionBank[randomIndex]
}

// 题目数据（随机选择3道题）
const questionList = ref(
  [...questionBank]
    .sort(() => 0.5 - Math.random())
    .slice(0, 1)
    .map((q, index) => ({ ...q, id: index + 1 }))
)


// 当前题目相关
const currentQuestionId = ref(1)
const currentQuestion = computed(() => 
  questionList.value.find(q => q.id === currentQuestionId.value) || questionList.value[0]
)

// 答题状态
const questionStatus = ref({
  1: 'in-progress',
  2: 'not-started',
  3: 'not-started'
})

const completedCount = computed(() => 
  Object.values(questionStatus.value).filter(status => status === 'completed').length
)

// 界面状态
const sectionExpanded = reactive({
  editor: true,
  table: true,
  mermaid: true
})

// 计时器
const timeLeft = ref(1200) // 20分钟默认
let timer = null

// 提交状态
const submitting = ref(false)
const showReview = ref(false)
const reviewLoading = ref(false)
const aiReview = ref('')
const reviewScore = ref(0)

// 富文本编辑器
const richEditor = ref(null)
const editorContent = ref('')

// 表格数据
const tableData = ref([
  { id: 1, feature: '', priority: '', owner: '', description: '' }
])

const tableColumns = [
  { colKey: 'feature', title: '功能名称', width: 150, cell: 'feature' },
  { colKey: 'priority', title: '优先级', width: 100, cell: 'priority' },
  { colKey: 'owner', title: '负责人', width: 100, cell: 'owner' },
  { colKey: 'description', title: '功能描述', width: 200, cell: 'description' },
  { colKey: 'actions', title: '操作', width: 80, cell: 'actions' }
]

const priorityOptions = [
  { label: 'P0-最高', value: 'P0' },
  { label: 'P1-高', value: 'P1' },
  { label: 'P2-中', value: 'P2' },
  { label: 'P3-低', value: 'P3' }
]

// Mermaid 相关
const mermaidCode = ref(`graph TD
    A[用户进入平台] --> B{首次使用?}
    B -->|是| C[新手引导]
    B -->|否| D[正常使用流程]
    C --> E[完成首单]
    E --> F[获得奖励]
    F --> G[培养使用习惯]
    D --> H[日常下单]
    G --> H
    H --> I[用户留存]`)

const mermaidHtml = ref('')
const mermaidPreview = ref(null)
const mermaidValid = ref(true)
const mermaidError = ref('')

// Mermaid 模板
const mermaidTemplates = {
  flowchart: `graph TD
    A[开始] --> B{判断条件}
    B -->|是| C[执行操作A]
    B -->|否| D[执行操作B]
    C --> E[结束]
    D --> E`,
  sequence: `sequenceDiagram
    participant U as 用户
    participant S as 系统
    participant D as 数据库
    
    U->>S: 发送请求
    S->>D: 查询数据
    D-->>S: 返回结果
    S-->>U: 响应数据`,
  gantt: `gantt
    title 项目进度计划
    dateFormat  YYYY-MM-DD
    section 需求分析
    需求调研    :done, des1, 2024-01-01, 2024-01-05
    需求整理    :active, des2, 2024-01-06, 3d
    section 设计阶段
    原型设计    :des3, after des2, 5d
    UI设计     :des4, after des3, 3d`
}

// 基础工具函数
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const getDifficultyTheme = (difficulty) => {
  const themes = {
    '简单': 'success',
    '中等': 'warning',
    '困难': 'danger'
  }
  return themes[difficulty] || 'default'
}

const getQuestionStatusIcon = (questionId) => {
  const status = questionStatus.value[questionId]
  const icons = {
    'not-started': 'circle',
    'in-progress': 'time',
    'completed': 'check-circle'
  }
  return icons[status] || 'circle'
}

const getQuestionStatusClass = (questionId) => {
  const status = questionStatus.value[questionId]
  return `status-${status}`
}

// Mermaid 相关函数
const updateMermaidPreview = async () => {
  if (!mermaidCode.value.trim()) {
    mermaidHtml.value = '<div class="empty-state">请输入Mermaid代码</div>'
    return
  }

  try {
    mermaidError.value = ''
    mermaidValid.value = true
    
    const mermaid = await import('mermaid')
    
    if (!mermaid.default.mermaidAPI) {
      mermaid.default.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: 'Arial, sans-serif'
      })
    }
    
    const id = `mermaid-${Date.now()}`
    const { svg } = await mermaid.default.render(id, mermaidCode.value)
    mermaidHtml.value = svg
    
  } catch (error) {
    console.error('Mermaid render error:', error)
    mermaidValid.value = false
    mermaidError.value = error.message || '流程图语法错误'
    mermaidHtml.value = '<div class="error-state">流程图渲染失败</div>'
  }
}

const initMermaid = async () => {
  try {
    await updateMermaidPreview()
  } catch (error) {
    console.error('Mermaid initialization failed:', error)
    mermaidError.value = 'Mermaid初始化失败'
  }
}

const refreshMermaid = () => {
  updateMermaidPreview()
  MessagePlugin.success('流程图已刷新')
}

const insertMermaidTemplate = (type) => {
  mermaidCode.value = mermaidTemplates[type]
  updateMermaidPreview()
  MessagePlugin.success(`已插入${type}模板`)
}

const debouncedUpdateMermaid = useDebounceFn(updateMermaidPreview, 500)

// 计时器函数
const startTimer = () => {
  // 根据当前题目设置时间
  timeLeft.value = currentQuestion.value.timeLimit * 60
  
  timer = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      clearInterval(timer)
      MessagePlugin.warning('答题时间已结束！')
    }
  }, 1000)
}

// 界面交互函数
const toggleSection = (section) => {
  sectionExpanded[section] = !sectionExpanded[section]
}

const switchQuestion = (questionId) => {
  if (currentQuestionId.value !== questionId) {
    saveCurrentProgress()
    currentQuestionId.value = questionId
    loadQuestionProgress(questionId)
    questionStatus.value[questionId] = 'in-progress'
    
    // 重置计时器
    clearInterval(timer)
    timeLeft.value = currentQuestion.value.timeLimit * 60
    startTimer()
    
    MessagePlugin.success(`已切换到：${currentQuestion.value.title}`)
  }
}

// 富文本编辑器函数
const formatText = (command, value = null) => {
  document.execCommand(command, false, value)
  richEditor.value?.focus()
}

const isFormatActive = (command) => {
  try {
    return document.queryCommandState(command)
  } catch (e) {
    return false
  }
}

const insertHeading = () => {
  const selection = window.getSelection()
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0)
    const heading = document.createElement('h3')
    heading.textContent = '标题'
    range.deleteContents()
    range.insertNode(heading)
    
    // 移动光标到标题后
    range.setStartAfter(heading)
    range.collapse(true)
    selection.removeAllRanges()
    selection.addRange(range)
  }
  richEditor.value?.focus()
}

const clearFormat = () => {
  formatText('removeFormat')
  formatText('unlink')
}

const onEditorInput = (e) => {
  editorContent.value = e.target.innerHTML
}

const onEditorKeydown = (e) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    formatText('insertHTML', '&nbsp;&nbsp;&nbsp;&nbsp;')
  }
}

const onEditorPaste = (e) => {
  e.preventDefault()
  const text = e.clipboardData.getData('text/plain')
  formatText('insertText', text)
}

// 表格函数
const addTableRow = () => {
  const newId = Math.max(...tableData.value.map(item => item.id)) + 1
  tableData.value.push({
    id: newId,
    feature: '',
    priority: '',
    owner: '',
    description: ''
  })
}

const removeTableRow = (index) => {
  if (tableData.value.length > 1) {
    tableData.value.splice(index, 1)
  } else {
    MessagePlugin.warning('至少保留一行数据')
  }
}

const updateTableData = () => {
  saveCurrentProgress()
}

// 数据保存和加载函数
const saveCurrentProgress = () => {
  const progressData = {
    questionId: currentQuestionId.value,
    editorContent: editorContent.value,
    tableData: tableData.value,
    mermaidCode: mermaidCode.value,
    timestamp: Date.now()
  }
  
  localStorage.setItem(`question_${currentQuestionId.value}`, JSON.stringify(progressData))
}

const loadQuestionProgress = (questionId) => {
  const saved = localStorage.getItem(`question_${questionId}`)
  if (saved) {
    try {
      const data = JSON.parse(saved)
      editorContent.value = data.editorContent || ''
      tableData.value = data.tableData || [{ id: 1, feature: '', priority: '', owner: '', description: '' }]
      mermaidCode.value = data.mermaidCode || mermaidTemplates.flowchart
      
      nextTick(() => {
        if (richEditor.value) {
          richEditor.value.innerHTML = editorContent.value || '<p>请详细描述您的产品方案...</p>'
        }
        updateMermaidPreview()
      })
    } catch (error) {
      console.error('Load progress error:', error)
    }
  } else {
    editorContent.value = ''
    tableData.value = [{ id: 1, feature: '', priority: '', owner: '', description: '' }]
    mermaidCode.value = mermaidTemplates.flowchart
    
    nextTick(() => {
      if (richEditor.value) {
        richEditor.value.innerHTML = '<p>请详细描述您的产品方案...</p>'
      }
      updateMermaidPreview()
    })
  }
}

const loadSavedProgress = () => {
  loadQuestionProgress(currentQuestionId.value)
}

const saveProgress = () => {
  saveCurrentProgress()
  MessagePlugin.success('草稿已保存')
}

// 主要操作函数
const submitAnswer = async () => {
  submitting.value = true
  
  try {
    saveCurrentProgress()
    
    const submitData = {
      questionId: currentQuestionId.value,
      answer_text: editorContent.value || richEditor.value?.innerHTML || '',
      table_data: tableData.value,
      flowchart_code: mermaidCode.value,
      submitted_at: new Date().toISOString()
    }
    
    console.log('Submit data:', submitData)
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    questionStatus.value[currentQuestionId.value] = 'completed'
    
    showReview.value = true
    reviewLoading.value = true
    
    setTimeout(() => {
      reviewLoading.value = false
      aiReview.value = '您的产品方案思路清晰，针对问题的分析较为深入。功能设计合理，优先级排序得当。流程图逻辑清楚，体现了良好的产品思维。建议在用户体验细节和数据验证方面进一步完善。'
      reviewScore.value = 86
    }, 1500)
    
    MessagePlugin.success('答案提交成功！')
    
  } catch (error) {
    MessagePlugin.error('提交失败，请重试')
    console.error('Submit error:', error)
  } finally {
    submitting.value = false
  }
}

const resetAnswer = () => {
  editorContent.value = ''
  tableData.value = [{ id: 1, feature: '', priority: '', owner: '', description: '' }]
  mermaidCode.value = mermaidTemplates.flowchart
  
  if (richEditor.value) {
    richEditor.value.innerHTML = '<p>请详细描述您的产品方案...</p>'
  }
  
  updateMermaidPreview()
  localStorage.removeItem(`question_${currentQuestionId.value}`)
  MessagePlugin.success('答题内容已重置')
}

const exportPDF = () => {
  MessagePlugin.info('PDF导出功能开发中...')
}

const exportReview = () => {
  const reviewData = {
    questionTitle: currentQuestion.value.title,
    score: reviewScore.value,
    review: aiReview.value,
    submittedAt: new Date().toISOString()
  }
  
  const dataStr = JSON.stringify(reviewData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `review-${currentQuestion.value.title}.json`
  link.click()
  URL.revokeObjectURL(url)
  
  MessagePlugin.success('点评报告导出成功！')
}

// 生命周期
onMounted(async () => {
  loadSavedProgress()
  startTimer()
  await nextTick()
  setTimeout(() => {
    initMermaid()
  }, 100)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.interview-system {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.layout-container {
  height: 100vh;
}

/* 左侧边栏样式 */
.sidebar {
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  background-color: rgb(0, 82, 217);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-content {
  padding: 20px;
}

.nav-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.question-list {
  margin-bottom: 32px;
}

.question-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 8px;
}

.question-item:hover {
  background-color: #f8f9fa;
}

.question-item.active {
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  background-color: rgb(0, 82, 217);
  color: white;
}

.question-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.question-item.active .question-number {
  background-color: rgba(255,255,255,0.2);
  color: white;
}

.question-info {
  flex: 1;
  min-width: 0;
}

.question-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.question-time {
  color: #666;
}

.question-item.active .question-time {
  color: rgba(255,255,255,0.8);
}

.question-status {
  flex-shrink: 0;
}

.status-not-started {
  color: #ccc;
}

.status-in-progress {
  color: #ff9500;
}

.status-completed {
  color: #52c41a;
}

.question-item.active .status-not-started,
.question-item.active .status-in-progress,
.question-item.active .status-completed {
  color: white;
}

.progress-section {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.stat-item {
  text-align: center;
  flex: 1;
  padding: 12px 8px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

/* 主内容区域样式 */
.main-layout {
  background-color: #f5f7fa;
}

.top-header {
  background: white;
  padding: 16px 24px;
  border-bottom: 1px solid #e7e7e7;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.timer-display {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.timer-text {
  font-family: 'Monaco', 'Menlo', monospace;
}

.main-content {
  padding: 24px;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* 卡片样式 */
.question-card,
.answer-card,
.action-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.question-card:hover,
.answer-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
}

.card-header .header-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}

.card-content {
  padding-top: 16px;
}

.question-description {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 20px;
}

.example-list,
.constraints-list {
  margin: 0;
  padding-left: 20px;
  color: #666;
}

.example-list li,
.constraints-list li {
  margin-bottom: 8px;
  line-height: 1.5;
}

/* 富文本编辑器样式 */
.rich-editor {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.editor-toolbar {
  padding: 12px;
  background-color: #fafafa;
  border-bottom: 1px solid #e0e0e0;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-btn {
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 28px;
}

.toolbar-btn:hover {
  border-color: #0052d9;
  color: #0052d9;
}

.toolbar-btn.active {
  background-color: #0052d9;
  color: white;
  border-color: #0052d9;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background-color: #e0e0e0;
  margin: 0 8px;
}

.editor-content {
  min-height: 200px;
  padding: 16px;
  outline: none;
  line-height: 1.6;
  font-size: 14px;
}

.editor-content:empty::before {
  content: '请详细描述您的产品方案...';
  color: #bbb;
}

.editor-content h3 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 18px;
}

.editor-content ul, .editor-content ol {
  margin: 8px 0;
  padding-left: 24px;
}

.editor-content li {
  margin-bottom: 4px;
}

/* 表格样式 */
.feature-table {
  margin-top: 16px;
}

/* Mermaid 样式 */
.mermaid-editor {
  height: 100%;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.mermaid-textarea {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 13px;
}

.mermaid-preview {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  height: 400px;
  overflow: hidden;
  background: white;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #fafafa;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
  font-weight: 500;
}

.mermaid-container {
  height: calc(100% - 49px);
  overflow: auto;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mermaid-chart {
  max-width: 100%;
  max-height: 100%;
}

.empty-state,
.error-state {
  color: #999;
  text-align: center;
  padding: 40px 20px;
}

.error-state {
  color: #e34d59;
}

.mermaid-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e34d59;
  background-color: #fef2f2;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
}

/* 操作按钮样式 */
.action-section {
  margin-top: 32px;
}

.action-card {
  background: white;
  text-align: center;
  padding: 24px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

/* AI点评弹窗样式 */
.review-dialog {
  border-radius: 12px;
}

.ai-review {
  padding: 8px 0;
}

.review-score-section {
  display: flex;
  gap: 24px;
  align-items: center;
  margin: 24px 0;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.score-display {
  text-align: center;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
}

.score-label {
  font-size: 14px;
  opacity: 0.9;
}

.score-breakdown {
  flex: 1;
}

.score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
}

.score-item:last-child {
  margin-bottom: 0;
}

.review-text h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 16px 0 12px 0;
  color: #333;
}

.review-text p {
  line-height: 1.6;
  color: #666;
  margin-bottom: 20px;
}

.review-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px !important;
  }
  
  .content-wrapper {
    padding: 0 16px;
  }
}

@media (max-width: 768px) {
  .layout-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100% !important;
    height: auto;
    order: 2;
  }
  
  .main-layout {
    order: 1;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .t-button {
    width: 100%;
  }
  
  .review-score-section {
    flex-direction: column;
    text-align: center;
  }
  
  .toolbar-group {
    flex-wrap: wrap;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 16px;
  }
  
  .question-item {
    padding: 8px;
  }
  
  .question-title {
    font-size: 13px;
  }
  
  .toolbar-btn {
    font-size: 11px;
    padding: 4px 8px;
    min-width: 28px;
    height: 24px;
  }
}
</style>
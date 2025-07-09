<template>
  <div class="ops-exam-system">
    <!-- 头部 -->
    <t-layout>
      <t-header class="header">
        <div class="header-content">
          <h1 class="title">
            <t-icon name="server" class="title-icon" />
            运维测试岗面试题
          </h1>
          <div class="exam-info">
            <t-tag theme="primary" variant="light">
              <t-icon name="time" />
              剩余时间: {{ formatTime(remainingTime) }}
            </t-tag>
            <!-- <t-tag theme="success" variant="light">
              完成进度: {{ completedQuestions }}/{{ totalQuestions }}
            </t-tag> -->
          </div>
          <div>
            <t-button theme="primary" :loading="isLoading" @click="submit">
              提交答案
            </t-button>
          </div>
        </div>
      </t-header>

      <t-content class="main-content">
        <div class="exam-container">
          <!-- 侧边导航 -->
          <div class="sidebar">
            <t-menu v-model="activeSection" theme="light">
              <t-menu-item value="process" @click="setActiveSection('process')">
                <template #icon><t-icon name="swap" /></template>
                流程排序题
              </t-menu-item>
              <t-menu-item value="scenario" @click="setActiveSection('scenario')">
                <template #icon><t-icon name="help-circle" /></template>
                场景决策题
              </t-menu-item>
              <!-- <t-menu-item value="command" @click="setActiveSection('command')">
                <template #icon><t-icon name="terminal" /></template>
                命令行模拟
              </t-menu-item> -->
              <!-- <t-menu-item value="result" @click="setActiveSection('result')">
                <template #icon><t-icon name="chart-bar" /></template>
                考试结果
              </t-menu-item> -->
            </t-menu>
          </div>

          <!-- 主要内容区域 -->
          <div class="content-area">
            <!-- 流程排序题 -->
            <el-scrollbar height="800px">
              <div v-if="activeSection === 'process'" class="section">
                <t-card title="服务异常处理流程排序" class="question-card">
                  <template #subtitle>
                    请将以下操作步骤按照正确的处理顺序进行排序
                  </template>

                  <div class="drag-container">
                    <div class="drag-area">
                      <h4>待排序步骤：</h4>
                      <div class="drag-list">
                        <transition-group name="drag-list" tag="div">
                          <div v-for="(element, index) in processSteps" :key="element.id" class="drag-item" :class="{
                            'correct': element.isCorrect,
                            'incorrect': element.isIncorrect,
                            'dragging': draggedIndex === index,
                            'drag-over': dragOverIndex === index && draggedIndex !== index
                          }" draggable="true" @dragstart="onDragStart($event, index)"
                            @dragover.prevent="onDragOver($event, index)"
                            @dragenter.prevent="onDragEnter($event, index)"
                            @dragleave.prevent="onDragLeave($event, index)" @drop="onDrop($event, index)"
                            @dragend="onDragEnd">
                            <t-icon name="drag" class="drag-handle" />
                            <span class="step-number">{{ index + 1 }}</span>
                            <span class="step-text">{{ element.text }}</span>
                            <t-icon v-if="element.isCorrect" name="check-circle" class="status-icon correct" />
                            <t-icon v-if="element.isIncorrect" name="close-circle" class="status-icon incorrect" />
                            <div class="drag-indicator" v-if="dragOverIndex === index && draggedIndex !== index"></div>
                          </div>
                        </transition-group>
                      </div>
                    </div>

                    <div class="action-buttons">
                      <t-button theme="primary" @click="checkProcessOrder">
                        <t-icon name="check" />
                        检查答案
                      </t-button>
                      <t-button theme="default" @click="resetProcessOrder">
                        <t-icon name="refresh" />
                        重置
                      </t-button>
                    </div>
                  </div>

                  <t-alert v-if="processResult" :theme="processResult.type" class="result-alert">
                    {{ processResult.message }}
                    <div v-if="processResult.score !== null" class="score">
                      得分: {{ processResult.score }}/100
                    </div>
                  </t-alert>
                </t-card>
              </div>

              <!-- 场景决策题 -->
              <div v-if="activeSection === 'scenario'" class="section">
                <t-card title="场景决策题" class="question-card">
                  <div v-for="(question, index) in scenarioQuestions" :key="question.id" class="scenario-question">
                    <h4>{{ index + 1 }}. {{ question.title }}</h4>
                    <p class="question-desc">{{ question.description }}</p>

                    <t-radio-group v-if="question.type === 'single'" v-model="question.answer"
                      @change="updateScenarioAnswer(question.id, $event)">
                      <t-radio v-for="option in question.options" :key="option.value" :value="option.value"
                        class="option-item">
                        {{ option.label }}
                      </t-radio>
                    </t-radio-group>

                    <t-checkbox-group v-if="question.type === 'multiple'" v-model="question.answer"
                      @change="updateScenarioAnswer(question.id, $event)">
                      <t-checkbox v-for="option in question.options" :key="option.value" :value="option.value"
                        class="option-item">
                        {{ option.label }}
                      </t-checkbox>
                    </t-checkbox-group>

                    <div v-if="question.result" class="question-result">
                      <t-alert :theme="question.result.correct ? 'success' : 'error'">
                        {{ question.result.explanation }}
                        <div class="score">得分: {{ question.result.score }}/{{ question.maxScore }}</div>
                      </t-alert>
                    </div>
                  </div>

                  <div class="action-buttons">
                    <t-button theme="primary" @click="checkScenarioAnswers">
                      <t-icon name="check" />
                      提交答案
                    </t-button>
                  </div>
                </t-card>
              </div>

              <!-- 命令行模拟 -->
              <div v-if="activeSection === 'command'" class="section">
                <t-card title="命令行模拟" class="question-card">
                  <template #subtitle>
                    在下方终端中输入运维命令，系统将模拟返回结果
                  </template>
                  <div v-if="currentCommandQuestion" class="command-question-info">
                    <t-alert theme="info" class="question-alert">
                      <h4>{{ currentCommandQuestion.title }}</h4>
                      <p>{{ currentCommandQuestion.scenario }}</p>
                      <div class="command-hints-inline">
                        <strong>提示：</strong>
                        <t-tag v-for="hint in currentCommandQuestion.hints" :key="hint" size="small"
                          class="hint-tag-small">
                          {{ hint }}
                        </t-tag>
                      </div>
                    </t-alert>
                  </div>

                  <div class="terminal-container">
                    <div class="terminal">
                      <div class="terminal-header">
                        <div class="terminal-buttons">
                          <span class="btn red"></span>
                          <span class="btn yellow"></span>
                          <span class="btn green"></span>
                        </div>
                        <span class="terminal-title">运维终端模拟器</span>
                      </div>

                      <div class="terminal-body" ref="terminalBody">
                        <div v-for="(entry, index) in terminalHistory" :key="index" class="terminal-entry">
                          <div class="command-line">
                            <span class="prompt">root@server:~$ </span>
                            <span class="command">{{ entry.command }}</span>
                          </div>
                          <div v-if="entry.output" class="command-output" v-html="entry.output"></div>
                        </div>

                        <div class="current-line">
                          <span class="prompt">root@server:~$ </span>
                          <input v-model="currentCommand" @keyup.enter="executeCommand" class="command-input"
                            placeholder="输入命令..." ref="commandInput" />
                        </div>
                      </div>
                    </div>

                    <div class="command-hints">
                      <h4>常用命令提示：</h4>
                      <t-tag v-for="hint in commandHints" :key="hint" @click="insertCommand(hint)" class="hint-tag">
                        {{ hint }}
                      </t-tag>
                    </div>
                  </div>

                  <div class="command-score">
                    <t-alert theme="info">
                      命令执行统计: 正确 {{ commandStats.correct }} / 总计 {{ commandStats.total }}
                      <div class="score">准确率: {{ commandAccuracy }}%</div>
                    </t-alert>
                  </div>
                </t-card>
              </div>

              <!-- 考试结果 -->
              <div v-if="activeSection === 'result'" class="section">
                <t-card title="考试结果" class="question-card">
                  <div class="result-overview">
                    <div class="score-circle">
                      <div class="circle-progress" :style="{ '--progress': totalScore }">
                        <span class="score-text">{{ totalScore }}</span>
                        <span class="score-label">总分</span>
                      </div>
                    </div>

                    <div class="result-details">
                      <div class="detail-item">
                        <h4>流程排序题</h4>
                        <t-progress :percentage="processScore" :color="getScoreColor(processScore)" />
                        <span class="score-value">{{ processScore }}/100</span>
                      </div>

                      <div class="detail-item">
                        <h4>场景决策题</h4>
                        <t-progress :percentage="scenarioScore" :color="getScoreColor(scenarioScore)" />
                        <span class="score-value">{{ scenarioScore }}/100</span>
                      </div>

                      <div class="detail-item">
                        <h4>命令行模拟</h4>
                        <t-progress :percentage="commandScore" :color="getScoreColor(commandScore)" />
                        <span class="score-value">{{ commandScore }}/100</span>
                      </div>
                    </div>
                  </div>

                  <div class="result-analysis">
                    <h4>能力分析</h4>
                    <div class="analysis-chart">
                      <div class="skill-item" v-for="skill in skillAnalysis" :key="skill.name">
                        <span class="skill-name">{{ skill.name }}</span>
                        <t-progress :percentage="skill.score" :color="skill.color" />
                        <span class="skill-level">{{ skill.level }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="action-buttons">
                    <t-button theme="primary" @click="exportResult">
                      <t-icon name="download" />
                      导出结果
                    </t-button>
                    <t-button theme="default" @click="restartExam">
                      <t-icon name="refresh" />
                      重新开始
                    </t-button>
                  </div>
                </t-card>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </t-content>
    </t-layout>

    <!-- 故障模拟弹窗 -->
    <!-- <t-dialog 
      v-model:visible="faultSimulation.visible" 
      title="故障模拟" 
      width="600px"
      @confirm="handleFaultResponse"
    >
      <div class="fault-content">
        <t-alert theme="error" class="fault-alert">
          <t-icon name="error-circle" />
          {{ faultSimulation.description }}
        </t-alert>
        
        <h4>请选择处理方案：</h4>
        <t-radio-group v-model="faultSimulation.selectedSolution">
          <t-radio 
            v-for="solution in faultSimulation.solutions" 
            :key="solution.id" 
            :value="solution.id"
            class="solution-option"
          >
            {{ solution.text }}
          </t-radio>
        </t-radio-group>
      </div>
    </t-dialog> -->
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLoading = ref(false)

const submit = () => {
  isLoading.value = true
  setTimeout(() => {
    router.push('/report')
  }, 2000)
}

// 响应式数据
const activeSection = ref('process')
const remainingTime = ref(3600) // 60分钟
const completedQuestions = ref(0)
const totalQuestions = ref(10)

// 拖拽相关
const draggedIndex = ref(null)
const dragOverIndex = ref(null)

// 流程排序题数据
const processSteps = ref([
  { id: 1, text: '确认故障现象和影响范围', correctOrder: 1, isCorrect: false, isIncorrect: false },
  { id: 2, text: '查看系统日志和监控数据', correctOrder: 2, isCorrect: false, isIncorrect: false },
  { id: 3, text: '定位故障根本原因', correctOrder: 3, isCorrect: false, isIncorrect: false },
  { id: 4, text: '制定应急处理方案', correctOrder: 4, isCorrect: false, isIncorrect: false },
  { id: 5, text: '执行故障修复操作', correctOrder: 5, isCorrect: false, isIncorrect: false },
  { id: 6, text: '验证修复效果', correctOrder: 6, isCorrect: false, isIncorrect: false },
  { id: 7, text: '编写故障处理报告', correctOrder: 7, isCorrect: false, isIncorrect: false },
  { id: 8, text: '总结经验和改进措施', correctOrder: 8, isCorrect: false, isIncorrect: false }
])

const originalProcessSteps = [...processSteps.value]
const processResult = ref(null)
const processScore = ref(0)

// 场景决策题数据
// 场景决策题题库
const scenarioQuestionsBank = [
  {
    id: 1,
    type: 'single',
    title: '服务器CPU使用率持续90%以上',
    description: '生产环境服务器CPU使用率持续在90%以上，用户反馈系统响应缓慢，你的优先操作是？',
    options: [
      { value: 'A', label: '立即重启服务器' },
      { value: 'B', label: '查看进程列表，定位高CPU占用进程' },
      { value: 'C', label: '增加服务器配置' },
      { value: 'D', label: '通知用户系统维护' }
    ],
    correctAnswer: 'B',
    maxScore: 20
  },
  {
    id: 2,
    type: 'multiple',
    title: '数据库连接异常处理',
    description: '应用系统出现数据库连接异常，可能的排查步骤包括：',
    options: [
      { value: 'A', label: '检查数据库服务状态' },
      { value: 'B', label: '验证网络连通性' },
      { value: 'C', label: '检查连接池配置' },
      { value: 'D', label: '查看数据库日志' },
      { value: 'E', label: '重启应用服务' }
    ],
    correctAnswer: ['A', 'B', 'C', 'D'],
    maxScore: 20
  },
  {
    id: 3,
    type: 'single',
    title: '磁盘空间不足告警',
    description: '收到服务器磁盘使用率95%的告警，应用日志显示写入失败，最紧急的处理措施是？',
    options: [
      { value: 'A', label: '立即清理日志文件和临时文件' },
      { value: 'B', label: '申请扩容磁盘' },
      { value: 'C', label: '迁移部分数据到其他服务器' },
      { value: 'D', label: '重启服务释放缓存' }
    ],
    correctAnswer: 'A',
    maxScore: 20
  },
  {
    id: 4,
    type: 'multiple',
    title: '网站访问缓慢排查',
    description: '用户反馈网站访问缓慢，作为运维人员需要检查哪些方面？',
    options: [
      { value: 'A', label: '服务器CPU和内存使用情况' },
      { value: 'B', label: '网络带宽使用情况' },
      { value: 'C', label: '数据库查询性能' },
      { value: 'D', label: '应用程序日志' },
      { value: 'E', label: 'CDN缓存状态' }
    ],
    correctAnswer: ['A', 'B', 'C', 'D', 'E'],
    maxScore: 20
  },
  {
    id: 5,
    type: 'single',
    title: '服务进程异常退出',
    description: '关键业务服务进程异常退出，用户无法正常访问，首要处理步骤是？',
    options: [
      { value: 'A', label: '查看系统日志分析退出原因' },
      { value: 'B', label: '立即重启服务进程' },
      { value: 'C', label: '检查服务器硬件状态' },
      { value: 'D', label: '通知开发团队' }
    ],
    correctAnswer: 'B',
    maxScore: 20
  },
  {
    id: 6,
    type: 'multiple',
    title: '系统安全加固措施',
    description: '新部署的Linux服务器需要进行安全加固，应该包括哪些措施？',
    options: [
      { value: 'A', label: '修改默认SSH端口' },
      { value: 'B', label: '禁用root用户远程登录' },
      { value: 'C', label: '配置防火墙规则' },
      { value: 'D', label: '定期更新系统补丁' },
      { value: 'E', label: '设置复杂密码策略' }
    ],
    correctAnswer: ['A', 'B', 'C', 'D', 'E'],
    maxScore: 20
  },
  {
    id: 7,
    type: 'single',
    title: '数据库备份策略',
    description: '生产环境数据库需要制定备份策略，最合理的方案是？',
    options: [
      { value: 'A', label: '每天凌晨进行全量备份' },
      { value: 'B', label: '每周全量备份，每天增量备份' },
      { value: 'C', label: '每月全量备份，每周增量备份' },
      { value: 'D', label: '实时同步到备份服务器' }
    ],
    correctAnswer: 'B',
    maxScore: 20
  },
  {
    id: 8,
    type: 'multiple',
    title: '负载均衡故障处理',
    description: '负载均衡器后端某台服务器出现故障，需要进行哪些操作？',
    options: [
      { value: 'A', label: '从负载均衡器中移除故障服务器' },
      { value: 'B', label: '检查故障服务器的具体问题' },
      { value: 'C', label: '监控其他服务器的负载情况' },
      { value: 'D', label: '准备备用服务器' },
      { value: 'E', label: '通知相关人员' }
    ],
    correctAnswer: ['A', 'B', 'C', 'D', 'E'],
    maxScore: 20
  }
]

// 从题库中随机选择5道题
const scenarioQuestions = ref([])

// 命令行模拟数据
const currentCommand = ref('')
const terminalHistory = ref([
  {
    command: 'welcome',
    output: '<span style="color: #00ff00;">欢迎使用运维终端模拟器！输入命令开始操作...</span>'
  }
])

const commandStats = reactive({
  correct: 0,
  total: 0
})

const commandHints = [
  'top', 'ps aux', 'df -h', 'free -m', 'netstat -tulpn',
  'systemctl status', 'tail -f /var/log/syslog', 'htop'
]

// 命令行模拟题库
const commandQuestionsBank = [
  {
    id: 1,
    title: '系统性能监控',
    description: '服务器响应缓慢，需要查看系统资源使用情况',
    scenario: '用户反馈系统访问缓慢，请使用命令查看CPU、内存使用情况',
    requiredCommands: ['top', 'free -m', 'ps aux'],
    hints: ['查看实时进程信息', '查看内存使用情况', '查看所有进程']
  },
  {
    id: 2,
    title: '磁盘空间检查',
    description: '收到磁盘空间不足告警，需要排查磁盘使用情况',
    scenario: '系统告警磁盘空间不足，请检查磁盘使用情况并找出占用空间较大的目录',
    requiredCommands: ['df -h', 'du -sh /*', 'find / -size +100M'],
    hints: ['查看磁盘使用情况', '查看目录大小', '查找大文件']
  },
  {
    id: 3,
    title: '网络连接诊断',
    description: '应用无法连接数据库，需要检查网络连接状态',
    scenario: '应用报告数据库连接失败，请检查网络连接和端口状态',
    requiredCommands: ['netstat -tulpn', 'ping database-server', 'telnet database-server 3306'],
    hints: ['查看端口监听状态', '测试网络连通性', '测试端口连通性']
  },
  {
    id: 4,
    title: '日志分析排错',
    description: '应用出现异常，需要查看相关日志进行排错',
    scenario: '应用服务异常，请查看系统日志和应用日志定位问题',
    requiredCommands: ['tail -f /var/log/syslog', 'journalctl -u service-name', 'grep ERROR /var/log/app.log'],
    hints: ['实时查看系统日志', '查看服务日志', '搜索错误信息']
  },
  {
    id: 5,
    title: '服务管理操作',
    description: '需要管理系统服务的启动、停止和状态检查',
    scenario: '某个关键服务停止运行，请检查服务状态并重启服务',
    requiredCommands: ['systemctl status nginx', 'systemctl restart nginx', 'systemctl enable nginx'],
    hints: ['查看服务状态', '重启服务', '设置开机自启']
  }
]

// 当前命令行题目
const currentCommandQuestion = ref(null)

const commandScore = ref(0)

// 故障模拟数据
const faultSimulation = reactive({
  visible: false,
  description: '',
  solutions: [],
  selectedSolution: null
})

// 计算属性
const totalScore = computed(() => {
  return Math.round((processScore.value + scenarioScore.value + commandScore.value) / 3)
})

const commandAccuracy = computed(() => {
  if (commandStats.total === 0) return 0
  return Math.round((commandStats.correct / commandStats.total) * 100)
})

const skillAnalysis = computed(() => [
  { name: '故障诊断', score: processScore.value, level: getSkillLevel(processScore.value), color: '#1890ff' },
  { name: '应急处理', score: scenarioScore.value, level: getSkillLevel(scenarioScore.value), color: '#52c41a' },
  { name: '命令操作', score: commandScore.value, level: getSkillLevel(commandScore.value), color: '#faad14' },
  { name: '综合能力', score: totalScore.value, level: getSkillLevel(totalScore.value), color: '#722ed1' }
])

// 拖拽方法
const onDragStart = (event, index) => {
  draggedIndex.value = index
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/html', event.target.outerHTML)
  // 添加拖拽开始的延迟效果
  setTimeout(() => {
    if (draggedIndex.value === index) {
      // 可以在这里添加额外的视觉效果
    }
  }, 100)
}

const onDragEnter = (event, index) => {
  if (draggedIndex.value !== null && draggedIndex.value !== index) {
    dragOverIndex.value = index
  }
}

const onDragLeave = (event, index) => {
  // 检查是否真的离开了元素
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX
  const y = event.clientY

  if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
    if (dragOverIndex.value === index) {
      dragOverIndex.value = null
    }
  }
}

const onDragOver = (event, index) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
  if (draggedIndex.value !== null && draggedIndex.value !== index) {
    dragOverIndex.value = index
  }
}

const onDrop = (event, dropIndex) => {
  event.preventDefault()
  if (draggedIndex.value !== null && draggedIndex.value !== dropIndex) {
    const draggedItem = processSteps.value[draggedIndex.value]
    processSteps.value.splice(draggedIndex.value, 1)
    processSteps.value.splice(dropIndex, 0, draggedItem)
    onStepsChange()
  }
  dragOverIndex.value = null
}

const onDragEnd = () => {
  draggedIndex.value = null
  dragOverIndex.value = null
}

// 其他方法
const setActiveSection = (section) => {
  activeSection.value = section
}

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const onStepsChange = () => {
  // 重置状态
  processSteps.value.forEach(step => {
    step.isCorrect = false
    step.isIncorrect = false
  })
  processResult.value = null
}

const checkProcessOrder = () => {
  let correctCount = 0

  processSteps.value.forEach((step, index) => {
    const isCorrect = step.correctOrder === index + 1
    step.isCorrect = isCorrect
    step.isIncorrect = !isCorrect
    if (isCorrect) correctCount++
  })

  const score = Math.round((correctCount / processSteps.value.length) * 100)
  processScore.value = score

  processResult.value = {
    type: score >= 80 ? 'success' : score >= 60 ? 'warning' : 'error',
    message: score >= 80 ? '优秀！流程排序完全正确' :
      score >= 60 ? '良好，大部分步骤正确' : '需要改进，请重新学习运维流程',
    score: score
  }

  updateCompletedQuestions()
}

const resetProcessOrder = () => {
  processSteps.value = [...originalProcessSteps].sort(() => Math.random() - 0.5)
  processResult.value = null
  processScore.value = 0
}

const updateScenarioAnswer = (questionId, answer) => {
  const question = scenarioQuestions.value.find(q => q.id === questionId)
  if (question) {
    question.answer = answer
  }
}

const checkScenarioAnswers = () => {
  let totalScore = 0

  scenarioQuestions.value.forEach(question => {
    let isCorrect = false
    let score = 0

    if (question.type === 'single') {
      isCorrect = question.answer === question.correctAnswer
      score = isCorrect ? question.maxScore : 0
    } else if (question.type === 'multiple') {
      const userAnswer = question.answer || []
      const correctAnswer = question.correctAnswer

      if (userAnswer.length === correctAnswer.length &&
        userAnswer.every(ans => correctAnswer.includes(ans))) {
        isCorrect = true
        score = question.maxScore
      } else {
        // 部分正确给部分分数
        const correctCount = userAnswer.filter(ans => correctAnswer.includes(ans)).length
        const incorrectCount = userAnswer.filter(ans => !correctAnswer.includes(ans)).length
        score = Math.max(0, Math.round((correctCount - incorrectCount) / correctAnswer.length * question.maxScore))
      }
    }

    question.result = {
      correct: isCorrect,
      score: score,
      explanation: isCorrect ? '回答正确！' : `正确答案是: ${Array.isArray(question.correctAnswer) ? question.correctAnswer.join(', ') : question.correctAnswer}`
    }

    totalScore += score
  })

  const scenarioScore = Math.round(totalScore / scenarioQuestions.value.reduce((sum, q) => sum + q.maxScore, 0) * 100)
  updateCompletedQuestions()
}

const executeCommand = () => {
  if (!currentCommand.value.trim()) return

  const command = currentCommand.value.trim()
  const output = simulateCommand(command)

  terminalHistory.value.push({
    command: command,
    output: output.content
  })

  // 更新统计
  commandStats.total++
  if (output.correct) {
    commandStats.correct++
  }

  commandScore.value = commandAccuracy.value

  currentCommand.value = ''

  nextTick(() => {
    const terminalBody = document.querySelector('.terminal-body')
    if (terminalBody) {
      terminalBody.scrollTop = terminalBody.scrollHeight
    }
  })

  updateCompletedQuestions()
}

const simulateCommand = (command) => {
  const commands = {
    'top': {
      content: `<div style="color: #00ff00;">
top - 14:30:25 up 5 days, 2:15, 3 users, load average: 0.85, 0.92, 1.05<br>
Tasks: 245 total, 2 running, 243 sleeping, 0 stopped, 0 zombie<br>
%Cpu(s): 12.5 us, 3.2 sy, 0.0 ni, 84.1 id, 0.2 wa, 0.0 hi, 0.0 si, 0.0 st<br>
MiB Mem : 7936.2 total, 1205.8 free, 4532.1 used, 2198.3 buff/cache<br>
<br>
PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND<br>
1234 root      20   0  156780  45632  12345 R  25.0   0.6   0:15.23 java<br>
5678 mysql     20   0 1234567 234567  45678 S  15.2   2.9   1:23.45 mysqld<br>
</div>`,
      correct: true
    },
    'ps aux': {
      content: `<div style="color: #00ff00;">
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND<br>
root         1  0.0  0.1  19356  1234 ?        Ss   Dec01   0:01 /sbin/init<br>
root      1234  2.5  5.7 156780 45632 ?        Sl   14:15   0:15 java -jar app.jar<br>
mysql     5678  1.5  2.9 1234567 234567 ?      Sl   Dec01   1:23 /usr/sbin/mysqld<br>
</div>`,
      correct: true
    },
    'df -h': {
      content: `<div style="color: #00ff00;">
Filesystem      Size  Used Avail Use% Mounted on<br>
/dev/sda1        20G  12G  7.2G  63% /<br>
/dev/sda2       100G  45G   50G  48% /home<br>
tmpfs           3.9G     0  3.9G   0% /dev/shm<br>
</div>`,
      correct: true
    },
    'free -m': {
      content: `<div style="color: #00ff00;">
              total        used        free      shared  buff/cache   available<br>
Mem:           7936        4532        1206         123        2198        3204<br>
Swap:          2047           0        2047<br>
</div>`,
      correct: true
    },
    'netstat -tulpn': {
      content: `<div style="color: #00ff00;">
Active Internet connections (only servers)<br>
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name<br>
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd<br>
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      5678/nginx<br>
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      9012/mysqld<br>
</div>`,
      correct: true
    }
  }

  return commands[command] || {
    content: `<div style="color: #ff6b6b;">bash: ${command}: command not found</div>`,
    correct: false
  }
}

const insertCommand = (command) => {
  currentCommand.value = command
}

const getScoreColor = (score) => {
  if (score >= 80) return '#52c41a'
  if (score >= 60) return '#faad14'
  return '#ff4d4f'
}

const getSkillLevel = (score) => {
  if (score >= 90) return '优秀'
  if (score >= 80) return '良好'
  if (score >= 60) return '合格'
  return '待提高'
}

const updateCompletedQuestions = () => {
  let completed = 0
  if (processResult.value) completed++
  if (scenarioQuestions.value.some(q => q.result)) completed++
  if (commandStats.total > 0) completed++
  completedQuestions.value = completed
}

const exportResult = () => {
  const result = {
    totalScore: totalScore.value,
    processScore: processScore.value,
    scenarioScore: scenarioScore.value,
    commandScore: commandScore.value,
    commandAccuracy: commandAccuracy.value,
    timestamp: new Date().toISOString()
  }

  const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ops-exam-result-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const restartExam = () => {
  // 重置所有数据
  resetProcessOrder()
  scenarioQuestions.value.forEach(q => {
    q.answer = q.type === 'multiple' ? [] : null
    q.result = null
  })
  terminalHistory.value = [terminalHistory.value[0]]
  commandStats.correct = 0
  commandStats.total = 0
  scenarioScore.value = 0
  commandScore.value = 0
  completedQuestions.value = 0
  remainingTime.value = 3600
  activeSection.value = 'process'
}

const handleFaultResponse = () => {
  // 处理故障模拟响应
  faultSimulation.visible = false
}

const triggerFaultSimulation = () => {
  faultSimulation.visible = true
  faultSimulation.description = '检测到服务器磁盘空间不足，剩余空间仅5%，系统可能随时崩溃！'
  faultSimulation.solutions = [
    { id: 1, text: '立即清理临时文件和日志' },
    { id: 2, text: '扩容磁盘空间' },
    { id: 3, text: '重启服务器释放内存' },
    { id: 4, text: '迁移部分数据到其他服务器' }
  ]
  faultSimulation.selectedSolution = null
}

// 生命周期
onMounted(() => {
  // 随机选择5道场景决策题
  const shuffledScenarios = [...scenarioQuestionsBank].sort(() => Math.random() - 0.5)
  scenarioQuestions.value = shuffledScenarios.slice(0, 5).map(q => ({
    ...q,
    answer: q.type === 'multiple' ? [] : null,
    result: null
  }))

  // 随机选择1道命令行题目
  const randomCommandQuestion = commandQuestionsBank[Math.floor(Math.random() * commandQuestionsBank.length)]
  currentCommandQuestion.value = randomCommandQuestion

  // 更新总题目数
  totalQuestions.value = 1 + scenarioQuestions.value.length + 1 // 流程题 + 场景题 + 命令题

  // 打乱初始顺序
  processSteps.value = processSteps.value.sort(() => Math.random() - 0.5)

  // 启动计时器
  const timer = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      clearInterval(timer)
      // 时间到，自动提交
      setActiveSection('result')
    }
  }, 1000)

  // 随机触发故障模拟
  setTimeout(() => {
    if (Math.random() > 0.7) {
      triggerFaultSimulation()
    }
  }, 30000)
})
</script>

<style scoped>
.ops-exam-system {
  min-height: 100vh;
  background: #f5f7fa;
}

.header {
  background: white;
  border-bottom: 1px solid #e6e8eb;
  padding-top: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 600;
}

.title-icon {
  color: #3b82f6;
}

.exam-info {
  display: flex;
  gap: 16px;
}

.main-content {
  padding: 24px;
  height: 86.2vh;
}

.exam-container {
  display: flex;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.sidebar {
  width: 200px;
  flex-shrink: 0;
}

.content-area {
  padding-left: 20px;
  flex: 1;
}

.section {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.question-card {
  margin-bottom: 24px;
}

.drag-container {
  margin-top: 16px;
}

.drag-area h4 {
  margin-bottom: 16px;
  color: #374151;
}

.drag-list {
  min-height: 400px;
  padding: 16px;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  background: #f9fafb;
}

.drag-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: move;
  transition: all 0.2s;
  user-select: none;
}

.drag-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.drag-item.dragging {
  opacity: 0.5;
  transform: rotate(5deg);
}

.drag-item.correct {
  border-color: #10b981;
  background: #ecfdf5;
}

.drag-item.incorrect {
  border-color: #ef4444;
  background: #fef2f2;
}

.drag-handle {
  color: #9ca3af;
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}

.step-text {
  flex: 1;
  color: #374151;
}

.status-icon {
  font-size: 18px;
}

.status-icon.correct {
  color: #10b981;
}

.status-icon.incorrect {
  color: #ef4444;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.result-alert {
  margin-top: 16px;
}

.score {
  margin-top: 8px;
  font-weight: 600;
}

.scenario-question {
  margin-bottom: 32px;
  padding: 24px;
  background: #f9fafb;
  border-radius: 8px;
}

.scenario-question h4 {
  margin-bottom: 8px;
  color: #1f2937;
}

.question-desc {
  margin-bottom: 16px;
  color: #6b7280;
  line-height: 1.6;
}

.option-item {
  display: block;
  margin-bottom: 12px;
  padding: 8px 0;
}

.question-result {
  margin-top: 16px;
}

.terminal-container {
  margin-top: 16px;
}

.terminal {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.terminal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #2d2d2d;
  border-bottom: 1px solid #404040;
}

.terminal-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.btn.red {
  background: #ff5f56;
}

.btn.yellow {
  background: #ffbd2e;
}

.btn.green {
  background: #27ca3f;
}

.terminal-title {
  color: #ffffff;
  font-size: 14px;
}

.terminal-body {
  height: 400px;
  padding: 16px;
  overflow-y: auto;
  background: #1a1a1a;
}

.terminal-entry {
  margin-bottom: 8px;
}

.command-line {
  color: #ffffff;
  font-size: 14px;
}

.prompt {
  color: #00ff00;
  font-weight: bold;
}

.command {
  color: #ffffff;
}

.command-output {
  margin-top: 4px;
  font-size: 13px;
  line-height: 1.4;
}

.current-line {
  display: flex;
  align-items: center;
  color: #ffffff;
  font-size: 14px;
}

.command-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-family: inherit;
  font-size: inherit;
  margin-left: 4px;
}

.command-hints {
  margin-top: 16px;
}

.command-hints h4 {
  margin-bottom: 12px;
  color: #374151;
}

.hint-tag {
  margin-right: 8px;
  margin-bottom: 8px;
  cursor: pointer;
}

.hint-tag:hover {
  background: #3b82f6;
  color: white;
}

.command-score {
  margin-top: 16px;
}

.result-overview {
  display: flex;
  gap: 48px;
  margin-bottom: 32px;
}

.score-circle {
  display: flex;
  align-items: center;
  justify-content: center;
}

.circle-progress {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(#3b82f6 calc(var(--progress) * 3.6deg), #e5e7eb 0);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.circle-progress::before {
  content: '';
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: white;
}

.score-text {
  position: relative;
  font-size: 24px;
  font-weight: bold;
  color: #1f2937;
}

.score-label {
  position: relative;
  font-size: 12px;
  color: #6b7280;
}

.result-details {
  flex: 1;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.detail-item h4 {
  width: 120px;
  margin: 0;
  color: #374151;
}

.score-value {
  min-width: 60px;
  text-align: right;
  font-weight: 600;
  color: #1f2937;
}

.result-analysis {
  margin-bottom: 32px;
}

.result-analysis h4 {
  margin-bottom: 16px;
  color: #1f2937;
}

.analysis-chart {
  background: #f9fafb;
  padding: 24px;
  border-radius: 8px;
}

.skill-item {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.skill-name {
  width: 80px;
  color: #374151;
  font-weight: 500;
}

.skill-level {
  min-width: 60px;
  text-align: right;
  font-weight: 600;
}

.fault-content {
  padding: 16px 0;
}

.fault-alert {
  margin-bottom: 24px;
}

.fault-content h4 {
  margin-bottom: 16px;
  color: #374151;
}

.solution-option {
  display: block;
  margin-bottom: 12px;
  padding: 8px 0;
}

/* 拖拽列表动画 */
.drag-list-move,
.drag-list-enter-active,
.drag-list-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.drag-list-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

.drag-list-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.drag-list-leave-active {
  position: absolute;
  width: calc(100% - 32px);
}

/* 拖拽项目增强动画 */
.drag-item {
  position: relative;
  transform-origin: center;
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.drag-item.dragging {
  opacity: 0.7;
  transform: rotate(3deg) scale(1.02);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.drag-item.drag-over {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  border-color: #3b82f6;
  background: #eff6ff;
}

.drag-item.drag-over::before {
  content: '';
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

.drag-item:hover:not(.dragging) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.drag-handle {
  transition: all 0.2s ease;
}

.drag-item:hover .drag-handle {
  color: #3b82f6;
  transform: scale(1.1);
}

.step-number {
  transition: all 0.2s ease;
}

.drag-item.dragging .step-number {
  background: #ef4444;
  transform: scale(1.1);
}

/* 命令行题目信息样式 */
.command-question-info {
  margin-bottom: 20px;
}

.question-alert {
  text-align: left;
}

.question-alert h4 {
  margin-bottom: 8px;
  color: #1f2937;
  font-size: 16px;
}

.question-alert p {
  margin-bottom: 12px;
  color: #6b7280;
  line-height: 1.5;
}

.command-hints-inline {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.hint-tag-small {
  font-size: 12px;
}

/* 增强拖拽区域视觉效果 */
.drag-list {
  position: relative;
  transition: all 0.3s ease;
}

.drag-list:hover {
  border-color: #3b82f6;
  background: #f8fafc;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .drag-item.dragging {
    transform: rotate(2deg) scale(1.01);
  }

  .command-hints-inline {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
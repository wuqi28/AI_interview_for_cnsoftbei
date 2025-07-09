<template>
  <div class="coding-platform">
    <!-- Header -->
    <div class="platform-header">
      <div class="header-left">
        <span class="title">算法编程面试题</span>
        <t-tag theme="primary" variant="light">python</t-tag>
      </div>
      <div class="timer">
        <t-icon name="time" />
        {{ formatTime(elapsedTime) }}
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Left Panel -->
      <div class="left-panel">
        <!-- Problem Selection -->
        <t-card class="problem-card" :bordered="false">
          <template #header>
            <div class="card-header">
              <span>题目描述</span>
              <t-tag :theme="getDifficultyTheme(currentProblem.difficulty)" variant="light">
                {{ currentProblem.difficulty }}
              </t-tag>
            </div>
          </template>

          <t-select v-model="selectedProblemId" @change="switchProblem" style="width: 100%; margin-bottom: 16px;">
            <t-option v-for="problem in problems" :key="problem.id" :value="problem.id"
              :label="`${problem.title} (${problem.difficulty})`" />
          </t-select>

          <h4 class="problem-title">{{ currentProblem.title }}</h4>
          <p class="problem-description">{{ currentProblem.description }}</p>

          <!-- Examples -->
          <div class="examples-section">
            <h5>示例:</h5>
            <div v-for="(example, idx) in currentProblem.examples" :key="idx" class="example-item">
              <div class="example-content">
                <div><strong>输入:</strong> {{ example.input }}</div>
                <div><strong>输出:</strong> {{ example.output }}</div>
                <div v-if="example.explanation" class="example-explanation">
                  <strong>解释:</strong> {{ example.explanation }}
                </div>
              </div>
            </div>
          </div>

          <!-- Constraints -->
          <div v-if="currentProblem.constraints" class="constraints-section">
            <h5>约束条件:</h5>
            <ul>
              <li v-for="constraint in currentProblem.constraints" :key="constraint">
                {{ constraint }}
              </li>
            </ul>
          </div>
        </t-card>

        <!-- Test Cases -->
        <t-card class="test-cases-card" :bordered="false">
          <template #header>
            <div class="card-header">
              <span>测试用例</span>
              <t-button theme="primary" size="small" :loading="loading" @click="runAllTests">
                运行所有测试
              </t-button>
            </div>
          </template>

          <div class="test-cases-list">
            <div v-for="(testCase, idx) in currentProblem.testCases" :key="idx" class="test-case-item">
              <div class="test-case-header">
                <span>测试用例 {{ idx + 1 }}</span>
                <t-button theme="success" size="small" :loading="loading" @click="runSingleTest(idx)">
                  运行
                </t-button>
              </div>

              <div class="test-case-content">
                <div><strong>输入:</strong> {{ testCase.input }}</div>
                <div><strong>期望输出:</strong> {{ testCase.expected }}</div>

                <div v-if="testResults[idx]" class="test-result">
                  <t-alert :theme="testResults[idx].status === 'passed' ? 'success' : 'error'"
                    :message="`${testResults[idx].status === 'passed' ? '✓ 通过' : '✗ 失败'} (${testResults[idx].time}ms)`" />
                  <div class="result-output">
                    <strong>实际输出:</strong> {{ testResults[idx].output }}
                  </div>
                  <div v-if="testResults[idx].error" class="result-error">
                    <strong>错误:</strong> {{ testResults[idx].error }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </t-card>

        <!-- Execution Results -->
        <t-card class="results-card" :bordered="false">
          <template #header>
            <span>运行结果</span>
          </template>

          <div v-if="!hasResults" class="no-results">
            <div class="empty-icon">🤖</div>
            <div>暂无数据</div>
            <div class="empty-hint">点击运行代码查看结果</div>
          </div>

          <div v-else class="results-summary">
            <div class="summary-item">
              <span>通过率:</span>
              <t-tag :theme="passRate === 100 ? 'success' : 'warning'">
                {{ passRate }}%
              </t-tag>
            </div>
            <div class="summary-item">
              <span>平均用时:</span>
              <span>{{ avgTime }}ms</span>
            </div>
            <div class="summary-item">
              <span>代码长度:</span>
              <span>{{ code.length }} 字符</span>
            </div>
          </div>
        </t-card>
      </div>

      <!-- Right Panel -->
      <div class="right-panel">
        <div class="editor-header">
          <span>代码编辑器</span>
          <t-select v-model="selectedLanguage" style="width: 120px;">
            <t-option value="python" label="Python" />
          </t-select>
        </div>

        <!-- Custom Code Editor -->
        <div class="code-editor-wrapper">
          <div class="code-editor">
            <div class="line-numbers">
              <div v-for="n in lineCount" :key="n" class="line-number">
                {{ n }}
              </div>
            </div>
            <div class="code-input-container">
              <pre class="code-highlight" v-html="highlightedCode"></pre>
              <textarea ref="codeTextarea" v-model="code" class="code-textarea" spellcheck="false"
                @input="handleCodeInput" @scroll="syncScroll" @keydown="handleKeydown"
                placeholder="在这里编写你的代码..."></textarea>
            </div>
          </div>
        </div>

        <div class="editor-actions">
          <t-space>
            <t-button theme="success" :loading="loading" @click="runCode" :disabled="!pyodideReady">
              <template #icon><t-icon name="play-circle" /></template>
              {{ loading ? '运行中...' : pyodideReady ? '运行代码' : 'Python环境加载中...' }}
            </t-button>
            <t-button theme="primary" :loading="loading" @click="submitCode" :disabled="!pyodideReady">
              <template #icon><t-icon name="check-circle" /></template>
              提交答案
            </t-button>
            <t-button theme="default" @click="resetCode">
              <template #icon><t-icon name="refresh" /></template>
              重置代码
            </t-button>
          </t-space>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

// State
const selectedProblemId = ref(1)
const selectedLanguage = ref('python')
const code = ref('')
const loading = ref(false)
const testResults = ref({})
const elapsedTime = ref(0)
const codeTextarea = ref(null)
const highlightedCode = ref('')
const pyodideReady = ref(false)

// Timer
let timerInterval = null

// Pyodide
let pyodide = null

// Problems data
const problems = ref([
  {
    id: 1,
    title: '两数之和',
    difficulty: '初级',
    description: '给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。',
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: '因为 nums[0] + nums[1] == 9，返回 [0, 1]。'
      }
    ],
    constraints: [
      '2 <= nums.length <= 10^4',
      '-10^9 <= nums[i] <= 10^9',
      '-10^9 <= target <= 10^9'
    ],
    testCases: [
      { input: '[2,7,11,15], 9', expected: '[0, 1]' },
      { input: '[3,2,4], 6', expected: '[1, 2]' },
      { input: '[3,3], 6', expected: '[0, 1]' }
    ],
    template: `def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    # 在这里编写你的代码
    pass

def test_solution():
    return twoSum`
  },
//   {
//     id: 2,
//     title: '最大子数组和',
//     difficulty: '中级',
//     description: '给你一个整数数组 nums，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。',
//     examples: [
//       {
//         input: '[-2,1,-3,4,-1,2,1,-5,4]',
//         output: '6',
//         explanation: '连续子数组 [4,-1,2,1] 的和最大，为 6。'
//       },
//       {
//         input: '[1]',
//         output: '1'
//       }
//     ],
//     constraints: [
//       '1 <= nums.length <= 10^5',
//       '-10^4 <= nums[i] <= 10^4'
//     ],
//     testCases: [
//       { input: '[-2,1,-3,4,-1,2,1,-5,4]', expected: '6' },
//       { input: '[1]', expected: '1' },
//       { input: '[5,4,-1,7,8]', expected: '23' },
//       { input: '[-1]', expected: '-1' }
//     ],
//     template: `def maxSubArray(nums):
//     """
//     :type nums: List[int]
//     :rtype: int
//     """
//     # 在这里编写你的代码
//     pass

// def test_solution():
//     return maxSubArray`
//   },
//   {
//     id: 3,
//     title: '合并两个有序链表',
//     difficulty: '高级',
//     description: '将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。',
//     examples: [
//       {
//         input: 'list1 = [1,2,4], list2 = [1,3,4]',
//         output: '[1,1,2,3,4,4]'
//       }
//     ],
//     constraints: [
//       '两个链表的节点数目范围是 [0, 50]',
//       '-100 <= Node.val <= 100'
//     ],
//     testCases: [
//       { input: '[1,2,4], [1,3,4]', expected: '[1,1,2,3,4,4]' },
//       { input: '[], []', expected: '[]' },
//       { input: '[], [0]', expected: '[0]' }
//     ],
//     template: `class ListNode:
//     def __init__(self, val=0, next=None):
//         self.val = val
//         self.next = next

// def mergeTwoLists(list1, list2):
//     """
//     :type list1: ListNode
//     :type list2: ListNode
//     :rtype: ListNode
//     """
//     # 在这里编写你的代码
//     pass

// def test_solution():
//     return mergeTwoLists`
//   }
])

// Computed
const currentProblem = computed(() => {
  return problems.value.find(p => p.id === selectedProblemId.value) || problems.value[0]
})

const hasResults = computed(() => {
  return Object.keys(testResults.value).length > 0
})

const passRate = computed(() => {
  const results = Object.values(testResults.value)
  if (results.length === 0) return 0
  const passed = results.filter(r => r.status === 'passed').length
  return Math.round((passed / results.length) * 100)
})

const avgTime = computed(() => {
  const results = Object.values(testResults.value)
  if (results.length === 0) return 0
  const totalTime = results.reduce((sum, r) => sum + r.time, 0)
  return Math.round(totalTime / results.length)
})

const lineCount = computed(() => {
  if (!code.value || typeof code.value !== 'string') return 1
  return Math.max(1, code.value.split('\n').length)
})

// Methods
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const getDifficultyTheme = (difficulty) => {
  switch (difficulty) {
    case '初级': return 'success'
    case '中级': return 'warning'
    case '高级': return 'danger'
    default: return 'default'
  }
}

const startTimer = () => {
  timerInterval = setInterval(() => {
    elapsedTime.value++
  }, 1000)
}

// 加载 Pyodide
const loadPyodide = async () => {
  try {
    console.log('开始加载 Pyodide...')

    // 动态加载 Pyodide 脚本
    if (!window.loadPyodide) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'
      script.onload = async () => {
        console.log('Pyodide 脚本加载完成')
        pyodide = await window.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
        })
        pyodideReady.value = true
        console.log('Pyodide 初始化完成')
      }
      script.onerror = () => {
        console.error('Pyodide 脚本加载失败')
        // 使用模拟模式
        pyodideReady.value = true
        console.log('使用模拟模式')
      }
      document.head.appendChild(script)
    } else {
      pyodide = await window.loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
      })
      pyodideReady.value = true
      console.log('Pyodide 初始化完成')
    }
  } catch (error) {
    console.error('Pyodide 加载失败:', error)
    // 使用模拟模式
    pyodideReady.value = true
    console.log('使用模拟模式')
  }
}

// Python syntax highlighting - 加强参数检查
const highlightPython = (inputCode) => {
  // 严格的参数检查
  if (inputCode === null || inputCode === undefined || typeof inputCode !== 'string') {
    console.warn('highlightPython: 无效的输入参数', inputCode)
    return ''
  }

  // 如果是空字符串，直接返回
  if (inputCode === '') {
    return ''
  }

  try {
    const keywords = ['def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'break', 'continue', 'pass', 'and', 'or', 'not', 'in', 'is', 'lambda', 'global', 'nonlocal']
    const builtins = ['True', 'False', 'None', 'int', 'str', 'list', 'dict', 'tuple', 'set', 'len', 'range', 'print', 'input', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr']

    let highlighted = inputCode
      // Escape HTML
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')

      // Comments
      // .replace(/(#.*$)/gm, '<span style="color: #6A9955;">$1</span>')

      // Strings
      .replace(/(".*?")/g, '<span style="color: #CE9178;">$1</span>')
      .replace(/('.*?')/g, '<span style="color: #CE9178;">$1</span>')
      .replace(/("""[\s\S]*?""")/g, '<span style="color: #CE9178;">$1</span>')
      .replace(/('''[\s\S]*?''')/g, '<span style="color: #CE9178;">$1</span>')

      // Numbers
      .replace(/\b(\d+\.?\d*)\b/g, '<span style="color: #B5CEA8;">$1</span>')

    // Keywords
    keywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g')
      highlighted = highlighted.replace(regex, `<span style="color: #569CD6;">${keyword}</span>`)
    })

    // Built-ins
    builtins.forEach(builtin => {
      const regex = new RegExp(`\\b${builtin}\\b`, 'g')
      highlighted = highlighted.replace(regex, `<span style="color: #4EC9B0;">${builtin}</span>`)
    })

    // Function names
    highlighted = highlighted.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()/g, '<span style="color: #DCDCAA;">$1</span>')

    // Type annotations
    highlighted = highlighted.replace(/:\s*([a-zA-Z_][a-zA-Z0-9_\[\]]*)/g, ': <span style="color: #4EC9B0;">$1</span>')

    return highlighted
  } catch (error) {
    console.error('语法高亮出错:', error)
    return inputCode || ''
  }
}

const updateHighlight = () => {
  try {
    highlightedCode.value = highlightPython(code.value)
  } catch (error) {
    console.error('更新高亮失败:', error)
    highlightedCode.value = code.value || ''
  }
}

const handleCodeInput = () => {
  updateHighlight()
}

const syncScroll = () => {
  const textarea = codeTextarea.value
  const highlight = document.querySelector('.code-highlight')
  const lineNumbers = document.querySelector('.line-numbers')

  if (textarea && highlight && lineNumbers) {
    highlight.scrollTop = textarea.scrollTop
    highlight.scrollLeft = textarea.scrollLeft
    lineNumbers.scrollTop = textarea.scrollTop
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    const start = e.target.selectionStart
    const end = e.target.selectionEnd
    const value = e.target.value

    e.target.value = value.substring(0, start) + '    ' + value.substring(end)
    e.target.selectionStart = e.target.selectionEnd = start + 4

    code.value = e.target.value
    updateHighlight()
  }
}

const switchProblem = () => {
  testResults.value = {}
  code.value = currentProblem.value.template
  updateHighlight()
}

const runCode = async () => {
  if (!pyodideReady.value) {
    alert('Python 环境还在加载中，请稍后再试')
    return
  }
  await runAllTests()
}

// 模拟运行单个测试用例
const runSingleTest = async (testIndex) => {
  if (!pyodideReady.value) {
    alert('Python 环境还在加载中，请稍后再试')
    return
  }

  loading.value = true
  const testCase = currentProblem.value.testCases[testIndex]

  try {
    let output = ''
    let error = ''
    const startTime = performance.now()

    if (pyodide) {
      // 使用真实的 Pyodide
      try {
        await pyodide.runPythonAsync(code.value)

        if (selectedProblemId.value === 1) {
          output = await pyodide.runPythonAsync(`str(test_solution()(${testCase.input}))`)
        } else if (selectedProblemId.value === 2) {
          const [nums, target] = testCase.input.split(', ')
          output = await pyodide.runPythonAsync(`str(test_solution()(${nums}, ${target}))`)
        } else {
          output = await pyodide.runPythonAsync(`str(test_solution()(${testCase.input}))`)
        }
      } catch (e) {
        error = e.toString()
      }
    } else {
      // 模拟模式
      await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200))

      // 简单的模拟逻辑
      if (code.value.includes('pass') || code.value.trim() === '') {
        error = 'NotImplementedError: 请实现你的解决方案'
      } else {
        // 随机生成结果用于演示
        const random = Math.random()
        if (random > 0.7) {
          output = testCase.expected // 正确答案
        } else if (random > 0.4) {
          output = 'wrong_answer' // 错误答案
        } else {
          error = 'RuntimeError: 代码执行出错'
        }
      }
    }

    const endTime = performance.now()
    const executionTime = Math.round(endTime - startTime)

    const status = output === testCase.expected ? 'passed' : 'failed'

    testResults.value = {
      ...testResults.value,
      [testIndex]: {
        output,
        error,
        time: executionTime,
        status
      }
    }
  } catch (e) {
    testResults.value = {
      ...testResults.value,
      [testIndex]: {
        output: '',
        error: e.toString(),
        time: 0,
        status: 'failed'
      }
    }
  } finally {
    loading.value = false
  }
}

const runAllTests = async () => {
  if (!pyodideReady.value) {
    alert('Python 环境还在加载中，请稍后再试')
    return
  }

  loading.value = true
  testResults.value = {}

  for (let i = 0; i < currentProblem.value.testCases.length; i++) {
    await runSingleTest(i)
  }

  loading.value = false
}

const submitCode = async () => {
  await runAllTests()
  loading.value = true
  if (passRate.value === 100) {
    MessagePlugin.success('🎉 恭喜！所有测试用例都通过了！')
  } else {
    MessagePlugin.error(`提交未通过全部测试，通过率：${passRate.value}%`)
  }
  setTimeout(() => {
    router.push('/report')
  }, 2000)
}

const resetCode = () => {
  code.value = currentProblem.value.template
  testResults.value = {}
  updateHighlight()
}

// Lifecycle
onMounted(async () => {
  // 首先设置初始代码
  code.value = currentProblem.value.template || ''

  // 等待 DOM 更新后再更新高亮
  await nextTick()
  updateHighlight()

  // 开始加载 Pyodide
  loadPyodide()

  // 启动计时器
  startTimer()
})
</script>

<style scoped>
.coding-platform {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.platform-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.timer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: monospace;
  color: #666;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-panel {
  width: 45%;
  background: white;
  border-right: 1px solid #e5e5e5;
  overflow-y: auto;
  padding: 20px;
}

.right-panel {
  width: 55%;
  display: flex;
  flex-direction: column;
  background: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.problem-card,
.test-cases-card,
.results-card {
  margin-bottom: 20px;
}

.problem-title {
  margin: 0 0 12px 0;
  color: #333;
}

.problem-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.examples-section,
.constraints-section {
  margin-bottom: 20px;
}

.examples-section h5,
.constraints-section h5 {
  margin: 0 0 8px 0;
  color: #333;
}

.example-item {
  margin-bottom: 8px;
}

.example-content {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
}

.example-explanation {
  margin-top: 8px;
  color: #666;
}

.constraints-section ul {
  margin: 0;
  padding-left: 20px;
}

.constraints-section li {
  color: #666;
  font-family: monospace;
  font-size: 13px;
  margin-bottom: 4px;
}

.test-cases-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.test-case-item {
  border: 1px solid #e5e5e5;
  border-radius: 4px;
}

.test-case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-bottom: 1px solid #e5e5e5;
}

.test-case-content {
  padding: 12px;
  font-family: monospace;
  font-size: 13px;
}

.test-result {
  margin-top: 8px;
}

.result-output,
.result-error {
  margin-top: 4px;
}

.result-error {
  color: #d32f2f;
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-hint {
  font-size: 12px;
  color: #ccc;
  margin-top: 8px;
}

.results-summary {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #e5e5e5;
  background: #f8f9fa;
}

.code-editor-wrapper {
  flex: 1;
  background: rgb(30, 30, 30);
  overflow: hidden;
}

.code-editor {
  display: flex;
  height: 100%;
  min-height: 400px;
}

.line-numbers {
  background: rgb(25, 25, 25);
  color: #858585;
  padding: 12px 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  text-align: right;
  user-select: none;
  border-right: 1px solid #404040;
  overflow: hidden;
  width: 50px;
  flex-shrink: 0;
}

.line-number {
  height: 21px;
}

.code-input-container {
  flex: 1;
  position: relative;
  overflow: auto;
}

.code-highlight {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 12px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #D4D4D4;
  white-space: pre;
  overflow: auto;
  pointer-events: none;
  z-index: 1;
  margin: 0;
}

.code-textarea {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  padding: 12px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  background: transparent;
  color: transparent;
  caret-color: #D4D4D4;
  border: none;
  outline: none;
  resize: none;
  white-space: pre;
  overflow: auto;
  z-index: 2;
}

.code-textarea::placeholder {
  color: #666;
}

.code-textarea::selection {
  background: rgba(173, 214, 255, 0.15);
}

.editor-actions {
  padding: 16px 20px;
  border-top: 1px solid #e5e5e5;
  background: #f8f9fa;
}

/* Scrollbar styles */
.code-highlight::-webkit-scrollbar,
.code-textarea::-webkit-scrollbar,
.line-numbers::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.code-highlight::-webkit-scrollbar-track,
.code-textarea::-webkit-scrollbar-track,
.line-numbers::-webkit-scrollbar-track {
  background: rgb(25, 25, 25);
}

.code-highlight::-webkit-scrollbar-thumb,
.code-textarea::-webkit-scrollbar-thumb,
.line-numbers::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 6px;
}

.code-highlight::-webkit-scrollbar-thumb:hover,
.code-textarea::-webkit-scrollbar-thumb:hover,
.line-numbers::-webkit-scrollbar-thumb:hover {
  background: #777;
}
</style>
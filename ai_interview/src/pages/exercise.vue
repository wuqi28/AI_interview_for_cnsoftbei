<template>
  <div class="exercise-page">
    <div style="margin-bottom: 20px;">
      <t-breadcrumb>
        <t-breadcrumb-item to="/">首页</t-breadcrumb-item>
        <t-breadcrumb-item>个性化问答题推荐</t-breadcrumb-item>
      </t-breadcrumb>
    </div>
    <t-layout class="app-layout">
      <!-- Content 区域 -->
      <t-content class="app-content">
        <div class="content-container">
          <!-- 筛选面板 -->
          <FilterPanel :filters="filters" :is-loading="isLoading" @update-filters="handleFiltersUpdate"
            @generate-questions="handleGenerateQuestions" />

          <!-- 题目展示区域 -->
          <div class="questions-section">
            <t-divider>
              <template #content>
                <t-space>
                  <span>题目列表</span>
                  <t-tag v-if="filters.knowledgePoints.length > 0" theme="primary" size="small">
                    已选择 {{ filters.knowledgePoints.length }} 个知识点
                  </t-tag>
                  <t-tag v-if="questions.length > 0" theme="primary" size="small">
                    共 {{ questions.length }} 道题目
                  </t-tag>
                  <t-button v-if="questions.length > 0" theme="danger" variant="text" size="small"
                    @click="clearAllQuestions" :disabled="isLoading">
                    清空所有题目
                  </t-button>
                </t-space>
              </template>
            </t-divider>

            <!-- 题目列表 - 自适应布局 -->
            <div class="questions-container">
              <!-- 已有题目 -->
              <QuestionPanel v-for="(question, index) in questions"
                :key="`question-${index}-${question.title.slice(0, 10)}`" :question="question"
                :question-number="index + 1" class="question-item" />

              <!-- 加载状态显示在已有题目下方 -->
              <div v-if="isLoading" class="loading-state">
                <t-loading size="large" text="正在生成题目，请稍候..." />
                <p class="loading-tip">
                  {{ questions.length > 0 ? '正在追加新题目...' : 'AI正在根据您的筛选条件生成个性化题目' }}
                </p>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-if="!isLoading && questions.length === 0 && !hasGenerated" class="empty-state">
              <t-empty description="请设置筛选条件并点击生成题目按钮开始">
                <template #image>
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                    <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                    <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                </template>
              </t-empty>
            </div>

            <div v-if="!isLoading && questions.length === 0 && hasGenerated" class="empty-state">
              <t-empty description="没有生成到符合条件的题目，请调整筛选条件重新生成" />
            </div>
          </div>
        </div>
      </t-content>
    </t-layout>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import QuestionPanel from '@/components/QuestionPanel.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import { generateQuestions } from '@/modules/backApi.js'

// 状态管理
const isLoading = ref(false)
const hasGenerated = ref(false)
const questions = ref([])
const generationCount = ref(0) // 记录生成批次

// 筛选条件
const filters = reactive({
  questionCount: 10,
  position: '',
  difficulty: '',
  knowledgePoints: [],
  resume: ''
})

// 筛选器更新
const handleFiltersUpdate = (newFilters) => {
  Object.assign(filters, newFilters)
}

// 生成题目
const handleGenerateQuestions = async () => {
  if (isLoading.value) {
    MessagePlugin.warning('正在生成题目中，请稍候...')
    return
  }

  isLoading.value = true
  hasGenerated.value = true

  try {
    const generatedQuestions = await generateQuestions(filters)

    if (generatedQuestions.length > 0) {
      questions.value.push(...generatedQuestions)
      generationCount.value += 1

      MessagePlugin.success(`成功生成 ${generatedQuestions.length} 道新题目，当前共 ${questions.value.length} 道题目`)
    } else {
      MessagePlugin.warning('没有生成到题目，请调整筛选条件重试')
    }
  } catch (error) {
    MessagePlugin.error(`生成题目失败: ${error.message}`)
    console.error('Generate questions error:', error)
  } finally {
    isLoading.value = false
  }
}

// 清空题目
const clearAllQuestions = () => {
  questions.value = []
  generationCount.value = 0
  hasGenerated.value = false
  MessagePlugin.info('已清空所有题目')
}
</script>

<style scoped>
.exercise-page {
  background-color: rgb(245, 247, 250);
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #0052d9 0%, #003ba3 100%);
  padding: 0;
  box-shadow: 0 2px 12px rgba(0, 82, 217, 0.2);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.app-content {
  background-color: rgb(245, 247, 250);
  min-height: calc(100vh - 64px);
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
}

.questions-section {
  margin-top: 16px;
}

/* 自适应题目容器布局 */
.questions-container {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  /* 最小间距 */
}

.question-item {
  margin: 0;
  /* 移除默认边距 */
}

/* 加载状态样式 - 现在显示在题目下方 */
.loading-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  gap: 8px;
  background-color: rgba(248, 250, 252, 0.8);
  border-radius: 8px;
  border: 1px dashed #d9e1e8;
  margin: 8px 0;
}

.loading-tip {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 40px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-content {
    padding: 12px;
  }

  .header-content {
    padding: 0 16px;
    flex-direction: column;
    height: auto;
    padding-top: 12px;
    padding-bottom: 12px;
    gap: 8px;
  }

  .header-title {
    font-size: 20px;
  }

  .questions-section {
    margin-top: 12px;
  }

  .questions-container {
    gap: 6px;
    /* 移动端更小的间距 */
  }

  .loading-state {
    padding: 16px 0;
  }

  .empty-state {
    padding: 30px 0;
  }
}
</style>

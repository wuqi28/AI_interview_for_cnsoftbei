<template>
  <div class="page">
    <div style="margin-bottom: 20px;">
      <t-breadcrumb>
        <t-breadcrumb-item to="/">首页</t-breadcrumb-item>
        <t-breadcrumb-item>面试岗位习题库</t-breadcrumb-item>
      </t-breadcrumb>
    </div>

    <div class="page-header">
      <h1 class="page-title">面试岗位习题库</h1>
      <p class="page-subtitle">选择您的目标岗位，开始刷题之旅</p>
    </div>

    <div class="position-grid">
      <t-card 
        v-for="position in positions" 
        :key="position.key"
        class="position-card"
        hover
        @click="selectPosition(position.key)"
      >
        <div class="card-content">
          <div class="card-icon" :style="{ backgroundColor: position.color }">
            <t-icon :name="position.icon" size="32px" />
          </div>
          <h3 class="card-title">{{ position.title }}</h3>
          <p class="card-description">{{ position.description }}</p>
          <div class="card-stats">
            <div class="stat-item">
              <span class="stat-number">{{ position.questionCount }}</span>
              <span class="stat-label">道题目</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ position.difficulty }}</span>
              <span class="stat-label">难度</span>
            </div>
          </div>
          <t-button 
            theme="primary" 
            variant="outline"
            block
            class="enter-button"
            @click.stop="selectPosition(position.key)"
          >
            开始刷题
            <template #suffix>
              <t-icon name="chevron-right" />
            </template>
          </t-button>
        </div>
      </t-card>
    </div>

    <div class="stats-section">
      <t-card class="stats-card">
        <div class="stats-grid">
          <div class="stat-block">
            <div class="stat-value">{{ totalQuestions }}</div>
            <div class="stat-desc">总题目数</div>
          </div>
          <div class="stat-block">
            <div class="stat-value">3</div>
            <div class="stat-desc">岗位类型</div>
          </div>
        </div>
      </t-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectPosition = (positionKey) => {
  const routeMap = {
    'programming-panel': '/programming',
    'operation-and-maintenance-panel': '/operation',
    'product-panel': '/product'
  }
  const targetRoute = routeMap[positionKey]
  if (targetRoute) router.push(targetRoute)
}

const positions = ref([
  {
    key: 'programming-panel',
    title: '算法编程',
    description: '涵盖数据结构、算法设计、编程实现等核心技能，助你在技术面试中脱颖而出',
    icon: 'code',
    color: '#0052D9',
    questionCount: 424,
    difficulty: '低-中-高'
  },
  {
    key: 'operation-and-maintenance-panel',
    title: '运维测试',
    description: '包含系统运维、自动化测试、性能优化等实战题目，提升运维技术水平',
    icon: 'setting',
    color: '#00A870',
    questionCount: 358,
    difficulty: '低-中-高'
  },
  {
    key: 'product-panel',
    title: '产品岗位',
    description: '产品设计、用户体验、需求分析等产品经理必备技能全覆盖，助你在产品岗位面试中脱颖而出',
    icon: 'chart-bubble',
    color: '#E37318',
    questionCount: 175,
    difficulty: '低-中-高'
  }
])

const totalQuestions = computed(() => {
  return positions.value.reduce((total, position) => total + position.questionCount, 0)
})
</script>

<style scoped>
.page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 20px 0;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0;
  font-weight: 400;
}

.position-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.position-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.position-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.card-content {
  padding: 32px 24px;
  text-align: center;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.card-description {
  color: #6b7280;
  line-height: 1.6;
  margin: 0 0 24px 0;
  font-size: 0.95rem;
}

.card-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 24px;
  padding: 16px 0;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.enter-button {
  margin-top: 8px;
  height: 44px;
  font-weight: 500;
}

.stats-section {
  margin-bottom: 40px;
}

.stats-card {
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 24px;
  padding: 32px;
}

.stat-block {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.stat-desc {
  color: #6b7280;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .page {
    padding: 16px;
  }
  .page-title {
    font-size: 2rem;
  }
  .position-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .card-content {
    padding: 24px 20px;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>

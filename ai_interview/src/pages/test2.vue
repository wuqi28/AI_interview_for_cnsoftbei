<template>
  <div class="interview-progress">
    <t-steps :current="currentStep" layout="horizontal" style="width: 100%;">
      <t-step-item
        v-for="(step, index) in stepList"
        :key="index"
        :title="`第 ${index + 1} 轮 ${step.label}`"
      >
        <template #icon>
          <div
            class="custom-dot"
            :style="{ backgroundColor: typeColorMap[step.type] || '#ccc' }"
          ></div>
        </template>
      </t-step-item>
    </t-steps>

    <!-- <div style="margin-top: 24px; text-align: center">
      <t-button theme="primary" @click="nextStep" :disabled="currentStep >= stepList.length">
        下一轮问答
      </t-button>
    </div> -->
  </div>
</template>

<script setup>
// ✅ 原始类型 → 显示颜色
const typeColorMap = {
  "专业技能测试": "#0052D9",
  "简历深挖与项目分析": "#FAAD14",
  "情景模拟": "#52C41A",
  "综合问答": "#722ED1"
}

// ✅ 原始类型 → 简化展示名
const typeAliasMap = {
  "专业技能测试": "专业技能",
  "简历深挖与项目分析": "简历深挖",
  "情景模拟": "情景模拟",
  "综合问答": "综合问答"
}

const rawTypes = [
  "专业技能测试", "专业技能测试",
  "简历深挖与项目分析", "简历深挖与项目分析",
  "情景模拟", "综合问答"
]

// ✅ 生成步骤列表（含原始类型和映射后的 label）
const stepList = rawTypes.map(type => ({
  type,
  label: typeAliasMap[type] || type
}))

const currentStep = ref(0)

const nextStep = () => {
  if (currentStep.value < stepList.length) {
    currentStep.value++
  }
}
</script>

<style scoped>
.custom-dot {
  margin-top: 4px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
}

.interview-progress {
  width: 100%;
  box-sizing: border-box;
}
</style>

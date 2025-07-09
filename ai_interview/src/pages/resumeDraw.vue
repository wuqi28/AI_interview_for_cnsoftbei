<template>
  <div class="resume-profile">
    <!-- 页面标题 -->
    <div class="page-header">
      <t-breadcrumb>
        <t-breadcrumb-item>首页</t-breadcrumb-item>
        <t-breadcrumb-item to="/resume">AI简历生成</t-breadcrumb-item>
        <t-breadcrumb-item>简历画像</t-breadcrumb-item>
      </t-breadcrumb>
      <h1 class="page-title">简历画像分析</h1>
    </div>

    <!-- 基本信息卡片 -->
    <t-card class="basic-info-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <t-icon name="user" />
          <span>基本信息</span>
        </div>
      </template>
      
      <div class="basic-info-content">
        <div class="avatar-section">
          <t-avatar size="large" :hide-on-load-failed="false">
            {{ profileData?.result?.name?.charAt(0) || 'U' }}
          </t-avatar>
          <div class="name-section">
            <h2>{{ profileData?.result?.name || '未知' }}</h2>
            <div class="tags">
              <t-tag theme="primary" variant="light">{{ profileData?.result?.gender || '未知' }}</t-tag>
              <t-tag theme="success" variant="light">{{ profileData?.result?.age || '未知' }}岁</t-tag>
              <t-tag theme="warning" variant="light">{{ profileData?.result?.degree || '未知' }}</t-tag>
            </div>
          </div>
        </div>
        
        <div class="info-grid">
          <div class="info-item">
            <span class="label">求职意向:</span>
            <span class="value">{{ profileData?.result?.expect_job || '未填写' }}</span>
          </div>
          <div class="info-item">
            <span class="label">毕业院校:</span>
            <span class="value">{{ profileData?.result?.college || '未填写' }}</span>
          </div>
          <div class="info-item">
            <span class="label">专业:</span>
            <span class="value">{{ profileData?.result?.major || '未填写' }}</span>
          </div>
          <div class="info-item">
            <span class="label">工作经验:</span>
            <span class="value">{{ profileData?.result?.work_year || '0' }}年</span>
          </div>
          <div class="info-item">
            <span class="label">联系电话:</span>
            <span class="value">{{ profileData?.result?.phone || '未填写' }}</span>
          </div>
          <div class="info-item">
            <span class="label">邮箱:</span>
            <span class="value">{{ profileData?.result?.email || '未填写' }}</span>
          </div>
        </div>
      </div>
    </t-card>

    <!-- 薪资评估和能力雷达图 -->
    <div class="analysis-row">
      <t-card class="salary-card" :bordered="false">
        <template #header>
          <div class="card-header">
            <t-icon name="money-circle" />
            <span>薪资评估</span>
          </div>
        </template>
        
        <div class="salary-content">
          <div class="salary-main">
            <span class="salary-amount">¥{{ profileData?.eval?.salary || 0 }}</span>
            <span class="salary-unit">/月</span>
          </div>
          <div class="salary-range">
            <t-tag theme="success" size="large">{{ profileData?.profiler_result?.predicted_salary || '未评估' }}</t-tag>
          </div>
          <div class="salary-desc">基于技能和经验的薪资预测</div>
        </div>
      </t-card>

      <t-card class="radar-card" :bordered="false">
        <template #header>
          <div class="card-header">
            <t-icon name="chart-radar" />
            <span>能力雷达图</span>
          </div>
        </template>
        
        <div class="radar-chart" ref="radarChartRef"></div>
      </t-card>
    </div>

    <!-- 技能标签 -->
    <t-card class="skills-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <t-icon name="code" />
          <span>技能标签</span>
        </div>
      </template>
      
      <div class="skills-content">
        <div class="skill-category">
          <h4>前端技能</h4>
          <div class="skill-tags">
            <t-tag 
              v-for="skill in frontendSkills" 
              :key="skill.tag"
              :theme="getSkillTheme(skill.weight)"
              class="skill-tag"
            >
              {{ skill.tag }} ({{ skill.weight }})
            </t-tag>
          </div>
        </div>
        
        <div class="skill-category">
          <h4>后端技能</h4>
          <div class="skill-tags">
            <t-tag 
              v-for="skill in backendSkills" 
              :key="skill.tag"
              :theme="getSkillTheme(skill.weight)"
              class="skill-tag"
            >
              {{ skill.tag }} ({{ skill.weight }})
            </t-tag>
          </div>
        </div>

        <div class="skill-category">
          <h4>其他技能</h4>
          <div class="skill-tags">
            <t-tag 
              v-for="skill in otherSkills" 
              :key="skill.tag"
              theme="default"
              class="skill-tag"
            >
              {{ skill.tag }} ({{ skill.weight }})
            </t-tag>
          </div>
        </div>
      </div>
    </t-card>

    <!-- 项目经历 -->
    <t-card class="projects-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <t-icon name="folder" />
          <span>项目经历</span>
        </div>
      </template>
      
      <div class="projects-content">
        <t-timeline>
          <t-timeline-item 
            v-for="(project, index) in profileData?.result?.proj_exp_objs || []" 
            :key="index"
            :dot-color="getProjectDotColor(index)"
          >
            <template #dot>
              <t-icon name="laptop" />
            </template>
            
            <div class="project-item">
              <div class="project-header">
                <h4>{{ project.proj_name }}</h4>
                <t-tag theme="primary" variant="outline">{{ project.proj_position }}</t-tag>
                <span class="project-date">{{ project.start_date }} - {{ project.end_date }}</span>
              </div>
              <div class="project-content">
                <p>{{ project.proj_content }}</p>
                <div v-if="project.proj_resp" class="project-resp">
                  <strong>主要职责：</strong>
                  <p>{{ project.proj_resp }}</p>
                </div>
              </div>
            </div>
          </t-timeline-item>
        </t-timeline>
      </div>
    </t-card>

    <!-- 教育背景和证书 -->
    <div class="education-row">
      <t-card class="education-card" :bordered="false">
        <template #header>
          <div class="card-header">
            <t-icon name="education" />
            <span>教育背景</span>
          </div>
        </template>
        
        <div class="education-content">
          <div 
            v-for="(edu, index) in profileData?.result?.education_objs || []" 
            :key="index"
            class="education-item"
          >
            <div class="edu-header">
              <h4>{{ edu.edu_college }}</h4>
              <t-tag theme="success" variant="light">{{ edu.edu_degree }}</t-tag>
            </div>
            <div class="edu-details">
              <p><strong>专业：</strong>{{ edu.edu_major }}</p>
              <p><strong>时间：</strong>{{ edu.start_date }} - {{ edu.end_date }}</p>
              <p v-if="edu.edu_college_dept"><strong>院系：</strong>{{ edu.edu_college_dept }}</p>
            </div>
          </div>
        </div>
      </t-card>

      <t-card class="certificates-card" :bordered="false">
        <template #header>
          <div class="card-header">
            <t-icon name="certificate" />
            <span>资格证书</span>
          </div>
        </template>
        
        <div class="certificates-content">
          <div 
            v-for="(cert, index) in profileData?.result?.all_cert_objs || []" 
            :key="index"
            class="cert-item"
          >
            <t-tag theme="warning" size="large">{{ cert.cert_name }}</t-tag>
          </div>
        </div>
      </t-card>
    </div>

    <!-- 风险提示 -->
    <t-card v-if="profileData?.profiler_result?.risks?.length" class="risks-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <t-icon name="error-circle" />
          <span>风险提示</span>
        </div>
      </template>
      
      <div class="risks-content">
        <t-alert 
          v-for="(risk, index) in profileData?.profiler_result?.risks" 
          :key="index"
          theme="warning"
          :message="risk.title"
          :description="risk.content"
          class="risk-alert"
        />
      </div>
    </t-card>

    <!-- 亮点总结 -->
    <t-card v-if="profileData?.profiler_result?.highlights?.length" class="highlights-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <t-icon name="star" />
          <span>亮点总结</span>
        </div>
      </template>
      
      <div class="highlights-content">
        <div 
          v-for="(highlight, index) in profileData?.profiler_result?.highlights" 
          :key="index"
          class="highlight-item"
        >
          <t-tag theme="success" variant="light" class="highlight-tag">{{ highlight.title }}</t-tag>
          <p>{{ highlight.content }}</p>
        </div>
      </div>
    </t-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import * as echarts from 'echarts';
import axiosLocal from '@/modules/axiosLocal';
import { useUserStore } from '@/stores/userStore';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const resumeName = route.query.name;

const profileData = ref(null);
const radarChartRef = ref(null);
let radarChart = null;

// 计算属性：分类技能
const frontendSkills = computed(() => {
  if (!profileData.value?.profiler_result?.skills?.job_skills) return [];
  return profileData.value.profiler_result.skills.job_skills
    .filter(skill => skill.type === '前端开发')
    .slice(0, 10);
});

const backendSkills = computed(() => {
  if (!profileData.value?.profiler_result?.skills?.job_skills) return [];
  return profileData.value.profiler_result.skills.job_skills
    .filter(skill => skill.type === '后端开发')
    .slice(0, 10);
});

const otherSkills = computed(() => {
  if (!profileData.value?.profiler_result?.skills?.job_skills) return [];
  return profileData.value.profiler_result.skills.job_skills
    .filter(skill => !['前端开发', '后端开发'].includes(skill.type))
    .slice(0, 15);
});

// 获取技能主题色
const getSkillTheme = (weight) => {
  if (weight >= 70) return 'success';
  if (weight >= 60) return 'warning';
  return 'default';
};

// 获取项目时间线颜色
const getProjectDotColor = (index) => {
  const colors = ['#0052d9', '#00a870', '#ed7b2f', '#e34d59', '#834ec2'];
  return colors[index % colors.length];
};

// 初始化雷达图
const initRadarChart = () => {
  if (!radarChartRef.value || !profileData.value?.profiler_result?.capacity) return;
  
  nextTick(() => {
    radarChart = echarts.init(radarChartRef.value);
    
    const capacity = profileData.value.profiler_result.capacity;
    const option = {
      title: {
        text: '能力评估',
        left: 'center',
        textStyle: {
          fontSize: 14,
          color: '#333'
        }
      },
      radar: {
        indicator: [
          { name: '教育背景', max: 100 },
          { name: '工作经验', max: 100 },
          { name: '管理能力', max: 100 },
          { name: '语言能力', max: 100 },
          { name: '社会经验', max: 100 },
          { name: '荣誉奖项', max: 100 }
        ],
        radius: '60%',
        splitNumber: 4,
        axisName: {
          color: '#666',
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            color: '#e6e6e6'
          }
        },
        splitArea: {
          areaStyle: {
            color: ['rgba(0, 82, 217, 0.1)', 'rgba(0, 82, 217, 0.05)']
          }
        }
      },
      series: [{
        type: 'radar',
        data: [{
          value: [
            capacity.education || 0,
            capacity.job_exp || 0,
            capacity.management || 0,
            capacity.language || 0,
            capacity.social_exp || 0,
            capacity.honor || 0
          ],
          name: '能力评估',
          areaStyle: {
            color: 'rgba(0, 82, 217, 0.2)'
          },
          lineStyle: {
            color: '#0052d9',
            width: 2
          },
          itemStyle: {
            color: '#0052d9'
          }
        }]
      }]
    };
    
    radarChart.setOption(option);
    
    // 响应式处理
    window.addEventListener('resize', () => {
      radarChart?.resize();
    });
  });
};

// 获取简历画像数据
const getResumeDraw = () => {
  if (!resumeName) {
    console.warn('缺少 name 参数');
    return;
  }

  axiosLocal.get('/resume/draw_resume', {
    params: {
      email: userStore.user.email,
      name: resumeName
    }
  }).then((res) => {
    console.log('简历分析结果：', res.data);
    profileData.value = res.data.data;
    
    // 初始化图表
    nextTick(() => {
      initRadarChart();
    });
  }).catch((error) => {
    console.error('获取简历画像失败：', error);
    // 使用模拟数据进行展示
    profileData.value = {
      "eval": { "salary": 11400 },
      "profiler_result": {
        "basic": [
          { "tag": "男", "type": "gender" },
          { "tag": "20-25岁", "type": "age" },
          { "tag": "无工作经验", "type": "experience" }
        ],
        "capacity": {
          "education": 10,
          "honor": 10,
          "job_exp": 32,
          "language": 20,
          "management": 10,
          "social_exp": 10
        },
        "skills": {
          "job_skills": [
            { "tag": "vue", "type": "前端开发", "weight": 82 },
            { "tag": "js", "type": "前端开发", "weight": 77 },
            { "tag": "redis", "type": "后端开发", "weight": 76 },
            { "tag": "ECharts", "type": "前端开发", "weight": 76 },
            { "tag": "MySQL", "type": "后端开发", "weight": 74 },
            { "tag": "Bootstrap", "type": "前端开发", "weight": 72 },
            { "tag": "SSM", "type": "后端开发", "weight": 72 },
            { "tag": "Flask", "type": "后端开发", "weight": 72 },
            { "tag": "SpringBoot", "type": "后端开发", "weight": 70 }
          ]
        },
        "predicted_salary": "10-20K",
        "risks": [
          {
            "content": "【专升本】：存在专升本嫌疑的教育经历",
            "title": "专升本",
            "type": "education"
          }
        ],
        "highlights": [
          {
            "content": "【很丰富】的【后端开发】经验：在redis、MySQL、SSM、Flask、SpringBoot等技能上有深入的理解",
            "title": "技能丰富",
            "type": "job_exp"
          }
        ]
      },
      "result": {
        "name": "吴奇",
        "gender": "男",
        "age": "22",
        "degree": "本科",
        "expect_job": "后端开发",
        "college": "武汉工程大学",
        "major": "计算机科学与技术",
        "phone": "18671505901",
        "email": "857592710@qq.com",
        "work_year": "0",
        "education_objs": [
          {
            "edu_college": "武汉工程大学",
            "edu_college_dept": "邮电与信息工程学院",
            "edu_degree": "本科",
            "edu_major": "计算机科学与技术",
            "start_date": "2022",
            "end_date": "2024"
          }
        ],
        "proj_exp_objs": [
          {
            "proj_name": "链家网数据可视化",
            "proj_position": "全栈",
            "start_date": "2023.02",
            "end_date": "2023.03",
            "proj_content": "实现了链家网的数据分析可视化，为客户提供购房向导"
          }
        ],
        "all_cert_objs": [
          { "cert_name": "计算机二级" },
          { "cert_name": "普通话二级乙等" }
        ]
      }
    };
    
    nextTick(() => {
      initRadarChart();
    });
  });
};

onMounted(() => {
  getResumeDraw();
});
</script>

<style scoped>
.resume-profile {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  margin: 16px 0 0 0;
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1f2937;
}

/* 基本信息卡片 */
.basic-info-card {
  margin-bottom: 24px;
}

.basic-info-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.name-section h2 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}

.tags {
  display: flex;
  gap: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item .label {
  font-weight: 500;
  color: #6b7280;
  min-width: 80px;
}

.info-item .value {
  color: #1f2937;
}

/* 分析行布局 */
.analysis-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
  margin-bottom: 24px;
}

/* 薪资卡片 */
.salary-content {
  text-align: center;
  padding: 20px 0;
}

.salary-main {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
  margin-bottom: 16px;
}

.salary-amount {
  font-size: 32px;
  font-weight: 700;
  color: #0052d9;
}

.salary-unit {
  font-size: 16px;
  color: #6b7280;
}

.salary-range {
  margin-bottom: 12px;
}

.salary-desc {
  color: #6b7280;
  font-size: 14px;
}

/* 雷达图 */
.radar-chart {
  height: 300px;
  width: 100%;
}

/* 技能卡片 */
.skills-card {
  margin-bottom: 24px;
}

.skills-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.skill-category h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  margin: 0;
}

/* 项目经历 */
.projects-card {
  margin-bottom: 24px;
}

.project-item {
  padding-left: 16px;
}

.project-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.project-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.project-date {
  color: #6b7280;
  font-size: 14px;
  margin-left: auto;
}

.project-content p {
  margin: 0 0 12px 0;
  color: #4b5563;
  line-height: 1.6;
}

.project-resp {
  margin-top: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.project-resp strong {
  color: #1f2937;
}

.project-resp p {
  margin: 8px 0 0 0;
}

/* 教育和证书行 */
.education-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.education-item {
  padding: 16px 0;
  border-bottom: 1px solid #e5e7eb;
}

.education-item:last-child {
  border-bottom: none;
}

.edu-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.edu-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.edu-details p {
  margin: 4px 0;
  color: #4b5563;
  font-size: 14px;
}

.certificates-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 风险提示 */
.risks-card {
  margin-bottom: 24px;
}

.risk-alert {
  margin-bottom: 12px;
}

.risk-alert:last-child {
  margin-bottom: 0;
}

/* 亮点总结 */
.highlights-card {
  margin-bottom: 24px;
}

.highlights-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.highlight-item {
  padding: 16px;
  background: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #0052d9;
}

.highlight-tag {
  margin-bottom: 8px;
}

.highlight-item p {
  margin: 0;
  color: #1f2937;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .analysis-row {
    grid-template-columns: 1fr;
  }
  
  .education-row {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .resume-profile {
    padding: 16px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .project-date {
    margin-left: 0;
  }
}
</style>

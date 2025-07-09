<template>
    <div class="video-recommendation-page">
        <div style="margin-bottom: 20px;">
            <t-breadcrumb>
                <t-breadcrumb-item to="/">首页</t-breadcrumb-item>
                <t-breadcrumb-item>学习资源智能推荐</t-breadcrumb-item>
            </t-breadcrumb>
        </div>
        <div class="content-container">
            <!-- TDesign风格的视频推荐设置面板 -->
            <div class="recommendation-panel">
                <!-- 面板头部 -->
                <div class="panel-header">
                    <div class="header-content">
                        <div class="title-section">
                            <h2 class="panel-title">
                                <t-icon name="video" class="title-icon" />
                                智能视频推荐
                            </h2>
                            <p class="panel-subtitle">基于AI的个性化学习资源匹配</p>
                        </div>
                        <div class="action-buttons">
                            <t-button variant="outline" @click="resetFilters" :disabled="isLoading">
                                <template #icon><t-icon name="refresh" /></template>
                                重置
                            </t-button>
                            <t-button theme="primary" @click="handleGenerateVideos" :loading="isLoading"
                                :disabled="filters.knowledgePoints.length === 0">
                                <template #icon><t-icon name="play-circle" /></template>
                                生成推荐
                            </t-button>
                        </div>
                    </div>
                </div>

                <!-- 模式选择卡片 -->
                <div class="mode-cards">
                    <t-card class="mode-card" :class="{ active: filters.mode === 'self-directed' }"
                        @click="selectMode('self-directed')" hover-shadow>
                        <div class="mode-content">
                            <div class="mode-icon">
                                <t-icon name="setting" />
                            </div>
                            <div class="mode-text">
                                <h3>自主探索</h3>
                                <p>自由选择学习方向和知识点</p>
                            </div>
                            <div class="mode-indicator">
                                <t-radio :checked="filters.mode === 'self-directed'" />
                            </div>
                        </div>
                    </t-card>

                    <t-card class="mode-card" :class="{ active: filters.mode === 'interview-driven' }"
                        @click="selectMode('interview-driven')" hover-shadow>
                        <div class="mode-content">
                            <div class="mode-icon">
                                <t-icon name="chart-bubble" />
                            </div>
                            <div class="mode-text">
                                <h3>智能分析</h3>
                                <p>基于面试表现精准推荐</p>
                            </div>
                            <div class="mode-indicator">
                                <t-radio :checked="filters.mode === 'interview-driven'" />
                            </div>
                        </div>
                    </t-card>
                </div>

                <!-- 配置区域 -->
                <div class="config-area">
                    <!-- 自主探索模式 -->
                    <div v-if="filters.mode === 'self-directed'" class="config-section">
                        <div class="section-title">
                            <h4>视频配置</h4>
                            <t-tag theme="primary" variant="light">自定义</t-tag>
                        </div>

                        <t-form layout="inline" class="form-container">
                            <t-row :gutter="[24, 16]">
                                <t-col :xs="24" :sm="12" :md="8">
                                    <t-form-item label="技术领域">
                                        <t-select v-model="filters.position" @change="handlePositionChange"
                                            :disabled="isLoading" placeholder="选择技术领域" clearable>
                                            <t-option value="前端工程师" label="前端工程师" />
                                            <t-option value="后端工程师" label="后端工程师" />
                                            <t-option value="人工智能-算法工程师" label="人工智能-算法工程师" />
                                            <t-option value="人工智能-计算机视觉工程师" label="人工智能-计算机视觉工程师" />
                                            <t-option value="人工智能-NLP工程师" label="人工智能-NLP工程师" />
                                            <t-option value="大数据-数据开发工程师" label="大数据-数据开发工程师" />
                                            <t-option value="大数据-数据分析师" label="大数据-数据分析师" />
                                            <t-option value="物联网-嵌入式工程师" label="物联网-嵌入式工程师" />
                                            <t-option value="物联网-物联网平台开发工程师" label="物联网-物联网平台开发工程师" />
                                            <t-option value="智能系统-智能制造工程师" label="智能系统-智能制造工程师" />
                                            <t-option value="智能系统-智能家居工程师" label="智能系统-智能家居工程师" />
                                            <t-option value="运维测试岗" label="运维测试岗" />
                                            <t-option value="产品岗" label="产品设计" />
                                        </t-select>
                                    </t-form-item>
                                </t-col>

                                <t-col :xs="24" :sm="12" :md="8">
                                    <t-form-item label="难度等级">
                                        <t-radio-group v-model="filters.difficulty" variant="default-filled">
                                            <t-radio-button value="初级">初级</t-radio-button>
                                            <t-radio-button value="中级">中级</t-radio-button>
                                            <t-radio-button value="高级">高级</t-radio-button>
                                            <t-radio-button value="随机">随机</t-radio-button>
                                        </t-radio-group>
                                    </t-form-item>
                                </t-col>
                            </t-row>

                            <t-row>
                                <t-col :span="24">
                                    <t-form-item label="知识点选择" v-if="availableKnowledgePoints.length">
                                        <div class="knowledge-selector">
                                            <div v-if="availableKnowledgePoints.length > 0" class="knowledge-grid">
                                                <t-tag v-for="point in availableKnowledgePoints" :key="point"
                                                    class="knowledge-chip"
                                                    :theme="filters.knowledgePoints.includes(point) ? 'primary' : 'default'"
                                                    :variant="filters.knowledgePoints.includes(point) ? 'dark' : 'outline'"
                                                    @click="toggleKnowledgePoint(point)" :disabled="isLoading">
                                                    <template #icon v-if="filters.knowledgePoints.includes(point)">
                                                        <t-icon name="check" />
                                                    </template>
                                                    {{ point }}
                                                </t-tag>
                                            </div>
                                            <t-empty v-else description="请先选择技术领域" image="default" />
                                        </div>
                                    </t-form-item>
                                </t-col>
                            </t-row>
                        </t-form>
                    </div>

                    <!-- 智能分析模式 -->
                    <div v-if="filters.mode === 'interview-driven'" class="config-section">
                        <div class="section-title">
                            <h4>面试记录分析</h4>
                            <t-tag theme="success" variant="light">AI驱动</t-tag>
                        </div>

                        <t-form class="form-container">
                            <t-form-item label="选择面试记录">
                                <t-select v-model="filters.selectedInterviewId" @change="handleInterviewRecordChange"
                                    :disabled="isLoading" placeholder="选择一次面试记录" clearable>
                                    <t-option v-for="record in interviewRecords" :key="record.id"
                                        :value="record.current_interview_id" :label="formatInterviewLabel(record)" />
                                </t-select>
                            </t-form-item>

                            <!-- 面试记录详情 -->
                            <div v-if="selectedInterviewRecord" class="interview-details">
                                <t-divider>面试详情</t-divider>
                                <t-descriptions :column="2" bordered>
                                    <t-descriptions-item label="公司">
                                        {{ parseInterviewId(selectedInterviewRecord.current_interview_id).company }}
                                    </t-descriptions-item>
                                    <t-descriptions-item label="岗位">
                                        {{ parseInterviewId(selectedInterviewRecord.current_interview_id).position }}
                                    </t-descriptions-item>
                                    <t-descriptions-item label="面试时间">
                                        {{ formatTime(selectedInterviewRecord.start_time) }}
                                    </t-descriptions-item>
                                    <t-descriptions-item label="面试时长">
                                        {{ parseFloat((selectedInterviewRecord.spend_time / 60).toFixed(1)) }}分钟
                                    </t-descriptions-item>
                                    <t-descriptions-item label="面试官">
                                        {{ selectedInterviewRecord.interviewer_name }}
                                    </t-descriptions-item>
                                    <t-descriptions-item label="面试风格">
                                        {{ selectedInterviewRecord.interview_style }}
                                    </t-descriptions-item>
                                </t-descriptions>
                            </div>
                        </t-form>
                    </div>

                    <!-- 已选择的知识点 -->
                    <div v-if="filters.knowledgePoints.length > 0" class="selected-knowledge">
                        <t-divider>
                            <template #content>
                                <t-space>
                                    <span>已选知识点</span>
                                    <t-tag theme="primary" size="small">{{ filters.knowledgePoints.length }}</t-tag>
                                </t-space>
                            </template>
                        </t-divider>
                        <t-space wrap>
                            <t-tag v-for="point in filters.knowledgePoints" :key="point" theme="primary" variant="light"
                                closable @close="removeKnowledgePoint(point)" :disabled="isLoading">
                                {{ point }}
                            </t-tag>
                        </t-space>
                    </div>
                </div>
            </div>

            <!-- 视频展示区域 - 恢复V4版本样式 -->
            <div class="videos-section">
                <t-divider>
                    <template #content>
                        <t-space>
                            <span>推荐视频</span>
                            <t-tag v-if="filters.knowledgePoints.length > 0" theme="primary" size="small">
                                已选择 {{ filters.knowledgePoints.length }} 个知识点
                            </t-tag>
                            <t-tag v-if="videoData.video && videoData.video.length > 0" theme="primary" size="small">
                                共 {{ videoData.video.length }} 个视频
                            </t-tag>
                            <t-button v-if="videoData.video && videoData.video.length > 0" theme="danger" variant="text"
                                size="small" @click="clearAllVideos" :disabled="isLoading">
                                清空所有视频
                            </t-button>
                        </t-space>
                    </template>
                </t-divider>

                <!-- 加载状态 -->
                <t-loading :loading="isLoading" text="正在生成推荐视频..." size="large" style="padding-top: 20px;">
                    <!-- 视频列表 -->
                    <div v-if="videoData.video && videoData.video.length > 0" class="video-container">
                        <div class="video-grid">
                            <div v-for="video in videoData.video" :key="video.bvid" class="video-card"
                                @click="selectVideo(video)">
                                <div class="video-thumbnail">
                                    <t-image :src="video.pic.startsWith('//') ? 'https:' + video.pic : video.pic"
                                        :alt="video.title" fit="cover" class="thumbnail-image"
                                        referrerpolicy="no-referrer" />
                                    <t-tag variant="dark" class="duration-badge">
                                        <!-- {{ formatDuration(video.duration) }} -->
                                        {{ video.duration }}
                                    </t-tag>
                                    <div class="play-overlay">
                                        <t-button shape="circle" theme="primary" size="large" class="play-button">
                                            <template #icon>
                                                <play-circle-filled-icon />
                                            </template>
                                        </t-button>
                                    </div>
                                </div>
                                <div class="video-info">
                                    <h3 class="video-title" :title="video.title">{{ video.title }}</h3>
                                    <p class="video-description" :title="video.description">{{ video.description }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 空状态 -->
                    <div v-if="!isLoading && (!videoData.video || videoData.video.length === 0) && !hasGenerated"
                        class="empty-state">
                        <t-empty description="请设置筛选条件并点击生成推荐视频按钮开始">
                            <template #image>
                                <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
                                    <path d="M15 10L11 12.5L15 15V10Z" stroke="currentColor" stroke-width="2"
                                        stroke-linecap="round" stroke-linejoin="round" />
                                    <path
                                        d="M17 6H3C1.89543 6 1 6.89543 1 8V16C1 17.1046 1.89543 18 3 18H17C18.1046 18 19 17.1046 19 16V8C19 6.89543 18.1046 6 17 6Z"
                                        stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" />
                                    <path d="M21 14V10L19 8V16L21 14Z" stroke="currentColor" stroke-width="2"
                                        stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                            </template>
                        </t-empty>
                    </div>

                    <div v-if="!isLoading && (!videoData.video || videoData.video.length === 0) && hasGenerated"
                        class="empty-state">
                        <t-empty description="没有找到符合条件的推荐视频，请调整筛选条件重新生成" />
                    </div>
                </t-loading>
            </div>
        </div>


        <t-dialog v-model:visible="showVideoModal" :header="selectedVideo?.title" width="90%" max-width="900px"
            :close-btn="true" :close-on-overlay-click="true" placement="center" class="video-dialog" @close="stopVideo">
            <div v-if="selectedVideo" class="video-modal-content">
                <div class="video-player">
                    <iframe ref="videoIframe" :src="videoSrc" allowfullscreen frameborder="0" title="视频播放器"></iframe>
                </div>
                <div class="video-details">
                    <t-space size="medium" class="video-meta">
                        <t-tag theme="default" variant="light">
                            <template #icon>
                                <time-icon />
                            </template>
                            <!-- 时长: {{ formatDuration(selectedVideo.duration) }} -->
                            时长: {{ selectedVideo.duration }}
                        </t-tag>
                        <t-tag theme="primary" variant="light">
                            <template #icon>
                                <video-icon />
                            </template>
                            {{ selectedVideo.bvid }}
                        </t-tag>
                    </t-space>
                    <p class="video-description-full">{{ selectedVideo.description }}</p>
                </div>
            </div>
        </t-dialog>
    </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import { useInterviewStore } from '@/stores/interviewStore'
import { useUserStore } from '@/stores/userStore'
import axiosLocal from '@/modules/axiosLocal'
import {
    PlayCircleFilledIcon,
    TimeIcon,
    VideoIcon
} from 'tdesign-icons-vue-next'

const interviewStore = useInterviewStore()
const userStore = useUserStore()

// 状态管理
const selectedVideo = ref(null)
const isLoading = ref(false)
const hasGenerated = ref(false)
const showVideoModal = ref(false)
const videoData = ref({ video: [] })
const videoIframe = ref(null)

// 筛选条件
const filters = reactive({
    mode: 'self-directed',
    selectedInterviewId: '',
    knowledgePoints: [],
    difficulty: '',
    position: '',
    videoCount: 10,
    resume: ''
})

// 知识点映射
const knowledgeMap = {
    '前端工程师': ['HTML', 'CSS', 'JavaScript', 'Vue.js', 'React', '前端工程化', '性能优化', 'TypeScript', 'Webpack', 'Node.js'],
    '后端工程师': ['Java', 'Python', 'Go', '数据库', 'Redis', '微服务', '消息队列', 'Spring', 'MySQL', 'Docker'],
    '人工智能-算法工程师': ['机器学习', '深度学习', '卷积神经网络', '自然语言处理', '推荐系统', '模型优化', 'TensorFlow', 'PyTorch', '数据标注'],
    '人工智能-计算机视觉工程师': ['图像处理', '目标检测', 'OpenCV', 'YOLO', '图像分割', 'GAN', '卷积神经网络'],
    '人工智能-NLP工程师': ['自然语言处理', '文本分类', '序列标注', 'BERT', 'Transformer', '情感分析', '信息抽取'],
    '大数据-数据开发工程师': ['Hadoop', 'Spark', 'Flink', 'Hive', 'Kafka', '数据仓库', 'ETL', 'SQL调优'],
    '大数据-数据分析师': ['数据可视化', '数据挖掘', '统计分析', 'Python', 'R', 'Tableau', 'PowerBI'],
    '物联网-嵌入式工程师': ['C语言', '嵌入式开发', 'ARM架构', 'RTOS', '硬件调试', '物联网协议', '传感器技术'],
    '物联网-物联网平台开发工程师': ['MQTT', 'CoAP', '物联网平台架构', '设备管理', '数据采集', '云平台对接'],
    '智能系统-智能制造工程师': ['PLC', 'SCADA', '工业机器人', '自动化控制', '工业以太网', '工业大数据'],
    '智能系统-智能家居工程师': ['智能硬件', '智能控制', 'ZigBee', '蓝牙', 'HomeKit', '智能场景设计'],
    '运维测试岗': ['Linux', 'Shell脚本', '网络基础', 'Docker', 'Kubernetes', 'CI/CD', '性能测试', '安全测试'],
    '产品岗': ['需求分析', '产品设计', 'Axure', '竞品分析', '用户调研', '数据驱动设计']
}

// 计算属性
const videoSrc = computed(() => {
    if (!selectedVideo.value) return ''
    return `https://player.bilibili.com/player.html?bvid=${selectedVideo.value.bvid}&autoplay=1`
})

const interviewRecords = computed(() => {
    return interviewStore.interview_record_list || []
})

const selectedInterviewRecord = computed(() => {
    if (!filters.selectedInterviewId) return null
    return interviewRecords.value.find(record =>
        record.current_interview_id === filters.selectedInterviewId
    )
})

const availableKnowledgePoints = computed(() => {
    return knowledgeMap[filters.position] || []
})

// 方法
const selectMode = (mode) => {
    filters.mode = mode
    if (mode === 'interview-driven') {
        filters.selectedInterviewId = ''
        filters.position = ''
        filters.difficulty = ''
        filters.knowledgePoints = []
    } else {
        filters.selectedInterviewId = ''
        filters.knowledgePoints = []
    }
}

const toggleKnowledgePoint = (point) => {
    const index = filters.knowledgePoints.indexOf(point)
    if (index > -1) {
        filters.knowledgePoints.splice(index, 1)
    } else {
        filters.knowledgePoints.push(point)
    }
}

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

const formatInterviewLabel = (record) => {
    const parsed = parseInterviewId(record.current_interview_id)
    return `${parsed.company} - ${parsed.position} (${formatTime(record.start_time)})`
}

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

const formatDuration = (seconds) => {
    const duration = parseInt(seconds)
    const hours = Math.floor(duration / 3600)
    const minutes = Math.floor((duration % 3600) / 60)
    const secs = duration % 60

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
}

const handleInterviewRecordChange = async () => {
    const selectedRecord = selectedInterviewRecord.value
    if (!selectedRecord) return

    const current_interview_id = selectedRecord.current_interview_id

    try {
        const reportRes = await axiosLocal.get('/interview/get_interview_report', {
            params: {
                email: userStore.user.email,
                current_interview_id: current_interview_id
            }
        })

        if (reportRes.data.code === 200) {
            const knowledgeNames = reportRes.data.data.knowledge_analysis.map(item => item.knowledge_name)
            filters.position = current_interview_id.split('-')[1]
            filters.knowledgePoints = knowledgeNames
            MessagePlugin.success(`已从面试报告中提取到 ${knowledgeNames.length} 个知识点`)
        }

        const resumeRes = await axiosLocal.get('/resume/get_resume_md', {
            params: {
                email: userStore.user.email,
                current_interview_id: current_interview_id
            }
        })

        if (resumeRes.data.code === 200) {
            filters.resume = resumeRes.data.data
            filters.difficulty = '随机'
        }
    } catch (error) {
        MessagePlugin.error('获取面试数据失败')
        console.error('Get interview data error:', error)
    }
}

const handlePositionChange = () => {
    filters.knowledgePoints = []
}

const removeKnowledgePoint = (point) => {
    const index = filters.knowledgePoints.indexOf(point)
    if (index > -1) {
        filters.knowledgePoints.splice(index, 1)
    }
}

const resetFilters = () => {
    filters.mode = 'self-directed'
    filters.selectedInterviewId = ''
    filters.position = ''
    filters.difficulty = ''
    filters.knowledgePoints = []
    filters.videoCount = 10
    filters.resume = ''
    videoData.value = { video: [] }
    hasGenerated.value = false
    MessagePlugin.info('已重置所有筛选条件')
}

const handleGenerateVideos = async () => {
    if (isLoading.value) {
        MessagePlugin.warning('正在生成视频中，请稍候...')
        return
    }

    if (filters.knowledgePoints.length === 0) {
        MessagePlugin.warning('请先选择知识点或选择面试记录')
        return
    }

    isLoading.value = true
    hasGenerated.value = true

    try {
        const knowledgePointsString = filters.knowledgePoints.join(',')
        await fetchVideoData(knowledgePointsString)

        if (videoData.value.video && videoData.value.video.length > 0) {
            MessagePlugin.success(`成功生成 ${videoData.value.video.length} 个推荐视频`)
        } else {
            MessagePlugin.warning('没有找到符合条件的推荐视频，请调整筛选条件重试')
        }
    } catch (error) {
        MessagePlugin.error(`生成推荐视频失败: ${error.message}`)
        console.error('Generate videos error:', error)
    } finally {
        isLoading.value = false
    }
}

const clearAllVideos = () => {
    videoData.value = { video: [] }
    hasGenerated.value = false
    MessagePlugin.info('已清空所有视频')
}

const selectVideo = (video) => {
    selectedVideo.value = video
    showVideoModal.value = true
}

const stopVideo = () => {
    if (videoIframe.value) {
        videoIframe.value.src = 'about:blank'
    }
    selectedVideo.value = null
}

const fetchVideoData = async (knowledgePoints) => {
    try {
        const response = await axiosLocal.post('/interview/generate_resource',
            { knowledgePoints },
            { headers: { "Content-Type": "application/json" } }
        )

        const responseText = response.data.data.outputs.text
        let cleanText = responseText.trim()

        if (cleanText.startsWith('\`\`\`json')) {
            cleanText = cleanText.slice(7).trim()
        } else if (cleanText.startsWith('\`\`\`')) {
            cleanText = cleanText.slice(3).trim()
        }

        if (cleanText.endsWith('\`\`\`')) {
            cleanText = cleanText.slice(0, -3).trim()
        }

        const parsedData = JSON.parse(cleanText)
        console.log(parsedData)
        videoData.value = parsedData
    } catch (error) {
        console.error('获取视频数据失败:', error)
        throw error
    }
}
</script>

<style scoped>
.video-recommendation-page {
    min-height: 100vh;
    /* background-color: var(--td-bg-color-page); */
    background-color: rgb(245, 247, 250);
    padding: 20px;
}

.content-container {
    max-width: 1400px;
    margin: 0 auto;
}

/* 推荐面板样式 */
.recommendation-panel {
    background: var(--td-bg-color-container);
    border-radius: var(--td-radius-large);
    box-shadow: var(--td-shadow-2);
    margin-bottom: 24px;
    border: 1px solid var(--td-border-level-1-color);
}

.panel-header {
    background: linear-gradient(135deg, var(--td-brand-color) 0%, var(--td-brand-color-8) 100%);
    padding: 24px;
    color: white;
    border-radius: var(--td-radius-large) var(--td-radius-large) 0 0;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.title-section {
    flex: 1;
}

.panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 24px;
    font-weight: 600;
    margin: 0 0 8px 0;
}

.title-icon {
    font-size: 24px;
}

.panel-subtitle {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
}

.action-buttons {
    display: flex;
    gap: 12px;
}

/* 模式选择卡片 */
.mode-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    padding: 24px;
    border-bottom: 1px solid var(--td-border-level-1-color);
}

.mode-card {
    cursor: pointer;
    transition: all var(--td-transition);
    border: 2px solid transparent;
}

.mode-card:hover {
    border-color: var(--td-brand-color);
}

.mode-card.active {
    border-color: var(--td-brand-color);
    background: var(--td-brand-color-1);
}

.mode-content {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
}

.mode-icon {
    width: 40px;
    height: 40px;
    background: var(--td-brand-color-1);
    border-radius: var(--td-radius-medium);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--td-brand-color);
    font-size: 20px;
    flex-shrink: 0;
}

.mode-card.active .mode-icon {
    background: var(--td-brand-color);
    color: white;
}

.mode-text {
    flex: 1;
}

.mode-text h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 4px 0;
    color: var(--td-text-color-primary);
}

.mode-text p {
    font-size: 12px;
    color: var(--td-text-color-secondary);
    margin: 0;
}

.mode-indicator {
    flex-shrink: 0;
}

/* 配置区域 */
.config-area {
    padding: 24px;
}

.config-section {
    margin-bottom: 24px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.section-title h4 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: var(--td-text-color-primary);
}

.form-container {
    width: 100%;
    padding-top: 20px;
}

.knowledge-selector {
    margin-top: 8px;
}

.knowledge-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.knowledge-chip {
    cursor: pointer;
    transition: all var(--td-transition);
}

.knowledge-chip:hover {
    transform: translateY(-1px);
}

.interview-details {
    margin-top: 16px;
}

.selected-knowledge {
    margin-top: 16px;
}

/* V4版本视频区域样式 */
.videos-section {
    margin-top: 16px;
}

.video-container {
    max-width: 1200px;
    margin: 0 auto;
}

.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
}

.video-card {
    background: white;
    border-radius: var(--td-radius-medium);
    overflow: hidden;
    box-shadow: var(--td-shadow-2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: 1px solid var(--td-border-level-1-color);
}

.video-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--td-shadow-3);
    border-color: var(--td-brand-color);
}

.video-thumbnail {
    position: relative;
    width: 100%;
    height: 180px;
    overflow: hidden;
    background: var(--td-bg-color-container-hover);
}

.thumbnail-image {
    width: 100%;
    height: 100%;
    transition: transform 0.3s ease;
}

.video-card:hover .thumbnail-image {
    transform: scale(1.05);
}

.duration-badge {
    position: absolute !important;
    bottom: 8px;
    right: 8px;
    backdrop-filter: blur(4px);
    font-size: 12px !important;
    z-index: 2;
}

.play-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.3);
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
}

.video-card:hover .play-overlay {
    opacity: 1;
}

.play-button {
    width: 64px !important;
    height: 64px !important;
    box-shadow: 0 4px 12px rgba(0, 82, 217, 0.4) !important;
}

.video-info {
    padding: 16px;
}

.video-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--td-text-color-primary);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.video-description {
    font-size: 0.875rem;
    color: var(--td-text-color-secondary);
    line-height: 1.5;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.empty-state {
    text-align: center;
    padding: 40px 0;
}

/* V4版本对话框样式 */
.video-dialog :deep(.t-dialog__body) {
    padding: 0;
}

.video-modal-content {
    width: 100%;
}

.video-player {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%;
    margin-bottom: 16px;
}

.video-player iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: var(--td-radius-medium);
}

.video-details {
    padding: 16px;
}

.video-meta {
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.video-description-full {
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--td-text-color-secondary);
    margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .video-recommendation-page {
        padding: 16px;
    }

    .panel-header {
        padding: 20px 16px;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }

    .panel-title {
        font-size: 20px;
    }

    .mode-cards {
        grid-template-columns: 1fr;
        padding: 16px;
    }

    .config-area {
        padding: 16px;
    }

    .video-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .video-dialog :deep(.t-dialog) {
        margin: 16px;
    }

    .video-meta {
        flex-direction: column;
        align-items: flex-start !important;
    }
}

@media (max-width: 480px) {
    .panel-title {
        font-size: 1.75rem;
    }

    .panel-subtitle {
        font-size: 1rem;
    }

    .video-thumbnail {
        height: 160px;
    }

    .play-button {
        width: 48px !important;
        height: 48px !important;
    }
}
</style>
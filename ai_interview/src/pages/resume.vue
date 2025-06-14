<script setup>
import axiosLocal from '@/modules/axiosLocal';
import { useResumeStore } from '../stores/resumeStore';
import { reactive, ref, onMounted } from 'vue';
import { NotifyPlugin } from 'tdesign-vue-next';
import { ThumbUpIcon, ChatIcon, ShareIcon, MoreIcon, BrowseIcon, TimeIcon, FileIcon } from 'tdesign-icons-vue-next';
import { MessagePlugin } from 'tdesign-vue-next';
import VuePdfEmbed from 'vue-pdf-embed'
import { useUserStore } from '@/stores/userStore';


const userStore = useUserStore();
const resumeStore = useResumeStore();

// 上传简历时获取当前日期
function getCurrentDate(needTime = false) {
    const d = new Date();
    let month = d.getMonth() + 1;
    month = month < 10 ? Number(`0${month}`) : month;
    const date = `${d.getFullYear()}-${month}-${d.getDate()}`;
    const time = `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`;
    if (needTime) return [date, time].join(' ');
    return date;
}

// 上传设置
const autoUpload = ref(true);
const files = ref([]);
const display = ref('file');

const loading = ref(false);

// 预览简历url
const resumeUrl = ref('')

// 预览对话框
const previewVisible = ref(false)

// res.url 图片地址；res.uploadTime 文件上传时间；res.error 上传失败的原因
function formatResponse(res) {
    // 响应结果添加上传时间字段，用于 UI 显示
    res.uploadTime = getCurrentDate();
    return res;
}

// 上传前检查用户是否登录
const beforeUploadCheck = (file) => {
    if (!userStore.user.email) {
        console.log("no");
        NotifyPlugin.error({ title: '错误', content: '用户未登录，无法上传简历' });
        return false; // 阻止上传
    } else {
        loading.value = true;
        setTimeout(() => {
            getResumeList();
            console.log("yes");
        }, 1500);
        return true; // 允许上传
    }
};

const handleUploadSuccess = ({ response, file }) => {
    console.log('上传成功，服务器返回：', response);
    loading.value = false;
};

const getResumeList = () => {
    axiosLocal.get('/resume/get_resume', { params: { email: userStore.user.email } })
        .then((res) => {
            console.log(res.data);
            if (res.data.code == 200) {
                resumeStore.setResumeList(res.data.data);
            }
        })
}

// 简历操作选项
const options = [
    {
        content: '查看简历画像',
        value: 1,
    },
    {
        content: 'AI优化简历',
        value: 2,
    },
];

// 点击选项后的处理逻辑
const clickHandler = (data, resume) => {
    MessagePlugin.success(`选中【${data.content}】`);
    console.log(resume)
};

const handlePreview = (url) => {
    window.open(url, '_blank')
    // resumeUrl.value = url;
    // previewVisible.value = true;
}

// 格式化文件大小
const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

onMounted(() => {
    if (userStore.user.email) {
        getResumeList();
    }
})

// ------------------------------------------------------------AI 生成简历------------------------------------------------------------
const generating = ref(false)
const openGenerateResumeVisible = ref(false)

const selectedResumeIndex = ref(null)  // 当前选择的简历索引
const generatedResumes = ref([])       // 接收后端传来的3份简历
const previewImageUrl = ref('')        // 放大图像的地址
const previewResumeVisible = ref(false)      // 放大预览是否展示
const word_url = ref('')                // 下载地址
const resume_name = ref('')             // 简历名称


const formData = reactive({
    name: '',
    position: '',
    skills: '',
    education: '',
    experience: ''
})

const rules = {
    name: [{ required: true, message: '请输入个人信息', trigger: 'blur' }],
    position: [{ required: true, message: '请输入目标职位', trigger: 'blur' }],
    skills: [{ required: true, message: '请输入技能特长', trigger: 'blur' }],
    education: [{ required: true, message: '请输入教育背景', trigger: 'blur' }],
    experience: [{ required: true, message: '请输入实习经历', trigger: 'blur' }]
}

const openGenerateResume = async () => {
    try {
        const form = document.querySelector('.ai-form')
        if (!formData.name || !formData.position || !formData.experience || !formData.skills || !formData.education) {
            MessagePlugin.warning('请填写完整信息')
            return
        }

        generating.value = true

        let text = `${formData.name}，目标岗位：${formData.position}，技能特长：${formData.skills}，教育背景：${formData.education}，实习经历：${formData.experience}`

        await axiosLocal.post('/resume/generate_resume', {  text: text  })
            .then((res) => {
                if (res.data.code == 200) {
                    console.log(res.data.data)
                    generatedResumes.value = res.data.data.links
                    openGenerateResumeVisible.value = true
                }
            })

    } catch (error) {
        console.log(error)
        MessagePlugin.error('生成失败，请重试')
    } finally {
        // generating.value = false
    }

}

const selectResume = (index) => {
    selectedResumeIndex.value = index
    console.log('选择了第', index + 1, '份简历')
    // 你也可以处理 resume.word_url，例如下载按钮
    console.log(generatedResumes.value[index].word_url)
    word_url.value = generatedResumes.value[index].word_url
}

const preview = (url) => {
    previewImageUrl.value = url
    previewResumeVisible.value = true
}


const generateResume = async () => {
    try {
        // 表单验证
        const form = document.querySelector('.ai-form')
        if (!formData.name || !formData.position || !formData.experience || !formData.skills || !formData.education) {
            MessagePlugin.warning('请填写完整信息')
            return
        }

        // generating.value = true
        openGenerateResumeVisible.value = false

        MessagePlugin.success('简历生成成功！正在为您下载...')

        axiosLocal.get('/resume/download_resume', { params: { 
            resume_name: resume_name.value,
            word_url: word_url.value,
            email: userStore.user.email,
        } })
           .then((res) => {
                if (res.data.code == 200) {
                    console.log(res.data.data)
                    getResumeList();
                    generating.value = false
                }
            })

        // 模拟AI生成过程
        // await new Promise(resolve => setTimeout(resolve, 3000))

    } catch (error) {
        MessagePlugin.error('生成失败，请重试')
    } finally {
    }
}
</script>

<template>
    <!-- <t-dialog v-model:visible="previewVisible" header="简历预览" width="80%">
        <vue-pdf-embed :source="resumeUrl" style="width: 100%;" />
    </t-dialog> -->

    <div class="resume-page">
        <div class="breadcrumb">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>个人简历</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div style="height: 20px;"></div>

        <t-row :gutter="16" style="margin-bottom: 20px;">
            <t-col :span="6">
                <!-- AI简历生成 -->
                <t-card style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);">
                    <template #header>
                        <div class="ai-header">
                            <div class="ai-icon">✨</div>
                            <div class="ai-title">AI 简历生成助手</div>
                        </div>
                    </template>

                    <div class="ai-content">
                        <div class="ai-description">
                            无需手动排版或反复修改内容，只需输入个人信息，系统将通过智能算法为你自动生成专业、美观的简历。
                        </div>

                        <t-form ref="form" :data="formData" :rules="rules" label-width="80px" class="ai-form">
                            <t-form-item label="个人信息" name="name">
                                <t-input v-model="formData.name" placeholder="请输入您的个人信息, 例如-姓名:张三、年龄:24..." />
                            </t-form-item>

                            <t-form-item label="目标岗位" name="position">
                                <t-input v-model="formData.position" placeholder="请输入目标职位" />
                            </t-form-item>

                            <t-form-item label="教育背景" name="education">
                                <t-input v-model="formData.education" placeholder="请输入学历信息" />
                            </t-form-item>

                            <t-form-item label="技能特长" name="skills">
                                <t-textarea v-model="formData.skills" placeholder="请输入您的技能特长，用逗号分隔"
                                    :autosize="{ minRows: 2, maxRows: 4 }" />
                            </t-form-item>

                            <t-form-item label="实习经历" name="experience">
                                <t-textarea v-model="formData.experience" placeholder="请输入您的技能特长，用逗号分隔"
                                    :autosize="{ minRows: 2, maxRows: 4 }" />
                            </t-form-item>

                        </t-form>

                        <div class="ai-actions">
                            <t-button theme="primary" size="large" :loading="generating" @click="openGenerateResume"
                                block>
                                <template #icon>
                                    <span class="ai-button-icon">🤖</span>
                                </template>
                                {{ generating ? 'AI正在生成中...' : '智能生成简历' }}
                            </t-button>
                        </div>

                        <div class="ai-features">
                            <div class="feature-item">
                                <div class="feature-icon">📄</div>
                                <div class="feature-text">支持WORD下载</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">🎨</div>
                                <div class="feature-text">专业美观模板</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">⚡</div>
                                <div class="feature-text">智能算法优化</div>
                            </div>
                        </div>
                    </div>
                </t-card>

                <t-dialog v-model:visible="openGenerateResumeVisible" theme="info" header="提示" :width="800"
                    :cancel-btn="null" @confirm="generateResume">
                    <template #body>
                        <div class="ai-description">
                            ✨ 我们为您智能生成了3份不同风格的简历，您可以自由预览、选择最满意的一份开始使用。
                        </div>

                        <t-input v-model="resume_name" placeholder="请输入简历名称" />

                        <div class="ai-resume-preview-wrapper">
                            <div class="ai-resume-card" v-for="(resume, index) in generatedResumes" :key="index"
                                @click="selectResume(index)">
                                <img :src="resume.img_url" alt="简历封面" class="ai-resume-img"
                                    @click.stop="preview(resume.img_url)" />
                                <div class="ai-resume-label">
                                    {{ selectedResumeIndex === index ? '✅ 已选择' : '点击选择' }}
                                </div>
                            </div>
                        </div>

                        <!-- 图片预览弹窗 -->
                        <t-dialog v-model:visible="previewResumeVisible" header="简历预览" width="80%">
                            <img :src="previewImageUrl" alt="预览图" style="width: 100%" />
                        </t-dialog>


                    </template>
                </t-dialog>
            </t-col>
            <t-col :span="6">
                <t-card style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);">
                    <template #header>
                        <div class="upload-header">
                            <div class="upload-icon">📤</div>
                            <div class="upload-title">手动上传简历</div>
                        </div>
                    </template>

                    <div class="upload-content">
                        <div class="upload-description">
                            已有简历？直接上传PDF文件，系统将自动解析并为您提供智能优化建议。
                        </div>

                        <div class="upload-wrapper">
                            <t-upload v-model="files" :auto-upload="autoUpload" :theme="display"
                                :data="{ email: userStore.user.email }" :abridge-name="[10, 8]"
                                :format-response="formatResponse" :before-upload="beforeUploadCheck" draggable
                                accept=".pdf" :on-success="handleUploadSuccess"
                                action="http://127.0.0.1:5000/resume/add_resume" class="enhanced-upload">
                            </t-upload>
                        </div>

                        <div class="upload-tips">
                            <div class="tip-item">
                                <span class="tip-icon">✓</span>
                                <span class="tip-text">支持PDF格式</span>
                            </div>
                            <div class="tip-item">
                                <span class="tip-icon">✓</span>
                                <span class="tip-text">文件大小不超过10MB</span>
                            </div>
                        </div>

                        <div class="upload-features">
                            <div class="feature-item">
                                <div class="feature-icon">🔍</div>
                                <div class="feature-text">智能解析</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">🎯</div>
                                <div class="feature-text">精准优化</div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon">📊</div>
                                <div class="feature-text">简历画像</div>
                            </div>
                        </div>
                    </div>
                </t-card>
            </t-col>
        </t-row>

        <div class="section-divider">个人简历</div>

        <!-- 美化后的简历展示区域 -->
        <div class="resume-grid">
            <div class="resume-card-wrapper" v-for="resume in resumeStore.resumeList" :key="resume.name">
                <div class="resume-card" v-loading="loading" element-loading-text="智能体正在解析您的简历，请稍候⏱️">

                    <!-- 封面区域 -->
                    <div class="resume-cover" @click="handlePreview(resume.url)">
                        <div class="cover-container">
                            <img :src="resume.preview" alt="简历封面" class="cover-image" />
                            <div class="cover-overlay">
                                <div class="overlay-content">
                                    <BrowseIcon size="2em" class="preview-icon" />
                                    <span class="preview-text">预览简历</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 简历信息 -->
                    <div class="resume-info">
                        <div class="resume-header">
                            <div class="resume-title">
                                <FileIcon size="1.2em" class="file-icon" />
                                <span class="resume-name">{{ resume.name }}</span>
                            </div>
                            <t-dropdown :options="options" :min-column-width="120"
                                @click="(data) => clickHandler(data, resume)" placement="bottom-right">
                                <t-button variant="text" shape="circle" size="small" class="action-button">
                                    <MoreIcon size="1.2em" />
                                </t-button>
                            </t-dropdown>
                        </div>

                        <div class="resume-meta">
                            <div class="meta-item">
                                <TimeIcon size="0.9em" class="meta-icon" />
                                <span class="meta-text">{{ getCurrentDate() }}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-text">{{ formatFileSize(1024 * 1024 * 2) }}</span>
                            </div>
                        </div>

                        <!-- 快捷操作按钮 -->
                        <div class="resume-actions">
                            <t-button size="small" variant="outline" theme="primary"
                                @click="clickHandler({ content: '查看简历画像', value: 1 }, resume)">
                                <template #icon>
                                    <span class="action-icon">📊</span>
                                </template>
                                简历画像
                            </t-button>
                            <t-button size="small" variant="outline" theme="success"
                                @click="clickHandler({ content: 'AI优化简历', value: 2 }, resume)">
                                <template #icon>
                                    <span class="action-icon">✨</span>
                                </template>
                                AI优化
                            </t-button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 空状态 -->
            <div v-if="!resumeStore.resumeList || resumeStore.resumeList.length === 0" class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-title">暂无简历</div>
                <div class="empty-description">
                    您还没有上传任何简历，快去上传或生成一份吧！
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.resume-page {
    background-color: rgb(245, 247, 250);
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

/* 覆盖拖拽区域宽度 */
::v-deep(.t-upload__dragger),
::v-deep(.t-upload__dragger-center) {
    width: 100%;
    /* 或你需要的宽度 */
    max-width: none;
}

/* 替换内容：你可以通过伪元素替代默认文字 */
::v-deep(.t-upload__dragger-center)::before {
    content: "请上传 PDF 简历文件，或将其拖拽到此处，";
    display: block;
}

.cover-wrapper {
    position: relative;
    cursor: pointer;
}

.cover-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.hover-mask {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 6px;
    background-color: rgba(0, 0, 0, 0.4);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: 0.3s ease;
}

.cover-wrapper:hover .hover-mask {
    opacity: 1;
}

.section-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 24px 0;
    font-weight: bold;
    color: #0052D9;
    /* 分割线文字颜色 */
}

.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #0052D9;
    /* 分割线颜色和粗细 */
    margin: 0 12px;
}

/* ------------------------------------------------------------AI 生成简历------------------------------------------------------------ */
.ai-header {
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-icon {
    font-size: 20px;
}

.ai-title {
    font-size: 16px;
    font-weight: 600;
    color: #0052D9;
}

.ai-content {
    padding: 0;
}

.ai-description {
    color: #666;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 20px;
    padding: 12px;
    background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
    border-radius: 6px;
    border-left: 3px solid #0052D9;
}

.ai-form {
    margin-bottom: 20px;
}

.ai-actions {
    margin-bottom: 20px;
}

.ai-button-icon {
    margin-right: 4px;
}

.ai-features {
    display: flex;
    justify-content: space-around;
    padding: 16px 0;
    border-top: 1px solid #eee;
}

.feature-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.feature-icon {
    font-size: 20px;
}

.feature-text {
    font-size: 12px;
    color: #666;
    text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .ai-features {
        flex-direction: column;
        gap: 12px;
    }

    .feature-item {
        flex-direction: row;
        justify-content: flex-start;
    }

    .feature-text {
        text-align: left;
    }
}

/* 加载状态样式 */
.t-button--loading .ai-button-icon {
    display: none;
}

/* 表单样式优化 */
:deep(.t-form-item__label) {
    font-weight: 500;
    color: #333;
}

:deep(.t-input__inner),
:deep(.t-textarea__inner),
:deep(.t-select .t-input__inner) {
    border-radius: 6px;
}

:deep(.t-input__inner:focus),
:deep(.t-textarea__inner:focus),
:deep(.t-select .t-input__inner:focus) {
    border-color: #0052D9;
    box-shadow: 0 0 0 2px rgba(0, 82, 217, 0.1);
}

/* ------------------------------------------------------------手动上传简历------------------------------------------------------------ */
.upload-header {
    display: flex;
    align-items: center;
    gap: 8px;
}

.upload-icon {
    font-size: 20px;
}

.upload-title {
    font-size: 16px;
    font-weight: 600;
    color: #0052D9;
}

.upload-content {
    padding: 0;
}

.upload-description {
    color: #666;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 20px;
    padding: 12px;
    background: linear-gradient(135deg, #fff8f0 0%, #fff2e8 100%);
    border-radius: 6px;
    border-left: 3px solid #ff7d00;
}

.upload-wrapper {
    margin-bottom: 16px;
}

.enhanced-upload {
    width: 100%;
}

/* 美化原有的拖拽区域，不破坏功能 */
.enhanced-upload :deep(.t-upload__dragger) {
    border: 2px dashed #d0d7ff !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #fafbff 0%, #f0f4ff 100%) !important;
    transition: all 0.3s ease !important;
    min-height: 120px !important;
}

.enhanced-upload :deep(.t-upload__dragger:hover) {
    border-color: #0052D9 !important;
    background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%) !important;
}

.enhanced-upload :deep(.t-upload__dragger-center) {
    padding: 20px !important;
}

/* 美化拖拽区域的文字 */
.enhanced-upload :deep(.t-upload__dragger-center)::before {
    content: "📄 拖拽PDF文件到此处，或点击选择文件上传" !important;
    display: block !important;
    font-size: 16px !important;
    color: #333 !important;
    font-weight: 500 !important;
    margin-bottom: 8px !important;
}

.enhanced-upload :deep(.t-upload__dragger-text) {
    color: #666 !important;
    font-size: 14px !important;
}

.upload-tips {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}

.tip-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: #0052D9;
    background: rgba(0, 82, 217, 0.1);
    padding: 6px 12px;
    border-radius: 12px;
}

.tip-icon {
    font-weight: bold;
}

.upload-features {
    display: flex;
    justify-content: space-around;
    padding: 16px 0;
    border-top: 1px solid #eee;
}

.upload-features .feature-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.upload-features .feature-icon {
    font-size: 20px;
}

.upload-features .feature-text {
    font-size: 12px;
    color: #666;
    text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .upload-tips {
        flex-direction: column;
        gap: 8px;
    }

    .upload-features {
        flex-direction: column;
        gap: 12px;
    }

    .upload-features .feature-item {
        flex-direction: row;
        justify-content: flex-start;
    }

    .upload-features .feature-text {
        text-align: left;
    }
}

/* ------------------------------------------------------------简历展示区域------------------------------------------------------------ */
.resume-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.resume-card-wrapper {
    position: relative;
}

.resume-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
    position: relative;
}

.resume-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.resume-status {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 2;
}

.resume-cover {
    position: relative;
    cursor: pointer;
    height: 400px;
    overflow: hidden;
}

.cover-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.cover-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.resume-card:hover .cover-image {
    transform: scale(1.05);
}

.cover-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(0, 82, 217, 0.8) 0%, rgba(0, 82, 217, 0.6) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.resume-cover:hover .cover-overlay {
    opacity: 1;
}

.overlay-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    color: white;
    text-align: center;
}

.preview-icon {
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.preview-text {
    font-size: 14px;
    font-weight: 500;
}

.resume-info {
    padding: 16px;
}

.resume-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.resume-title {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
}

.file-icon {
    color: #0052D9;
}

.resume-name {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.action-button {
    color: #666;
    transition: color 0.2s ease;
}

.action-button:hover {
    color: #0052D9;
}

.resume-meta {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 4px;
}

.meta-icon {
    color: #999;
}

.meta-text {
    font-size: 12px;
    color: #666;
}

.resume-actions {
    display: flex;
    gap: 8px;
}

.resume-actions .t-button {
    flex: 1;
    border-radius: 6px;
}

.action-icon {
    font-size: 12px;
}

/* 空状态 */
.empty-state {
    grid-column: 1 / -1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    text-align: center;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.6;
}

.empty-title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
}

.empty-description {
    font-size: 14px;
    color: #666;
    line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .resume-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .resume-cover {
        height: 160px;
    }

    .resume-actions {
        flex-direction: column;
    }

    .resume-actions .t-button {
        flex: none;
    }
}

@media (max-width: 480px) {
    .resume-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }

    .resume-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }

    .action-button {
        align-self: flex-end;
    }
}

/* 加载状态覆盖 */
:deep(.t-loading__overlay) {
    border-radius: 12px;
}

.ai-resume-preview-wrapper {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 16px;
}

.ai-resume-card {
  width: 160px;
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 6px;
  padding: 8px;
  transition: border-color 0.2s;
}

.ai-resume-card:hover {
  border-color: #0052d9;
}

.ai-resume-img {
  width: 100%;
  height: auto;
  border-radius: 4px;
  object-fit: cover;
}

.ai-resume-label {
  margin-top: 6px;
  font-size: 13px;
  text-align: center;
  color: #333;
}
</style>
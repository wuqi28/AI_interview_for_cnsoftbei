<script setup lang="jsx">
import { onMounted, ref, watch, reactive, onBeforeMount } from 'vue';
import { Edit, Picture, Upload, Location, OfficeBuilding, Suitcase, School, CirclePlus, ChatDotSquare} from '@element-plus/icons-vue';
import { PlayCircleIcon, LoadingIcon } from 'tdesign-icons-vue-next';
import Vue3MarkdownIt from 'vue3-markdown-it';
import { BaiduMap } from 'vue-baidu-map-3x';
import { useResumeStore } from '../stores/resumeStore';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { useUserStore } from '../stores/userStore';
import axiosLocal from '../modules/axiosLocal';
import { useInterviewStore } from '../stores/interviewStore';
import { useRouter } from 'vue-router'
import { MessagePlugin, Drawer, Loading } from 'tdesign-vue-next';

const resumeStore = useResumeStore();
const userStore = useUserStore();
const interviewStore = useInterviewStore();

const router = useRouter()

// 定义当前步骤，初始为 1
const activeStep = ref(1);
// 定义上一步按钮是否禁用
const prevDisabled = ref(false);
// 定义下一步按钮是否禁用
const nextDisabled = ref(false);

// 上一步按钮点击事件处理函数
const prevStep = () => {
    if (activeStep.value > 1) {
        activeStep.value--;
    }
};

// 下一步按钮点击事件处理函数
const nextStep = () => {
    if (activeStep.value < 4) {
        activeStep.value++;
    }
};

// 监听activeStep的变化，当为1时上一步按钮disable，为3时下一步按钮disable
watch(activeStep, (newValue) => {
    if (newValue === 1) {
        prevDisabled.value = true;
        nextDisabled.value = false;
    } else if (newValue === 3) {
        interviewStore.setQuestionType();
        prevDisabled.value = false;
        nextDisabled.value = false;
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                console.log('权限已获取')
                getDevices();
            })
            .catch(() => {
                console.log('权限未获取')
            })
    } else if (newValue === 2){
        prevDisabled.value = false;
        nextDisabled.value = false;
    } else if (newValue === 4){
        prevDisabled.value = false;
        nextDisabled.value = true; 
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                console.log('权限已获取')
                getDevices();
            })
            .catch(() => {
                console.log('权限未获取')
            })
    }
});

// 模拟岗位数据
const jobs = ref([
    {
        type: 1,
        similarity: 0,
        title: '算法工程师',
        salary: '10k-20k',
        location: '北京',
        experience: '2年以上',
        education: '本科以上',
        description: `## 职位描述

**ByteIntern**：面向2026届毕业生（2025年9月 - 2026年8月期间毕业），为符合岗位要求的同学提供转正机会。

### 团队介绍

风控研发团队致力于解决各个产品（包括抖音、今日头条等）面临的各种黑灰产对抗问题，涵盖内容、交易、流量、账号等多个方面的风险治理领域。利用机器学习、多模态、大模型等技术对用户行为、内容进行理解，从而识别潜在的风险和问题。团队不断深入理解业务和用户行为，进行模型和算法创新，打造业界领先的风控算法体系。

### 岗位职责

1. 负责字节跳动各产品（包括抖音、今日头条等）各种作弊风险的发现与治理，包括内容、交易、流量、账号等方面的风险；
2. 通过指标监控归因，及时感知风险及业务的变化，主动识别潜在攻击，持续优化调整风控方案，并推动风控治理建设及业务模式调整；
3. 通过计算机视觉（CV）、自然语言处理（NLP）、大语言模型、多模态大模型、表征学习、图模型、深度学习、迁移学习、多任务学习等技术，提升问题发现的效率，从而快速阻断风险，优化平台的各项生态指标；
4. 挖掘和分析海量内容和用户行为，进行用户长短期画像建设，提升模型的精准性和召回面；
5. 结合各场景业务（抖音短视频、电商、直播、生活服务、用户增长等）特性，进行模型和算法创新，打造业界领先的风控算法体系。

### 职位要求

1. 2026届本科及以上学历在读，计算机、机器学习和模式识别等相关专业优先；
2. 热爱计算机科学和互联网技术，对人工智能类产品有浓厚兴趣；
3. 具备优秀的编码能力，熟悉 Linux 开发环境，熟悉 C++ 和 Python 语言优先；
4. 有扎实的数据结构和算法功底，熟悉机器学习、自然语言处理、数据挖掘、分布式计算、计算机视觉、计算机图形中的一项或多项；
5. 优秀的分析问题和解决问题的能力，对解决具有挑战性问题充满激情；
6. 每周可实习 4 天以上，实习时间 3 个月以上。`,
        company: '字节跳动',
    },
    {
        type: 1,
        similarity: 0,
        title: '前端开发工程师',
        salary: '15k-31k',
        location: '北京',
        experience: '1-3年',
        education: '本科',
        description: `## 职位描述

1. 负责 C 端与后台产品的前端开发工作，包括页面设计、交互实现及性能优化，提升用户体验；
2. 参与后台管理系统的设计与开发，确保功能稳定性和易用性；
3. 维护现有前端系统，及时修复问题并持续改进代码质量；
4. 与产品、设计及后端团队协作，完成拉新相关功能的开发和上线；
5. 关注前端技术发展趋势，引入合适的工具和技术提升开发效率；
6. 编写清晰规范的技术文档，为团队协作提供支持。

## 职位要求

1. 计算机相关专业本科及以上学历，具备扎实的计算机基础知识；
2. 1-3 年前端开发经验，熟悉 HTML/CSS/JavaScript 等核心技术，熟练使用 React/Vue 等主流框架进行项目开发；
3. 熟悉前后端交互流程，能够独立完成 C 端及后台系统的前端功能设计与实现，了解 RESTful API 或 GraphQL 的使用；
4. 具备良好的逻辑思维能力和代码规范意识，注重用户体验和性能优化；
5. 拥有较强的沟通协作能力，能够快速理解业务需求并转化为技术方案，适应敏捷开发模式；
6. 熟悉 Node.js 或有小程序开发经验者优先，对新技术保持敏感度和学习热情。
`,
        company: '网易'
    },
    {
        type: 1,
        similarity: 0,
        title: 'Java研发专家',
        salary: '20k-36k·16薪',
        location: '北京',
        experience: '经验不限',
        education: '本科',
        description: `## 职位描述

阿里云开放平台企业 IT 治理团队专注于构建阿里云的核心基础设施——身份认证、权限管理、审计以及资源管理系统。我们负责了阿里云每一次控制台访问以及每一次 API 调用的安全性和合规性，并提供了云资源中台服务，支撑了客户海量云资源的完整生命周期管理。

企业 IT 治理团队围绕认证（Authentication）、授权（Authorization）和审计（Auditing）的方向提供了以下的产品和服务：

1. **访问控制（RAM）：**
   - 负责阿里云身份模型的设计与研发，提供云平台上安全灵活的身份管理能力和解决方案；
   - 负责阿里云授权系统的设计与研发；提供灵活、可扩展、高性能的鉴权平台；每天为阿里云超过数百款产品和服务提供数万亿次鉴权服务；
   - 负责阿里云访问密钥和认证服务的设计与研发，提供安全可靠的 API 认证协议和全球化部署的认证平台，每天支撑阿里云数万亿次认证请求；
   
2. **阿里云资源管理服务(ResourceManager)：**
   - 负责阿里云账号内与跨账号的资源管理服务——资源组(ResourceGroup)和资源目录(ResourceDirectory/Organizations)的研发, 为企业客户提供全套云上资源管理能力和解决方案；
   - 负责阿里云基础组件资源管理中心的设计与研发，为数百款云产品提供统一的资源数据中台，为海量资源提供统一的商业化计费服务以及生命周期管理；
   
3. **阿里云操作审计(ActionTrail)：**
   - 负责阿里云上记录所有操作的审计系统的设计与研发，每天处理数万亿的事件数据，通过对审计数据的发掘，帮助云上客户发现潜在的安全和稳定性风险；
   
4. **阿里云配置审计(CloudConfig)：**
   - 负责阿里云上面向资源的审计产品的设计与研发，提供精确的资源配置历史追踪和高效的配置合规审计能力，帮助客户实现云上基础设施的自主监管以及持续合规。

### 该岗位负责

1. 负责开放平台资源管理业务的需求分析和交付，解决面向高并发、稳定性、海量数据、复杂业务场景的技术问题；
2. 确保系统的稳定性、安全性、性能，寻找并解决系统中的潜在风险和瓶颈；
3. 通过平台化的方式服务于各云产品的企业级能力构建，制定平台级的资源生命周期管控技术标准；
4. 调研并分析业界云资源管控、CMDB的发展态势，在技术和产品上不断提升阿里资源管理平台的服务和客户体验；
5. 帮助团队不断提升工程质量和工程效率。

### 职位要求

1. 有扎实的 Java 基础，熟悉 IO/多线程/网络等基础框架，熟悉分布式/缓存/消息/搜索等机制；
2. 精通 Java Web 应用的开发，深入了解 Spring/Mybatis/Cache/RPC/JVM 等机制；
3. 具备在大中型项目中担任负责人或主开发的经验，熟练掌握设计模式和系统架构设计；
4. 具备高并发系统的稳定性和安全性保障经验，熟练掌握稳定性和安全性保障的技术和方法；
5. 具备良好的分析和解决问题的能力及沟通协作能力；
6. 计算机及相关专业本科及以上学历，有云计算业务背景或者大型互联网公司、大型企业软件设计开发经验优先。
`,
        company: '阿里云'
    },
    {
        type: 2,
        similarity: 0,
        title: '服务器运维算力基础设施北京【校招】',
        salary: '15k-21k',
        location: '北京',
        experience: '在校/应届',
        education: '本科',
        description: `## 职位描述

### 团队介绍

字节跳动系统部，负责字节跳动从芯片到服务器、操作系统、网络、CDN、数据中心等基础设施的研发、设计、采购、交付与运营管理，为包含抖音、头条、火山引擎等全球业务提供高效、稳定、具备可扩展性的基础设施。部门当前业务开展包括不限于：数据中心设计建设、芯片研发、服务器研发、网络工程研发、火山引擎边缘云业务、高性能智能硬件研发、IDC资源智能交付与运维、硬件基础设施智能监控与预警、操作系统与内核、虚拟化技术、编译工具链、供应链管理等众多基础设施相关方向。

### 岗位职责

1. 负责线上服务器稳定性保障服务，规划和建设稳定性流程规范、平台系统、保障机制和能力，负责现网运营稳定性监控、稳定性风险识别、问题响应处理和保障措施，保障业务稳定健康运行；
2. 规划和建设路标、维保范围、SLO/SLA，驱动并协同配套流程建设和运营，面向业务提供整体服务交付；
3. 运营技术支持能力建设和运营，服务器自维保运营适配，运维赋能建设和管理；运营数据及指标化建设和运营，过程分析和治理，运营技术、流程、工具系统优化；
4. 自维保现场运维规范化标准化建设和运营，包含自维保现场运维流程规范、操作规范、运维技术规范等；
5. 数据中心自维保现场管理和运营，包含自维保现场服务水平、服务质量、人效、赋能、过程管理和运营等；技术支持，包含复杂问题支持、共性问题、质量问题、风险隐患发掘、处理和驱动解决等；
6. 服务器可维护性、易维护性标准建设、风险识别，标准化规范化管理和运营。

### 职位要求

1. 2025届获得本科及以上学历，理工科、计算机、电子信息工程、自动化等相关专业优先；
2. 具有较强的沟通协调能力，善于思考和总结，具备良好的文档能力，有项目管理认证或经历优先；
3. 责任心强，细致认真，对工作充满热情、富有团队精神；学习能力强，对新技术充满热情和好奇心，具有较强的解决问题、动手实践能力；具备较强的抗压抗干扰能力，能适应快节奏工作和丰富的工作任务；
4. 具备较好的计算机编程基础，熟练掌握 Python/Java/PHP/Perl/Go 等常用计算机语言之一；
5. 了解服务器、Linux 系统相关知识，掌握 Shell 脚本。
`,
        company: '字节跳动'
    },
    {
        type: 3,
        similarity: 0,
        title: '互联网产品经理',
        salary: '20k-30k·16薪',
        location: '北京',
        experience: '1-3年',
        education: '本科',
        description: `## 岗位职责

1. 深入理解目标市场和用户需求，通过多渠道收集和分析数据，为产品方向和功能提供决策支持；
2. 与团队成员紧密合作，共同探索产品功能和用户体验的优化；
3. 关注产品设计和用户界面，确保产品符合市场趋势和用户期望；
4. 与研发、运营等部门紧密合作，确保产品从概念到推出各环节顺畅。
        `,
        company: '百度'
    },
    {
        type: 1,
        similarity: 0,
        title: '嵌入式工程师',
        salary: '30k-50k·20薪',
        location: '北京',
        experience: '3-5年',
        education: '本科',
        description: `## 职位描述

### 一、工作职责

- 基于 Android 的物联网应用开发、5G 路由器及嵌入式终端系统搭建，实现本地组网和端云协同系统，包括：
  - 基于 Android 平台物联网应用的架构设计、开发与优化，实现设备与云端的数据交互及远程控制功能，对接和处理硬件设备的通信接口。
  - 开发和部署物联网常用网络协议（如 MQTT、CoAP、HTTP/HTTPS、TCP/IP、UDP 等），配置和维护 5G 路由器，优化设备在 5G 环境下的通信稳定性与低延迟。
  - 主导或参与物联网嵌入式终端的软硬件开发，包括传感器、网关设备、控制执行器等。

### 二、任职要求

- 计算机科学、电子工程、通信工程或相关专业本科及以上学历，3 年以上物联网/嵌入式开发经验。
- 熟练掌握 Java/Kotlin，熟悉 Android SDK；熟悉 Android NDK/JNI 开发，具备硬件接口（如 UART、SPI、I2C）控制经验，有 BLE/Wi-Fi/NFC 等无线通信协议开发经验。
- 熟悉 4G/5G 协议栈，具备 5G 路由器固件开发、网络配置优化及故障排查能力。
- 熟练掌握 C/C++，有嵌入式产品的量产开发经验，熟悉常见通信协议（如 LoRa、ZigBee、NB-IoT）。

### 三、加分项

- 熟悉 CAN 协议，具有汽车电子软件开发经验；
- 深入理解某种通信协议的架构和实现（如蓝牙，ZigBee 等）；
- 硬件调试经验；
- 了解信息安全相关的开发和加固技术。
`,
        company: '京东'
    }
])

// 当前岗位的表单数据
const form = reactive({
    title: '',
    salary: '',
    location: '',
    experience: '',
    education: '',
    description: '',
    company: '',
})

let lastSelectedCard = null; // 记录上一次点击的岗位卡片元素

// 点击左侧岗位项时更新表单
function handleSelect(index, event) {
    const job = jobs.value[Number(index)];
    interviewStore.setJob(job);
    interviewStore.setJobType(job.type);
    console.log(job);
    form.title = job.title;
    form.salary = job.salary;
    form.location = job.location;
    form.experience = job.experience;
    form.education = job.education;
    form.description = job.description;
    form.company = job.company;

    // 获取当前DOM 元素
    const selectedCard = event?.currentTarget;
    if (selectedCard) {
        // 清除上一个选中项的边框样式
        if (lastSelectedCard && lastSelectedCard !== selectedCard) {
            lastSelectedCard.style.border = '2px solid rgb(255, 255, 255)'; // 恢复默认样式
        }

        // 设置当前点击项的边框样式
        selectedCard.style.border = '2px solid rgb(64, 158, 255)';

        // 更新记录
        lastSelectedCard = selectedCard;
    }
}

const addJobDialogVisible = ref(false) // 添加岗位对话框

// 新岗位对象
const newJob = ref({
    title: '',
    salary: '',
    location: '',
    experience: '',
    education: '',
    description: '',
    company: '',
    similarity: 0,
})

// 添加岗位方法
const addJob = () => {
    // 简单校验
    if (!newJob.value.title || !newJob.value.company) {
        return alert('请填写岗位名称和公司名称')
    }

    // 将副本添加进 jobs
    jobs.value.unshift({ ...newJob.value })

    // 清空表单
    Object.keys(newJob.value).forEach((key) => {
        newJob.value[key] = ''
    })

    // 关闭弹窗
    addJobDialogVisible.value = false
}

// 添加匹配成功的岗位
const addMatchedJob = (job) => {
    // console.log('添加匹配成功的岗位:', job.job)
    let newMatchedJob = job.job;
    newMatchedJob.similarity = job.similarity;
    // 将副本添加进 jobs
    jobs.value.unshift({ ...newMatchedJob })
    handleSelect(0)
    MessagePlugin.success('岗位申请成功')
}

const selectedResumeName = ref('');
const hightWeightTags = ref('');

// 任务1: 添加岗位匹配功能
const matchedJobs = ref([]);
const isMatchingJobs = ref(false);
const showMatchResults = ref(false);

// 岗位匹配方法
const matchJobs = async () => {
    if (!hightWeightTags.value) {
        MessagePlugin.warning('请先选择简历，获取技能标签');
        return;
    }

    isMatchingJobs.value = true;
    showMatchResults.value = false;

    try {
        const response = await axiosLocal.post('/resume/resume_match_job', {
            resume_tags: hightWeightTags.value
        });
        console.log('匹配岗位返回数据:', response.data);

        if (response.data.code == 200) {
            matchedJobs.value = response.data.data;
            showMatchResults.value = true;
            MessagePlugin.success('岗位匹配成功');
        } else {
            MessagePlugin.error('获取匹配岗位失败，返回数据格式不正确');
        }
    } catch (error) {
        console.error('岗位匹配请求失败:', error);
        MessagePlugin.error('岗位匹配请求失败，请稍后重试');
    } finally {
        isMatchingJobs.value = false;
    }
};

const handleSelectResume = (resume) => {
    selectedResumeName.value = resume.name;
    // console.log('你选择了：', resume.tags);

    // 提取 tag_weight > 0.5 的 tag_name
    let selectedTags = [];

    ['pos_tags', 'pos_types', 'skills_tags'].forEach(category => {
        if (resume.tags && Array.isArray(resume.tags[category])) {
            resume.tags[category].forEach(tag => {
                if (tag.tag_weight > 0.5) {
                    selectedTags.push(tag.tag_name);
                }
            });
        }
    });

    // 拼接为字符串
    const tagsStr = selectedTags.join('，');
    hightWeightTags.value = tagsStr;
    // console.log('提取出的高权重标签：', tagsStr);

    // 请求简历内容
    axiosLocal.get('/resume/get_resume_txt', { params: { email: userStore.user.email, name: resume.name } })
        .then((res) => {
            if (res.data.code == 200) {
                resumeMarkDown.value = res.data.data;
                interviewStore.setResumeMarkDown(resumeMarkDown.value);
            }
        })
        .catch((error) => {
            console.error('Error fetching resume:', error);
        });
};


const resumeMarkDown = ref() // 当前选中的简历MarkDown

onBeforeMount(() => {
    handleSelect(0)
})

onMounted(() => {
    // 等待数据加载完后选中第一个
    if (resumeStore.resumeList.length > 0) {
        handleSelectResume(resumeStore.resumeList[0]);
    }
})

// 设备选项
const audioOptions = ref([])
const videoOptions = ref([])

const selectedAudioDeviceId = ref('')
const selectedVideoDeviceId = ref('')

const audioAvailable = ref(false)
const videoAvailable = ref(false)

const videoPreview = ref(null)

const getDevices = async () => {
    try {
        // 获取设备列表
        const devices = await navigator.mediaDevices.enumerateDevices()
        // console.log(devices)
        const audioInputs = devices.filter(d => d.kind === 'audioinput')
        const videoInputs = devices.filter(d => d.kind === 'videoinput')

        // 格式化成 TDesign option 格式
        audioOptions.value = audioInputs.map(device => ({
            label: device.label || `麦克风 ${device.deviceId.slice(0, 5)}`,
            value: device.deviceId
        }))
        videoOptions.value = videoInputs.map(device => ({
            label: device.label || `摄像头 ${device.deviceId.slice(0, 5)}`,
            value: device.deviceId
        }))

        // 默认选择第一个设备
        if (audioOptions.value.length) selectedAudioDeviceId.value = audioOptions.value[0].value
        if (videoOptions.value.length) selectedVideoDeviceId.value = videoOptions.value[0].value

        await startPreview()
    } catch (err) {
        MessagePlugin.error('无法获取媒体设备权限')
    }
}

const startPreview = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: selectedVideoDeviceId.value ? { exact: selectedVideoDeviceId.value } : undefined },
            audio: { deviceId: selectedAudioDeviceId.value ? { exact: selectedAudioDeviceId.value } : undefined }
        })

        if (videoPreview.value) {
            videoPreview.value.srcObject = stream
        }

        audioAvailable.value = true
        videoAvailable.value = true
    } catch (err) {
        console.error('媒体设备获取失败：', err)
        audioAvailable.value = false
        videoAvailable.value = false
        MessagePlugin.warning('部分设备不可用，请检查权限或连接')
    }
}

const handleAudioChange = async () => {
    await startPreview()
}

const handleVideoChange = async () => {
    await startPreview()
}

// 面试官角色参数
const interviewerOptions = [
    { label: '马可', value: '110017006' },
    { label: '浩然', value: 'cnr5dg8n2000000003' },
    { label: '沐沐', value: '110332017' },
    { label: '诗雅', value: 'cnrn9jgi2000000005' },
];

// 面试官选中参数
const interviewerValue = ref();
const interviewerIsTrue = ref(false);
const interviewerLabel = ref();

// 面试官参数变化时的处理函数
const interviewerChange = (value) => {
    interviewerIsTrue.value = true;
    interviewerValue.value = value;
    const selected = interviewerOptions.find(opt => opt.value === value)
    const label = selected ? selected.label : ''
    interviewerLabel.value = label;
};

// 声音参数
const vcnOptions = [
    { label: '小钟4.0', value: 'x4_xiaozhong' },
    { label: '天明4.0', value: 'x4_mingge' },
    { label: '悦小妮', value: 'x4_yuexiaoni_assist' },
    { label: '聆小琪', value: 'x4_lingxiaoqi_oral' }
]

// 声音选中参数
const vcnValue = ref();
const vcnIsTrue = ref(false);

// 声音参数变化时的处理函数
const vcnChange = (value) => {
    vcnIsTrue.value = true;
    vcnValue.value = value;
}

// 面试风格参数
const styleOptions = [
    { label: '亲切随和型', value: '亲切随和型(Friendly & Supportive)' },
    { label: '专业严谨型', value: '专业严谨型(Professional & Rational)' },
    { label: '施压挑战型', value: '施压挑战型(Challenging & Critical)' },
]

// 面试风格选中参数
const styleValue = ref();
const styleIsTrue = ref(false);

// 面试风格参数变化时的处理函数
const styleChange = (value) => {
    styleIsTrue.value = true;
    styleValue.value = value;
}

// 开始面试点击事件
const handleStartInterview = () => {
    if (interviewerIsTrue.value && vcnIsTrue.value && styleIsTrue.value) {
        interviewStore.setInterviewConfig(interviewerValue.value, vcnValue.value, styleValue.value);
        interviewStore.setInterviewerName(interviewerLabel.value);
        axiosLocal.post('/interview/start_interview', { email: userStore.user.email, job: interviewStore.job, resumeMarkdown: interviewStore.resumeMarkDown, interviewerConfig: interviewStore.interviewConfig, interviewer_name: interviewStore.interviewConfig.interviewerName, interview_style: interviewStore.interviewConfig.styleValue }).then((resp) => {
            if (resp.data.code == 200) {
                let res_data = resp.data.data;
                interviewStore.setCurrentInterviewId(res_data.current_interview_id);
                interviewStore.setInterviewRecord(res_data.interview_record);
                localStorage.setItem('current_interview_id', res_data.current_interview_id);
            }
        })
        router.push('/mock');
    } else {
        MessagePlugin.warning({ content: '完成面试配置即可进入模拟面试' });
    }
}

</script>

<template>
    <!-- 添加岗位对话框 -->
    <el-dialog v-model="addJobDialogVisible" title="新增岗位" width="800">
        <el-form :model="newJob" label-width="100px">
            <el-form-item label="岗位名称">
                <el-input v-model="newJob.title" />
            </el-form-item>
            <el-form-item label="薪资范围">
                <el-input v-model="newJob.salary" />
            </el-form-item>
            <el-form-item label="工作地点">
                <el-input v-model="newJob.location" />
            </el-form-item>
            <el-form-item label="经验要求">
                <el-input v-model="newJob.experience" />
            </el-form-item>
            <el-form-item label="学历要求">
                <el-input v-model="newJob.education" />
            </el-form-item>
            <el-form-item label="岗位描述">
                <el-input type="textarea" :rows="6" v-model="newJob.description" />
            </el-form-item>
            <el-form-item label="公司名称">
                <el-input v-model="newJob.company" />
            </el-form-item>
        </el-form>

        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addJobDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="addJob">确认</el-button>
            </div>
        </template>
    </el-dialog>

    <!-- 岗位匹配结果抽屉 -->
    <t-drawer v-model:visible="showMatchResults" header="岗位匹配结果" size="large" :footer="false" destroyOnClose>
        <template v-if="matchedJobs.length > 0">
            <div class="matched-jobs-container">
                <div v-for="(item, index) in matchedJobs" :key="index" class="matched-job-card">
                    <div class="matched-job-header">
                        <div class="matched-job-title">{{ item.job.title }}</div>
                        <div class="matched-job-similarity">
                            <!-- <t-progress :percentage="item.similarity"
                                :color="item.similarity > 90 ? '#0ABF5B' : item.similarity > 80 ? '#0052D9' : '#ED7B2F'"
                                :stroke-width="8" /> -->
                            <span class="similarity-text">匹配度: {{ item.similarity }}%</span>
                        </div>
                    </div>
                    <div class="matched-job-details">
                        <div class="matched-job-info">
                            <div class="info-item">
                                <t-icon name="money-circle" />
                                <span>{{ item.job.salary }}</span>
                            </div>
                            <div class="info-item">
                                <t-icon name="location" />
                                <span>{{ item.job.location }}</span>
                            </div>
                            <div class="info-item">
                                <t-icon name="user-circle" />
                                <span>{{ item.job.experience }}</span>
                            </div>
                            <div class="info-item">
                                <t-icon name="book-open" />
                                <span>{{ item.job.education }}</span>
                            </div>
                        </div>
                        <div class="matched-job-company">
                            <t-icon name="office-building" />
                            <span>{{ item.job.company }}</span>
                        </div>
                        <div class="matched-job-description">
                            <p>{{ item.job.description }}...</p>
                        </div>
                        <div class="matched-job-actions">
                            <t-button theme="primary" @click="addMatchedJob(item)">申请职位</t-button>
                        </div>
                    </div>
                </div>
                <t-button theme="primary" variant="outline" @click="showMatchResults = false">关闭</t-button>
            </div>
        </template>
        <template v-else>
            <div class="no-matches">
                <t-empty description="暂无匹配结果" />
            </div>
        </template>
    </t-drawer>

    <div class="resume-page">
        <!-- <el-row>
            <div class="breadcrumb">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                    <el-breadcrumb-item>模拟面试</el-breadcrumb-item>
                </el-breadcrumb>
            </div>
        </el-row> -->

        <el-row>
            <el-col :span="24">
                <!-- 修正：绑定当前步骤的值 -->
                <el-steps :active="activeStep" simple class="steps-container">
                    <el-step title="选择简历" :icon="Edit" />
                    <el-step title="岗位匹配" :icon="Upload" />
                    <el-step title="问题配置" :icon="ChatDotSquare" />
                    <el-step title="面试配置" :icon="Picture" />
                </el-steps>
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="24">
                <!-- 根据当前步骤显示不同内容 -->
                <div v-if="activeStep === 1">
                    <!-- <t-row justify="center" style="margin-bottom: 30px;">
                        <t-col :span="12">
                            <h1 class="page-title">😎 选一份你最"得意"的简历吧，让 AI 更懂你！</h1>
                        </t-col>
                    </t-row> -->

                    <t-row justify="center" :gutter="16">
                        <t-col :span="4">
                            <t-card class="resume-list-card">
                                <div class="resume-container">
                                    <el-scrollbar height="69.5vh">
                                        <div class="card-list">
                                            <div v-if="!userStore.user.email">{{ resumeStore.resumeMsg }}</div>
                                            <t-card v-for="resume in resumeStore.resumeList" :key="resume.name"
                                                :title="resume.name" :cover="resume.preview"
                                                :style="{ width: '22vh', cursor: 'pointer', flexShrink: 0 }"
                                                :class="{ 'selected-card': selectedResumeName === resume.name }"
                                                @click="handleSelectResume(resume)" class="resume-item-card" />
                                        </div>
                                    </el-scrollbar>
                                </div>
                            </t-card>
                        </t-col>
                        <t-col :span="8">
                            <MdEditor v-model="resumeMarkDown" style="height: 73vh;" class="md-editor-container" />
                        </t-col>
                    </t-row>
                </div>

                <div v-else-if="activeStep === 2">
                    <!-- 岗位匹配按钮 -->
                    <t-row justify="center">
                        <t-col :span="12">
                            <div class="match-container">
                                <h2 class="match-title">🔍 基于你的技能标签匹配最适合的岗位</h2>
                                <div class="tags-container">
                                    <span class="tags-label">你的技能标签:</span>
                                    <div class="tags-list">
                                        <t-tag v-for="(tag, index) in hightWeightTags.split('，')" :key="index"
                                            theme="primary" variant="light" class="skill-tag">
                                            {{ tag }}
                                        </t-tag>
                                    </div>
                                </div>
                                <t-button theme="primary" :loading="isMatchingJobs" @click="matchJobs"
                                    class="match-button">
                                    <template #icon><t-icon name="search" /></template>
                                    {{ isMatchingJobs ? '匹配中...' : '开始岗位匹配' }}
                                </t-button>
                                <t-loading :loading="isMatchingJobs" fullscreen size="large">
                                    <template #indicator>
                                        <div class="my-dots-jump-spinner">
                                            <span class="dot"></span>
                                            <span class="dot"></span>
                                            <span class="dot"></span>
                                        </div>
                                    </template>
                                </t-loading>
                            </div>
                        </t-col>
                    </t-row>

                    <!-- 左侧岗位菜单 -->
                    <el-row justify="center">
                        <el-col :span="7">
                            <el-scrollbar height="75vh">
                                <div class="job-list-container">
                                    <!-- 新增岗位 -->
                                    <el-button class="add-job-button" @click="addJobDialogVisible = true">
                                        <el-icon>
                                            <CirclePlus />
                                        </el-icon>添加岗位
                                    </el-button>

                                    <el-card v-for="(job, index) in jobs" :key="index" shadow="hover"
                                        @click="handleSelect(index.toString(), $event)" class="job-card">
                                        <div class="job-card-header">
                                            <div class="job-title">{{ job.title }} <span
                                                    style="color: rgb(0, 82, 217);">{{
                                                        job.similarity == 0 ? '' : job.similarity + '%匹配度' }}</span></div>
                                            <div class="job-salary">{{ job.salary }}</div>
                                        </div>
                                        <div class="job-requirements">
                                            <span>{{ job.experience }}</span>
                                            <span>{{ job.education }}</span>
                                        </div>
                                        <div class="job-footer">
                                            <span class="job-company">
                                                <el-icon>
                                                    <OfficeBuilding />
                                                </el-icon>{{ job.company }}
                                            </span>
                                            <span class="job-location">
                                                <el-icon>
                                                    <Location />
                                                </el-icon>{{ job.location }}
                                            </span>
                                        </div>
                                    </el-card>
                                </div>
                            </el-scrollbar>
                        </el-col>

                        <!-- 右侧岗位详情 -->
                        <el-col :span="17">
                            <el-scrollbar height="75vh">
                                <el-card shadow="never" class="job-detail-card">
                                    <!-- 职位名称和薪资 -->
                                    <div class="job-detail-header">
                                        <div class="job-detail-title">
                                            {{ form.title || '未填写职位名称' }}
                                        </div>
                                        <div class="job-detail-salary">
                                            {{ form.salary || '薪资待定' }}
                                        </div>
                                    </div>

                                    <!-- 工作经验、学历、地点 -->
                                    <div class="job-detail-info">
                                        <span>
                                            <el-icon>
                                                <Location />
                                            </el-icon>&nbsp;{{ form.location || '工作地点未填写' }}
                                        </span>
                                        <span>
                                            <el-icon>
                                                <Suitcase />
                                            </el-icon>&nbsp;{{ form.experience || '经验不限' }}
                                        </span>
                                        <span>
                                            <el-icon>
                                                <School />
                                            </el-icon>&nbsp;{{ form.education || '学历不限' }}
                                        </span>
                                    </div>

                                    <el-divider />

                                    <!-- 岗位职责 -->
                                    <div class="job-detail-description">
                                        <vue3-markdown-it :source="form.description" />
                                    </div>

                                    <!-- 公司名称和地点 -->
                                    <div class="job-detail-footer">
                                        <span>{{ form.company || '公司名称未填写' }}</span>
                                        <span>{{ form.location || '工作地点未填写' }}</span>
                                    </div>

                                    <el-divider />
                                    <!-- 地图 -->
                                    <baidu-map class="map" ak="IpbDCp37pH66sx3Hxv7sbDmyv7qLlM7X" v="3.0" type="API"
                                        :center="form.location + form.company + '公司'" :zoom="17" />
                                </el-card>
                            </el-scrollbar>
                        </el-col>
                    </el-row>
                </div>
                <div v-else-if="activeStep === 3">
                    <question-type-config/>
                </div>
                <div v-else-if="activeStep === 4">
                    <t-row :gutter="16" justify="center">
                        <t-col :span="5">
                            <t-card class="interview-info-card">
                                <t-image src="/public/img/interview_config_bg.jpg" :gallery="true" fit="cover"
                                    shape="round" class="interview-image" />
                                <div class="interview-info-content">
                                    <h1 class="interview-info-title">AI模拟面试</h1>

                                    <div class="interview-info-item">
                                        <div class="interview-info-check">
                                            <div class="check-icon">✓</div>
                                            <p class="check-text">模拟面试将由AI担任面试官向你进行提问，
                                                模拟一次完整的面试过程。</p>
                                        </div>
                                    </div>

                                    <div class="interview-info-item">
                                        <div class="interview-info-check">
                                            <div class="check-icon">✓</div>
                                            <h2 class="check-title">面试配置</h2>
                                        </div>
                                        <p class="check-description">首先，请按需配置这次模拟面试的相关参数；</p>
                                    </div>

                                    <div class="interview-info-item">
                                        <div class="interview-info-check">
                                            <div class="check-icon">✓</div>
                                            <h2 class="check-title">设备测试</h2>
                                        </div>
                                        <p class="check-description">然后，进行「麦克风测试」与「摄像头测试」确保设备正常，智能体才能正常运行。</p>
                                    </div>

                                    <div class="interview-info-item">
                                        <div class="interview-info-check">
                                            <div class="check-icon">✓</div>
                                            <h2 class="check-title">开始面试</h2>
                                        </div>
                                        <p class="check-description">最后，录音确认无误后，即可「开始面试」。</p>
                                    </div>
                                </div>
                            </t-card>
                        </t-col>

                        <t-col :span="1"></t-col>

                        <t-col :span="5">
                            <t-card class="interview-config-card">
                                <t-row justify="center">
                                    <h1 class="config-title">AI模拟面试配置</h1>
                                </t-row>

                                <t-row justify="center">
                                    <p class="config-subtitle">请选择面试官、音色、面试风格、摄像头以及麦克风。</p>
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <!-- 面试官选择 -->
                                        <div class="config-item">
                                            <t-select v-model="interviewerValue" :options="interviewerOptions"
                                                @change="interviewerChange" placeholder="-请选择面试官角色-"
                                                class="config-select" />
                                        </div>
                                    </t-col>
                                    <t-col :span="1">
                                        <div class="check-status">
                                            <t-icon name="check-circle-filled" v-if="interviewerIsTrue"
                                                class="check-icon-success" />
                                        </div>
                                    </t-col>
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <!-- 音色选择 -->
                                        <div class="config-item">
                                            <t-select v-model="vcnValue" :options="vcnOptions" @change="vcnChange"
                                                placeholder="-请选择面试官音色-" class="config-select" />
                                        </div>
                                    </t-col>
                                    <t-col :span="1">
                                        <div class="check-status">
                                            <t-icon name="check-circle-filled" v-if="vcnIsTrue"
                                                class="check-icon-success" />
                                        </div>
                                    </t-col>
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <!-- 风格选择 -->
                                        <div class="config-item">
                                            <t-select v-model="styleValue" :options="styleOptions" @change="styleChange"
                                                placeholder="-请选择面试风格-" class="config-select" />
                                        </div>
                                    </t-col>
                                    <t-col :span="1">
                                        <div class="check-status">
                                            <t-icon name="check-circle-filled" v-if="styleIsTrue"
                                                class="check-icon-success" />
                                        </div>
                                    </t-col>
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <!-- 摄像头选择 -->
                                        <div class="config-item">
                                            <t-select v-model="selectedVideoDeviceId" :options="videoOptions"
                                                @change="handleVideoChange" placeholder="选择摄像头" class="config-select" />
                                        </div>
                                    </t-col>
                                    <t-col :span="1">
                                        <div class="check-status">
                                            <t-icon name="check-circle-filled" v-if="videoAvailable"
                                                class="check-icon-success" />
                                        </div>
                                    </t-col>
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <!-- 麦克风选择 -->
                                        <div class="config-item">
                                            <t-select v-model="selectedAudioDeviceId" :options="audioOptions"
                                                @change="handleAudioChange" placeholder="选择麦克风" class="config-select" />
                                        </div>
                                    </t-col>
                                    <t-col :span="1">
                                        <div class="check-status">
                                            <t-icon name="check-circle-filled" v-if="audioAvailable"
                                                class="check-icon-success" />
                                        </div>
                                    </t-col>
                                </t-row>

                                <t-row class="config-row" justify="center">
                                    <!-- <t-col :span="1"></t-col> -->
                                    <t-col>
                                        <!-- 摄像头预览 -->
                                        <video ref="videoPreview" autoplay muted playsinline width="300" height="240"
                                            class="video-preview" />
                                    </t-col>
                                    <!-- <t-col :span="1"></t-col> -->
                                </t-row>

                                <t-row class="config-row">
                                    <t-col :span="1"></t-col>
                                    <t-col :span="10">
                                        <t-button block theme="primary" @click="handleStartInterview"
                                            class="start-interview-button">
                                            <template #icon><play-circle-icon /></template>
                                            开始面试
                                        </t-button>
                                    </t-col>
                                    <t-col :span="1"></t-col>
                                </t-row>
                            </t-card>
                        </t-col>
                    </t-row>
                </div>
            </el-col>
        </el-row>

        <!-- 新增按钮容器 -->
        <div class="button-container">
            <t-button theme="default" @click="prevStep" :disabled="prevDisabled" class="step-button">上一步</t-button>
            <t-button theme="primary" class="step-button" @click="nextStep" :disabled="nextDisabled">下一步</t-button>
        </div>
    </div>
</template>

<style scoped>
.resume-page {
    background-color: #f5f7fa;
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.steps-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
}

.page-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
    color: #0052d9;
    font-weight: 600;
}

.resume-list-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.resume-container {
    width: 100%;
    padding: 0;
    box-sizing: border-box;
}

.card-list {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    padding: 8px;
}

.resume-item-card {
    transition: all 0.3s ease;
    border-radius: 8px;
}

.resume-item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.selected-card {
    border: 2px solid #0052d9;
    box-shadow: 0 0 12px rgba(0, 82, 217, 0.5);
}

.md-editor-container {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 岗位匹配样式 */
.match-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    text-align: center;
}

.match-title {
    color: #0052d9;
    font-size: 20px;
    margin-bottom: 16px;
}

.tags-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 16px;
}

.tags-label {
    font-weight: 600;
    margin-bottom: 8px;
}

.tags-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    max-width: 1000px;
}

.skill-tag {
    margin: 4px;
}

.match-button {
    padding: 0 24px;
    height: 40px;
    font-size: 16px;
}

/* 岗位列表样式 */
.job-list-container {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.add-job-button {
    height: 50px;
    background-color: #0052d9;
    color: white;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.add-job-button:hover {
    background-color: #003db3;
}

.job-card {
    cursor: pointer;
    background-color: white;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    border-radius: 8px;
    overflow: hidden;
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.job-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.job-title {
    font-weight: bold;
    font-size: 16px;
    color: #303133;
}

.job-salary {
    color: #0052d9;
    font-weight: bold;
}

.job-requirements {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 14px;
    color: #606266;
}

.job-footer {
    margin-top: 12px;
    font-size: 14px;
    color: #909399;
    display: flex;
    justify-content: space-between;
}

.job-company,
.job-location {
    display: flex;
    align-items: center;
    gap: 4px;
}

/* 岗位详情样式 */
.job-detail-card {
    background-color: white;
    transition: 0.3s;
    margin-top: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    min-height: 73vh;
}

.job-detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.job-detail-title {
    font-weight: bold;
    font-size: 20px;
    color: #303133;
}

.job-detail-salary {
    color: #0052d9;
    font-weight: bold;
    font-size: 18px;
}

.job-detail-info {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 14px;
    color: #606266;
    margin-bottom: 16px;
}

.job-detail-description {
    font-size: 14px;
    color: #606266;
    margin-bottom: 16px;
    line-height: 1.6;
}

.job-detail-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    color: #909399;
}

.map {
    width: 100%;
    height: 300px;
    border-radius: 8px;
    overflow: hidden;
}

/* 面试配置样式 */
.interview-info-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    height: 80vh;
}

.interview-image {
    border-radius: 8px;
    margin-bottom: 16px;
}

.interview-info-content {
    color: black;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.interview-info-title {
    font-size: 28px;
    margin-bottom: 20px;
    color: #0052d9;
    text-align: center;
}

.interview-info-item {
    margin-bottom: 16px;
}

.interview-info-check {
    display: flex;
    align-items: flex-start;
    margin-bottom: 8px;
}

.check-icon {
    color: #0ABF5B;
    font-size: 20px;
    margin-right: 12px;
    font-weight: bold;
}

.check-title {
    margin: 0;
    font-size: 18px;
    color: #303133;
}

.check-text {
    margin: 0;
    line-height: 1.5;
    color: #606266;
}

.check-description {
    margin-left: 32px;
    color: #606266;
    line-height: 1.5;
}

.interview-config-card {
    height: 80vh;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.config-title {
    color: #0052d9;
    font-size: 24px;
    margin-bottom: 16px;
}

.config-subtitle {
    color: #606266;
    text-align: center;
    margin-bottom: 24px;
}

.config-row {
    margin-bottom: 20px;
}

.config-item {
    display: flex;
    align-items: center;
}

.config-select {
    width: 100%;
}

.check-status {
    margin-left: 10px;
}

.check-icon-success {
    color: #0ABF5B;
}

.video-preview {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.start-interview-button {
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}

/* 按钮容器样式 */
.button-container {
    margin-top: auto;
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 20px 0;
}

.step-button {
    width: 250px;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.step-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 匹配结果样式 */
.matched-jobs-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.matched-job-card {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.matched-job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.matched-job-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.matched-job-title {
    font-size: 20px;
    font-weight: bold;
    color: #303133;
}

.matched-job-similarity {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
}

.similarity-text {
    font-size: 14px;
    font-weight: 600;
    color: #0052d9;
}

.matched-job-details {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.matched-job-info {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #606266;
}

.matched-job-company {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
}

.matched-job-description {
    color: #606266;
    line-height: 1.6;
}

.matched-job-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 16px;
}

.no-matches {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
}

.el-row {
    margin-bottom: 20px;
}

.breadcrumb {
    background-color: white;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.my-dots-jump-spinner .dot {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin: 0 2px;
    border-radius: 50%;
    background-color: #409EFF;
    animation: jump 1s infinite ease-in-out;
}

.my-dots-jump-spinner .dot:nth-child(2) {
    animation-delay: 0.2s;
}

.my-dots-jump-spinner .dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes jump {

    0%,
    80%,
    100% {
        transform: scaleY(1);
    }

    40% {
        transform: scaleY(1.6);
    }
}
</style>

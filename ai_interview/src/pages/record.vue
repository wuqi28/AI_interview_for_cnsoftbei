<template>
    <div class="interview-record-page">
        <div class="breadcrumb">
            <t-breadcrumb>
                <t-breadcrumb-item to="/">首页</t-breadcrumb-item>
                <t-breadcrumb-item>面试记录</t-breadcrumb-item>
            </t-breadcrumb>
        </div>

        <div class="content-container">
            <t-card title="我的面试记录" subtitle="查看您的历史面试详情" class="record-card" hover>
                <template #actions>
                    <t-space>
                        <t-button theme="primary" variant="text" @click="refreshRecords">
                            <template #icon><t-icon name="refresh" /></template>
                            刷新
                        </t-button>
                    </t-space>
                </template>

                <t-table :data="paginatedData" :columns="columns" row-key="id" hover stripe :loading="loading"
                    class="record-table">
                    <template #company="{ row }">
                        <div class="company-cell">
                            <t-avatar size="small" :image="getCompanyLogo(row.company)" />
                            <span class="company-name">{{ row.company }}</span>
                        </div>
                    </template>

                    <template #position="{ row }">
                        <t-tag theme="success" variant="light">{{ row.position }}</t-tag>
                    </template>

                    <template #interview_style="{ row }">
                        <t-tag theme="primary" variant="light">{{ row.interview_style }}</t-tag>
                    </template>

                    <template #start_time="{ row }">
                        <div class="time-cell">
                            <t-icon name="time" size="small" />
                            <span>{{ formatDateTime(row.start_time) }}</span>
                        </div>
                    </template>

                    <template #spend_time="{ row }">
                        {{ formatTimeHMS(row.spend_time) }}
                    </template>

                    <template #operation="{ row }">
                        <t-space>
                            <t-button theme="primary" size="small" variant="outline" @click.stop="viewDetail(row)">
                                <template #icon><t-icon name="browse" /></template>
                                查看详情
                            </t-button>
                        </t-space>
                    </template>
                </t-table>

                <div class="pagination-container" v-if="recordList.length > 0">
                    <t-pagination v-model="pagination.current" v-model:pageSize="pagination.pageSize"
                        :total="recordList.length" :page-size-options="[5, 10, 20, 50]" show-total show-jumper
                        show-page-size-options @change="onPageChange" @page-size-change="onPageSizeChange" />
                </div>
            </t-card>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axiosLocal from '@/modules/axiosLocal';
import { useUserStore } from '@/stores/userStore';
import { useInterviewStore } from '@/stores/interviewStore';
import { MessagePlugin } from 'tdesign-vue-next';
import { useRouter } from 'vue-router'

const router = useRouter()

const userStore = useUserStore();
const interviewStore = useInterviewStore();
const recordList = ref([]);
const loading = ref(false);

// 分页状态
const pagination = ref({
    current: 1,
    pageSize: 10,
});

// 表格列配置
const columns = [
    {
        colKey: 'company',
        title: '公司',
        width: 180,
    },
    {
        colKey: 'position',
        title: '岗位',
        width: 180,
    },
    {
        colKey: 'interviewer_name',
        title: '面试官',
        width: 120,
    },
    {
        colKey: 'interview_style',
        title: '面试风格',
        width: 200,
    },
    {
        colKey: 'start_time',
        title: '开始时间',
        width: 180,
    },
    {
        colKey: 'spend_time',
        title: '用时',
        width: 100,
    },
    {
        colKey: 'operation',
        title: '操作',
        fixed: 'right',
        width: 140,
    },
];

// 格式化日期和时间
const formatDateTime = (dateTimeStr) => {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    });
};

// 格式化时长为 HH:MM:SS 格式
const formatTimeHMS = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    return [
        hours.toString().padStart(2, '0'),
        minutes.toString().padStart(2, '0'),
        remainingSeconds.toString().padStart(2, '0')
    ].join(':');
};

// 获取公司logo（占位函数）
const getCompanyLogo = (company) => {
    // 这里理想情况下应该替换为实际的公司logo
    // 目前返回基于公司名称的占位图像
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(company)}&background=random&color=fff`;
};

// 查看面试详情
const viewDetail = (row) => {
    //   console.log('查看详情:', row);
    //   console.log('Email:', userStore.user.email);
    //   console.log('Interview ID:', row.current_interview_id);
    interviewStore.setCurrentInterviewId(row.current_interview_id)
    router.push('/report')


    //   MessagePlugin.info(`正在查看面试记录: ${row.company} - ${row.position}`);
};

// 分页处理函数
const onPageChange = (pageInfo) => {
    pagination.value.current = pageInfo.current;
};

const onPageSizeChange = (pageSize) => {
    pagination.value.pageSize = pageSize;
    pagination.value.current = 1; // 更改页面大小时重置到第一页
};

// 刷新记录
const refreshRecords = () => {
    getInterviewRecord();
};

// 获取面试记录
const getInterviewRecord = () => {
    loading.value = true;
    // recordList.value = interviewStore.interview_record_list.map(record => {
    //     const parts = record.current_interview_id.split('-');
    //     return {
    //         ...record,
    //         company: parts[0] || '未知公司',
    //         position: parts.length > 1 ? parts[1] : '未知岗位'
    //     };
    // });
    // loading.value = false;

      axiosLocal.get('/interview/get_interview_record_by_email', {
        params: {
          email: userStore.user.email
        }
      }).then((res) => {
        if (res.data.code === 200) {
        //   console.log(res.data.data);
          // 解析面试ID以提取公司和职位
          recordList.value = res.data.data.map(record => {
            const parts = record.current_interview_id.split('-');
            return {
              ...record,
              company: parts[0] || '未知公司',
              position: parts.length > 1 ? parts[1] : '未知岗位'
            };
          });
        //   MessagePlugin.success('面试记录获取成功');
        } else {
          MessagePlugin.error('获取面试记录失败');
        }
      }).catch((error) => {
        console.error('获取面试记录出错:', error);
        MessagePlugin.error('获取面试记录出错');
      }).finally(() => {
        loading.value = false;
      });
};

// 获取分页数据
const paginatedData = computed(() => {
    const start = (pagination.value.current - 1) * pagination.value.pageSize;
    const end = start + pagination.value.pageSize;
    return recordList.value.slice(start, end);
});

onMounted(() => {
    getInterviewRecord();
});
</script>

<style scoped>
.interview-record-page {
    background-color: rgb(245, 247, 250);
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.breadcrumb {
    margin-bottom: 20px;
}

.content-container {
    flex: 1;
}

.record-card {
    box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    transition: all 0.3s ease;
}

.record-table {
    margin-top: 16px;
    height: 70vh;
}

.company-cell {
    display: flex;
    align-items: center;
    gap: 8px;
}

.company-name {
    font-weight: 500;
}

.time-cell {
    display: flex;
    align-items: center;
    gap: 6px;
    color: rgba(0, 0, 0, 0.6);
}

.empty-state {
    padding: 60px 0;
    display: flex;
    justify-content: center;
}

.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}

/* 行悬停动画 */
:deep(.t-table__row) {
    transition: all 0.2s ease-in-out;
}

:deep(.t-table__row:hover) {
    transform: translateY(-2px);
}
</style>

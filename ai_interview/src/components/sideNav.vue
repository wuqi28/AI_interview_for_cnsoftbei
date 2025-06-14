<template>
  <div class="sidebar-container">
    <t-menu theme="light" :default-value="pageStore.pageIndex" collapsed @change="handleChange">
      <template #logo>
        <div class="logo-container">
          <img :width="36" :src="iconUrl" alt="logo" />
        </div>
      </template>

      <t-menu-group>
        <t-menu-item value="1" to="/interview" class="menu-item">
          <template #icon>
            <t-icon name="desktop" class="menu-icon" />
          </template>
          AI模拟面试
        </t-menu-item>

        <div style="height: 10px;"></div>

        <t-menu-item value="2" to="/resume" class="menu-item">
          <template #icon>
            <t-icon name="file" class="menu-icon" />
          </template>
          AI简历生成
        </t-menu-item>
        <div style="height: 10px;"></div>

        <t-menu-item value="3" to="/interviewRecord" class="menu-item">
          <template #icon>
            <t-icon name="chart" class="menu-icon" />
          </template>
          面试记录
        </t-menu-item>

        <div style="height: 10px;"></div>
        
        <t-menu-item value="4" to="/exercise" class="menu-item">
          <template #icon>
            <t-icon name="book" class="menu-icon" />
          </template>
          个性化习题推荐
        </t-menu-item>

        <div style="height: 10px;"></div>
        
        <t-menu-item value="5" class="menu-item">
          <template #icon>
            <t-icon name="star" class="menu-icon" />
          </template>
          智能推荐
        </t-menu-item>
      </t-menu-group>

      <template #operations>
        <div class="operations-container">
          <t-tooltip content="登录" placement="right" show-arrow>
            <t-button variant="text" shape="square" @click="loginVisible = true" class="login-button">
              <template #icon><t-icon name="user" /></template>
            </t-button>
          </t-tooltip>
          
          <t-tooltip content="设置" placement="right" show-arrow>
            <t-button variant="text" shape="square" class="settings-button">
              <template #icon><t-icon name="setting" /></template>
            </t-button>
          </t-tooltip>
        </div>
      </template>
    </t-menu>
  </div>

  <t-dialog :footer="false" placement="center" v-model:visible="loginVisible" class="login-dialog">
    <t-image fit="cover" position="center" src="../../public/img/logo_chinese.png" :style="{ height: '80px' }" />
    <div style="height: 30px;"></div>
    <t-form ref="form" :data="formData" :colon="true" :label-width="0" @reset="onReset" @submit="onSubmit">
      <t-form-item name="email">
        <t-input v-model="formData.email" clearable placeholder="请输入邮箱">
          <template #prefix-icon>
            <t-icon name="mail" />
          </template>
        </t-input>
      </t-form-item>

      <t-form-item name="password">
        <t-input v-model="formData.password" type="password" clearable placeholder="请输入密码">
          <template #prefix-icon>
            <lock-on-icon />
          </template>
        </t-input>
      </t-form-item>

      <t-form-item>
        <t-button theme="primary" type="submit" block>登录</t-button>
      </t-form-item>
      <div style="height: 5px;"></div>

      <router-link to="/register">
        <p style="text-align: right; color: rgb(28, 97, 231); margin: 0; text-decoration: underline;">
          没有账号，前去注册 <t-icon name="arrow-right" />
        </p>
      </router-link>
    </t-form>
  </t-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { DesktopIcon, LockOnIcon } from 'tdesign-icons-vue-next';
import { usePageStore } from '../stores/pageStore';
import { NotifyPlugin } from 'tdesign-vue-next';
import axiosLocal from '../modules/axiosLocal';
import { useUserStore } from '../stores/userStore';
import { useResumeStore } from '../stores/resumeStore';
import { useInterviewStore } from '../stores/interviewStore';
import { useRouter } from 'vue-router';

const pageStore = usePageStore();
const userStore = useUserStore();
const resumeStore = useResumeStore();
const interviewStore = useInterviewStore();

const router = useRouter();

const iconUrl = ref('../../public/img/logo.png')

const loginVisible = ref(false)

const handleChange = (active) => {
  console.log('当前选中菜单：', active)
  pageStore.pageIndex = active;
}

const formData = reactive({
  email: '',
  password: '',
});

const onReset = () => {
  MessagePlugin.success('重置成功');
};

const onSubmit = () => {
  if (!formData.email || !formData.password) {
    NotifyPlugin.error({ title: '错误通知', content: '请输入邮箱或密码!' });
    return;
  }
  axiosLocal.post('/user/login', formData)
    .then((res) => {
      if (res.data.code === 200) {
        NotifyPlugin.success({ title: '成功通知', content: '登录成功' });
        loginVisible.value = false;
        let user = res.data.data;
        userStore.setUser(user);
        localStorage.setItem('user', JSON.stringify(user))
        getResumeList();
        getInterviewRecordByEmail();
        resumeStore.setResumeMsg("");
      }
    })
};

const getResumeList = () => {
  axiosLocal.get('/resume/get_resume', { params: { email: userStore.user.email } })
    .then((res) => {
      // console.log(res.data);
      if (res.data.code == 200) {
        resumeStore.setResumeList(res.data.data);
      }
    })
}

const getInterviewRecordByEmail = () => {
  axiosLocal.get('/interview/get_interview_record_by_email', { params: { email: userStore.user.email } })
    .then((res) => {
      // console.log(res.data);
      if (res.data.code == 200) {
        interviewStore.setInterviewRecordList(res.data.data);
        // console.log(interviewStore.interview_record_list);
      }
    })
}

// 根据pageIndex的值自动跳转页面
onMounted(() => {
  if (pageStore.pageIndex === '1') {
    router.push('/interview');
  } else if (pageStore.pageIndex === '2') {
    router.push('/resume');
  } else if (pageStore.pageIndex === '3') {
    router.push('/interviewRecord');
  } else if (pageStore.pageIndex === '4') {
    router.push('/exercise');
  }
});
</script>

<style scoped>
.sidebar-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.menu-item {
  margin: 8px 0;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.menu-icon {
  font-size: 20px;
}

.operations-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;
  gap: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.login-button, .settings-button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.login-button:hover, .settings-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.login-dialog :deep(.t-dialog__body) {
  padding: 24px;
}

/* Override TDesign menu styles for better aesthetics */
:deep(.t-menu) {
  border-right: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

:deep(.t-menu__item) {
  margin: 4px 8px;
}

:deep(.t-menu__item.t-is-active) {
  background-color: rgba(0, 82, 217, 0.1);
  font-weight: 500;
}

:deep(.t-menu__item:hover) {
  background-color: rgba(0, 0, 0, 0.03);
}
</style>

<template>
  <t-menu theme="light" :default-value="pageStore.pageIndex" :collapsed="true" @change="handleChange">
    <template #logo>
      <img :width="40" :src="iconUrl" alt="logo" />
    </template>

    <t-menu-group title="功能导航">

      <t-menu-item value="1" to="/interview">
        <template #icon>
          <t-icon name="desktop" />
        </template>
        模拟面试
      </t-menu-item>
      <div style="height: 10px;"></div>

      <t-menu-item value="2" to="/resume">
        <template #icon>
          <t-icon name="file" />
        </template>
        个人简历
      </t-menu-item>
      <div style="height: 10px;"></div>

      <t-menu-item value="3">
        <template #icon>
          <t-icon name="folder" />
        </template>
        岗位信息
      </t-menu-item>
    </t-menu-group>


    <!-- <t-menu-group title="更多">
      <t-menu-item value="item3">
        <template #icon>
          <t-icon name="user" />
        </template>
        个人页
      </t-menu-item>
      <t-menu-item value="item4">
        <template #icon>
          <t-icon name="login" />
        </template>
        登录页
      </t-menu-item>
    </t-menu-group> -->

    <template #operations>
      <t-tooltip class="placement right-full align" content="登录" :overlay-style="{ width: '200px' }" placement="right"
        show-arrow>
        <t-button block variant="text" shape="square" @click="loginVisible = true">
          <template #icon><t-icon name="login" /></template>
        </t-button>
      </t-tooltip>
    </template>
  </t-menu>

  <!-- 登录对话框 -->
  <t-dialog :footer="false" placement="center" v-model:visible="loginVisible">
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

const pageStore = usePageStore();
const userStore = useUserStore();
const resumeStore = useResumeStore();

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
        // console.log("我是store的user ",userStore.user);
        getResumeList();
        resumeStore.setResumeMsg("");
      }
    })
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

// 根据pageIndex的值自动跳转页面
onMounted(() => {
  if (pageStore.pageIndex === '1') {
    router.push('/interview');
  } else if (pageStore.pageIndex === '2') {
    router.push('/resume');
  }
});


</script>

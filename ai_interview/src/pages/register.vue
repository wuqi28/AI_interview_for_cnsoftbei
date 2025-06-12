<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import axiosLocal from '../modules/axiosLocal';
import topNav from '../components/topNav.vue';
import { NotifyPlugin} from 'tdesign-vue-next';
import { useRouter } from 'vue-router';

const router = useRouter();

// 当前激活标签页默认设置为注册
const activeTab = ref('register');

// 注册表单数据
const registerForm = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  captcha: ''
});

// 验证码按钮状态
const captchaBtn = ref(false)

// 提交注册表单
const handleRegister = async () => {
  if (registerForm == null) return;
  // console.log(registerForm);
  axiosLocal.post('/user/register', registerForm).then(res => {
    if (res.data.code === 200) {
      NotifyPlugin.success({ title: '成功通知', content: '账号注册成功' });
      setTimeout(() => {
        router.push('/index'); // 注册成功后跳转到首页
      }, 1000); // 1秒后跳转到登录页面
    } else {
     console.log(res.data); 
    }
  })
  
};

const sendCaptcha = (buttonEl) => {
  if (!registerForm.email) {
    NotifyPlugin.warning({ title: '提示', content: '请先输入邮箱' });
    return;
  }
  axiosLocal.get('/user/getCaptcha', { params: { email: registerForm.email } })
    .then(res => {
      if (res.data.code === 200) {
        NotifyPlugin.success({ title: '成功通知', content: '发送成功' });

        // 启动倒计时
        let seconds = 60;
        // buttonEl.disabled = true;
        captchaBtn.value = true
        buttonEl.innerText = `${seconds}s`;

        const timer = setInterval(() => {
          seconds--;
          if (seconds > 0) {
            buttonEl.innerText = `${seconds}s`;
          } else {
            clearInterval(timer);
            // buttonEl.disabled = false;
            captchaBtn.value = false
            buttonEl.innerText = '获取验证码';
          }
        }, 1000);
      } else {
        NotifyPlugin.error({ title: '错误通知', content: '验证码发送失败' });
      }
    })
    .catch(() => {
      NotifyPlugin.error({ title: '错误通知', content: '发送异常，请稍后重试' });
    });
};

</script>

<template>
  <topNav />
  <div class="register-container">
    <t-row>
      <t-col :span="12">
        <div style="width: 50vh; text-align: center;">
          <iframe src="../../public/earth.html" frameborder="0" style="height: 25vh; width: 25vh;"></iframe>
        </div>
        <t-card class="register-card">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="注册" name="register">
              <el-form :model="registerForm" label-width="80px">
                <el-form-item label="邮箱" prop="email">
                  <t-input v-model="registerForm.email" placeholder="请输入邮箱"></t-input>
                </el-form-item>
                <el-form-item label="验证码" prop="captcha">
                  <t-input v-model="registerForm.captcha" placeholder="请输入验证码">
                    <template #suffix>
                      <t-button size="small" variant="text" @click="(e) => sendCaptcha(e.currentTarget)" :disabled="captchaBtn">获取验证码</t-button>
                    </template>
                  </t-input>

                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <t-input v-model="registerForm.password" type="password" placeholder="请输入密码"></t-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                  <t-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码"></t-input>
                </el-form-item>
              </el-form>
              <t-button theme="primary" @click="handleRegister" style="width: 100%;">注册</t-button>
            </el-tab-pane>
          </el-tabs>
        </t-card>
      </t-col>
    </t-row>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  padding-top: 5vh;
  min-height: 89vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 50vh;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 5vh;
}
</style>

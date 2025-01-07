<template>
  <div>
    <button @click="loginWithDouyin">扫码登录抖音</button>
    <div v-if="userInfo">
      <div style="height: 200px;width: 360px;border-radius: 20px;">
        <img style="width: 100px; height: 100px;border-radius: 50%;" :src="userInfo.avatar" alt="头像" />
        <p style="color: black;">昵称: {{ userInfo.nickname }}</p>  
      </div>
    </div>
  </div>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  name: 'DouyinLogin',
  setup() {
    const router = useRouter();
    const userInfo = ref(null);

    const loginWithDouyin = () => {
      const clientKey = 'awnqhtekw8itxr5p';
      const redirectUri = 'https://localhost:5173'; // 替换为你的回调URL
      const scope = 'user_info,trial.whitelist';

      const loginUrl = `https://open.douyin.com/platform/oauth/connect/?client_key=${clientKey}&response_type=code&scope=${scope}&redirect_uri=${encodeURIComponent(redirectUri)}`;
      window.location.href = loginUrl; // 重定向到抖音登录
    };

    const getAccessToken = async (code) => {
      const clientKey = 'awnqhtekw8itxr5p';
      const clientSecret = '22af238b2f84a2c7c706a7cab5c82300';

      try {
        const response = await axios.post('/api/oauth/access_token/', {
          client_key: clientKey,
          client_secret: clientSecret,
          code: code,
          grant_type: 'authorization_code',
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        console.log('响应数据:', JSON.stringify(response.data));
        if (response && response.data && response.data.data) {
          const accessToken = response.data.data.access_token;
          const openId = response.data.data.open_id;
          if (accessToken && openId) {
            await getUserInfo(accessToken, openId);
            console.log('响应数据:', accessToken);
          } else {
            console.error('access_token 不存在');
          }
        } else {
          console.error('响应数据为空或格式不正确');
        }
      } catch (error) {
        console.error('获取 access token 失败:', error.response ? error.response.data : error);
      }
    };

    const getUserInfo = async (accessToken, openId) => {
      try {
        const response = await axios.get('/api/oauth/userinfo/', {
          params: {
            access_token: accessToken,
            open_id: openId
          }
        });
        console.log('响应数据:', JSON.stringify(response.data));
        userInfo.value = response.data.data; // 更新用户信息
        router.push('/home')
      } catch (error) {
        console.error('获取用户信息失败:', error.response ? error.response.data : error);
      }
    };

    const handleRedirect = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code'); // 获取code参数
      console.log('测试code:', code);
      if (code) {
        await getAccessToken(code);
      }
    };

    return {
      userInfo,
      loginWithDouyin,
      handleRedirect,
    };
  },
  mounted() {
    this.handleRedirect(); // 处理重定向逻辑
  },
};
</script>

<style scoped>
/* 你的样式 */
</style>
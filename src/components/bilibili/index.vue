<template>
  <div class="minimal-container">
    <!-- 左侧介绍 -->
    <div class="minimal-intro">
      <div class="branding">
        <img src="@/assets/img/logo.png" alt="项目Logo" class="logo" />
        <h1>短视频文本评论动态分析系统</h1>
        <p class="subtitle">基于哔哩哔哩视频文本评论分析</p>
      </div>
    </div>

    <!-- 右侧登录 -->
    <div class="minimal-login">
      <div class="login-panel">
        <h2 class="login-title">扫码登录</h2>
        <div class="qrcode-container">
          <transition name="fade">
            <img 
              v-if="qrUrl" 
              :src="qrUrl" 
              alt="登录二维码"
              class="qrcode-image"
            />
          </transition>
          <div v-if="!qrUrl" class="loading-indicator"></div>
        </div>
        <p class="status-text">{{ statusMessage }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.minimal-container {
  display: flex;
  min-height: 100vh;
}

/* 左侧介绍 */
.minimal-intro {
  flex: 1;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.branding {
  margin-bottom: 80px;
  text-align: center;
}

.logo {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
}

.branding h1 {
  font-size: 2.2rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  font-size: 1rem;
}



/* 右侧登录 */
.minimal-login {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-panel {
  width: 100%;
  max-width: 320px;
  text-align: center;
}

.login-title {
  font-weight: 600;
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 40px;
}

.qrcode-container {
  position: relative;
  margin: 0 auto;
  width: 200px;
  height: 200px;
  background: #f8f8f8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qrcode-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 12px;
  border-radius: 12px;
}

.loading-indicator {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 400% 100%;
  animation: loading 1.5s ease infinite;
  border-radius: 12px;
}

.status-text {
  text-align: center;
  margin-top: 24px;
  color: #666;
  font-size: 0.9rem;
}

.fade-enter-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 768px) {
  .minimal-container {
    flex-direction: column;
  }

  .minimal-intro {
    padding: 40px 24px;
    border-right: none;
    border-bottom: 1px solid #eee;
  }

  .branding {
    margin-bottom: 40px;
  }

  .minimal-login {
    padding: 60px 24px;
  }
}
</style>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  data() {
    return {
      qrUrl: "",
      qrKey: "",
      statusMessage: "请使用哔哩哔哩扫描二维码登录",
      user: null, // 确保 user 在 data 中定义
    };
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    return {
      router,
      store,
    };
  },
  async created() {
    await this.getQRCode();
  },
  methods: {
    async getQRCode() {
      try {
        const response = await axios.get("http://localhost:3000/api/get_qr_code");
        if (response.data.code === 0) {
          const encodedUrl = encodeURIComponent(response.data.data.url);
          this.qrUrl = "https://pan.misakamoe.com/qrcode/?url=" + encodedUrl;
          this.qrKey = response.data.data.qrcode_key;
          console.log("✅ 获取二维码成功，oauthKey:", this.qrKey);
          this.pollQRCode();
        } else {
          console.error("❌ 获取二维码失败，响应:", response.data);
        }
      } catch (error) {
        console.error("❌ 获取二维码失败:", error);
      }
    },
    async pollQRCode() {
      try {
        const response = await axios.post("http://localhost:3000/api/check_qr_code", {
          oauthKey: this.qrKey
        });

        if (response.data.data.code === 0) {
          console.log("🎉 登录成功:", response.data);
          this.statusMessage = "登录成功！";

          // 从响应中提取 URL
          const url = response.data.data.url;

          // 解析 URL 中的参数
          const urlParams = new URLSearchParams(new URL(url).search);

          // 提取 DedeUserID 和 SESSDATA
          const dedeUserID = urlParams.get("DedeUserID");
          const sessdata = urlParams.get("SESSDATA");

          if (!dedeUserID || !sessdata) {
            console.error("❌ 无法从 URL 中提取 DedeUserID 或 SESSDATA");
            return;
          }

          // 保存用户信息
          this.user = {
            DedeUserID: dedeUserID,
            SESSDATA: sessdata,
          };

          // console.log("用户信息:", this.user);

          // 调用获取用户信息的方法
          this.getUserInfo();
        } else if (response.data.code === 86038) {
          console.log("⌛ 等待扫码...");
          setTimeout(() => this.pollQRCode(), 1000);
        } else if (response.data.code === 86101) {
          console.log("📌 已扫码，等待用户确认...");
          setTimeout(() => this.pollQRCode(), 1000);
        } else if (response.data.data.code === 86038) {
          console.log("❌ 二维码已过期，重新获取");
        } else {
          console.log("❌ 未知错误:", response.data.data.message);
          setTimeout(() => this.pollQRCode(), 1000);
        }
      } catch (error) {
        console.error("❌ 二维码状态检查失败:", error);
      }
    },
    async getUserInfo() {
      try {
        const response = await axios.get("http://localhost:3000/api/user_info", {
          params: {
            DedeUserID: this.user.DedeUserID,
            SESSDATA: this.user.SESSDATA,
          },
          withCredentials: true, // 确保携带凭证
        });

        if (response.data.code === 0) {
          const userInfo = response.data.data;
          console.log("用户信息:", userInfo);

          // 将用户信息存储到 Vuex store
          this.store.dispatch('updateUserInfo', userInfo);

          // 设置 Cookie
          document.cookie = `DedeUserID=${this.user.DedeUserID}; path=/`;
          document.cookie = `SESSDATA=${this.user.SESSDATA}; path=/`;

          // 登录成功后重定向到 Main.vue
          this.router.push({ name: 'Main' });
        } else {
          console.error("获取用户信息失败:", response.data.message);
        }
      } catch (error) {
        console.error("获取用户信息失败:", error);
      }
    }
  },
};
</script>
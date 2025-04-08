<template>
  <div class="main">
    <nav class="navbar">
      <div v-if="userInfo" class="navbar-container">
        <!-- 这里显示用户头像 -->
        <div class="logo">
          <img 
            class="avator" 
            :src="`http://localhost:3000/api/proxy_image?url=${encodeURIComponent(userInfo.face)}`" 
            alt="头像" 
            @error="handleImageError"
            @click="showUserInfo"
          />
        </div>
        
        <!-- 弹窗展示用户信息 -->
        <div v-if="isUserInfoVisible" class="user-info-popup">
          <div class="user-info-content">
            <img 
              :src="`http://localhost:3000/api/proxy_image?url=${encodeURIComponent(userInfo.face)}`" 
              alt="头像" 
              class="popup-avatar"
            />
            <h3>{{ userInfo.uname }}</h3>
            <p>{{ userInfo.sign }}</p>
          </div>
        </div>
        
        <!--这里显示用户昵称-->
        <div class="title">
          <h1>{{userInfo.uname}}</h1>
        </div>
        
        <!-- 搜索框和搜索按钮 -->
        <div class="search-bar">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索视频"
            @keyup.enter="handleSearch"
          />
          <button @click="handleSearch">搜索</button>
        </div>
        
        <!-- 菜单栏 -->
        <ul class="menu">
          <li><a href="#home" @click.prevent="router.push({ name: 'Home' })">首页</a></li>
         <li><a href="#mine" @click.prevent="router.push({ name: 'Mine' })">我的</a></li>
          <!-- <li>
            <a href="#analyse" @click.prevent="toggleSubMenu">内容分析</a>
            <ul v-if="isSubMenuVisible" class="sub-menu">
              <li><a href="#analyse1" @click.prevent="router.push({ name: 'Analyse' })">词云图</a></li>
              <li><a href="#analyse2">情感极性</a></li>
              <li><a href="#analyse2">性别占比</a></li>
              <li><a href="#analyse2">朴素贝叶斯</a></li>
              <li><a href="#analyse2">K-mean聚类</a></li>
            </ul>
          </li> -->
          <li><a href="#about" @click.prevent="router.push({ name: 'About' })">关于</a></li>
        </ul>
      </div>
    </nav>
    <div class="page">
      <router-view></router-view> <!-- 显示子路由组件 -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { computed, ref } from 'vue';

export default {
  name: 'Main',
  setup() {
    const router = useRouter();
    const store = useStore();
    const isUserInfoVisible = ref(false);
    const searchKeyword = ref("");
    const isSubMenuVisible = ref(false);

    // 从 Vuex store 获取用户信息
    const userInfo = computed(() => store.getters.userInfo);
    console.log("用户信息:", userInfo.value); // 打印完整的 userInfo 对象

    const showUserInfo = () => {
      // isUserInfoVisible.value = true;
      router.push({ name: 'Mine' })
    };

    const hideUserInfo = () => {
      isUserInfoVisible.value = false;
    };

    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        router.push({ name: 'Search', params: { keyword: searchKeyword.value } });
        searchKeyword.value = ""; // 清空输入框
      }
    };

    const toggleSubMenu = () => {
      isSubMenuVisible.value = !isSubMenuVisible.value;
    };

    return {
      userInfo,
      videoData: [],
      commentData: [],
      router, // 返回 router 对象以便在模板中使用
      isUserInfoVisible,
      showUserInfo,
      hideUserInfo,
      searchKeyword,
      handleSearch,
      isSubMenuVisible,
      toggleSubMenu,
    };
  },

  methods: {
    handleImageError(event) {
      console.error("图片加载失败:", event.target.src);
      console.log("尝试加载默认图片");
      event.target.src = "https://via.placeholder.com/400"; // 使用默认图片
    },
  }
};
</script>

<style scoped>
.main {
  margin: 0; /* 重置外边距 */
  padding: 0; /* 重置内边距 */
  width: 100%;
  height: 100vh; /* 设置为视口高度 */
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column; /* 垂直排列子元素 */
  overflow: hidden; /* 禁止外部滚动 */
}

.navbar {
  background-color: #fff;
  display: flex;
  border-bottom-color: #333;
  padding: 5px 5px;
  width: 100%;
  align-items: center;
  flex-shrink: 0; /* 禁止导航栏收缩 */
  position: sticky; /* 固定导航栏 */
  top: 0;
  z-index: 1000; /* 确保导航栏在最上层 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

.navbar-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.logo img {
  height: 40px;
  margin-left: 10px;
  margin-right: 10px;
}

.avator {
  width: 40px; /* 设置图片的宽度 */
  height: 40px; /* 设置图片的高度 */
  border-radius: 50%; /* 将图片裁剪为圆形 */
  object-fit: cover; /* 保持图片的宽高比并填充整个区域 */
  border: 1px solid #fff; /* 添加边框 */
}

.title h1 {
  font-size: 20px;
  margin: 0;
  margin-right: 5px;
  color: #333; /* 白色文字 */
  font-weight: 500; /* 加粗字体 */
}

.search-bar {
  height: 36px;
  display: flex;
  margin-left: auto;
  margin-right: 20px;
  position: relative;
}

.search-bar input {
  flex: 1;
  padding: 8px 40px 8px 10px; /* 调整内边距，为按钮留出空间 */
  border: 1px solid #ddd;
  border-radius: 36px;
  font-size: 14px;
  outline: none; /* 移除默认的聚焦边框 */
}

.search-bar button {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  padding: 0 12px;
  background-color: transparent;
  color: #fa7298;
  border: none;
  border-radius: 0 36px 36px 0;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-bar button:hover {
  background-color: rgba(250, 114, 152, 0.1)
  ;
}

.menu {
  list-style: none;
  display: flex;
  padding: 0;
  margin-left: auto;
  margin-right: 0;
  position: relative; /* 添加相对定位 */
}

.menu a {
  color: #333;
  text-decoration: none;
  font-size: 18px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.menu a:hover {
  background-color: rgba(250, 114, 152, 0.1);
  text-decoration: none;
}

.sub-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 100%; /* 调整位置，使其位于菜单项下方 */
  z-index: 1000;
  display: none; /* 默认隐藏 */
}

.menu li:hover .sub-menu {
  display: block; /* 鼠标悬停时显示 */
}

.sub-menu li {
  padding: 10px 10px;
}

.sub-menu a {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  display: block;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.sub-menu a:hover {
  background-color: rgba(250, 114, 152, 0.1);
}
.page {
  flex: 1;
  /* overflow-y: auto; */
  background-color: #fff;
}
</style>
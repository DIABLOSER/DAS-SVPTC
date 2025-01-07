<template>
    <div class="main">
      <nav class="navbar">
        <div class="navbar-container">
          <!-- Logo -->
          <div class="logo">
            <img class="avator" src="../../assets/img/logo3.png" alt="Logo" />
          </div>
          
          <!-- 标题 -->
          <div class="title">
            <h1>DAS-SVPTC</h1>
          </div>
          
          <!-- 菜单栏 -->
          <ul class="menu">
            <li><a href="" @click.prevent="this.router.push('/home')">首页</a></li>
            <li><a href="" @click.prevent="this.router.push('/about')">关于我们</a></li>
            <li><a href="" @click.prevent="this.router.push('/analyse')">服务</a></li>
            <li><a href="#contact">联系我们</a></li>
          </ul>
        </div>
      </nav>
      <div class="page">
        <h1>这是分析主页面</h1>
        <router-view></router-view>
      </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'MainNavbar',
    setup() {
      const router = useRouter();
      return {
        router,
      };
    },
    methods: {
      Intent_Analyse() {
        this.router.push('/analyse');
      },
      Intent_About() {
        this.router.push('/about');
      },
    },
  };
  </script>
  
  <style scoped>
  .main {
    width: 100%;
    height: 100vh;
  }
  .navbar {
    background-color: #FA7298;
    color: white;
    border-bottom-width: 10px;
    border-bottom-color: #333;
    padding: 10px 10px;
    display: flex;
    width: 100%;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3), -2px -2px 5px rgba(255, 255, 255, 0.7);
    position: absolute;
    justify-content: space-between;
    align-items: center;
  }
  
  .navbar-container {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .logo img {
    height: 40px;
    margin-right: 20px;
  }
  
  .avator {
    width: 40px; /* 设置图片的宽度 */
    height: 40px; /* 设置图片的高度 */
    border-radius: 50%; /* 将图片裁剪为圆形 */
    object-fit: cover; /* 保持图片的宽高比并填充整个区域 */
  }
  
  .title h1 {
    font-size: 24px;
    margin: 0;
    margin-right: 20px;
  }
  
  .menu {
    list-style: none;
    display: flex;
    margin: 0;
    padding: 0;
    margin-left: auto;
    margin-right: 0;
  }
  
  .menu li {
    margin-left: 20px;
  }
  
  .menu a {
    color: white;
    text-decoration: none;
    font-size: 18px;
  }
  
  .menu a:hover {
    text-decoration: underline;
  }
  
  .page {
    width: 100%;
    height: 100%;
  }
  </style>
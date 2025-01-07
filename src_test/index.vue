<template>
  <div class="main">
    <!-- 容器元素，用于展示页面内容 -->
    <div class="container">
      <!-- 页面标题 -->
      <h1>折现图</h1>
      <!-- 动态显示图表图片，当 plotUrl 存在时显示 -->
      <img v-if="plotUrl" :src="plotUrl" alt="Line Chart">
    </div>
  </div>
  </template>
  
  <script>
  import axios from 'axios';  // 引入 axios 库，用于发送 HTTP 请求
  
  export default {
    data() {
      return {
        // 存储图表图片的 URL
        plotUrl: null,
      };
    },
    mounted() {
      // 组件挂载后调用 fetchChart 方法获取图表数据
      this.fetchChart();
    },
    methods: {
      async fetchChart() {
        try {
          // 发送 GET 请求获取图表数据
          const response = await axios.get('https://127.0.0.1:5000/api/chart');
          // 打印响应数据到控制台
          console.log('Response data:', response.data);
          // 将返回的图表 URL 转换为 base64 格式并赋值给 plotUrl
          this.plotUrl = `data:image/png;base64,${response.data.plot_url}`;
        } catch (error) {
          // 捕获请求错误并打印到控制台
          console.error('Error fetching chart:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .main{
    display: flex;
    height: 100%; /* 确保容器有高度 */
            width: 100%;
            /* 水平剧中 */
            justify-content: center;
            /* 垂直居中 */
            align-items: center;
  }
  /* 定义容器的样式 */
  .container {
    background-color: #fff;
            width: auto;
            height: 60%;
            border-radius: 15px;
            padding: 0 50px;
  }
  </style>
<template>
  <div class="about-container">
    <div class="header">
      <h1>关于本项目</h1>
      <p>本项目致力于构建一个面向Bilibili短视频平台的评论数据动态分析系统，利用前后端分离架构，实现对用户评论内容的采集、处理与可视化展示，帮助用户更全面地了解视频下观众的反馈、舆情趋势及潜在热点内容。</p>
    </div>
    <div class="content">
      <div class="card">
        <h2>技术栈</h2>
        <ul>
          <li>前端：Vue3 + Element Plus + ECharts</li>
          <li>后端：Python Flask + Requests + SnowNLP</li>
        </ul>
      </div>
      <div class="card">
        <h2>项目地址</h2>
        <ul>
          <li>
            <a href="https://github.com/yourusername/your-repo" target="_blank">GitHub</a>
          </li>
          <!-- <li>
            <a href="https://blog.csdn.net/your_csdn" target="_blank">CSDN博客</a>
          </li> -->
        </ul>
      </div>
      <div class="card">
        <h2>联系方式</h2>
        <ul>
          <li>邮箱：<a >daboluo719@gmail.com</a></li>
          <li>学习交流群：<a>994140903</a></li>
        </ul>
      </div>
    </div>
    <!-- 底部 -->
    <div class="footer">
      <h2>免责声明</h2>
      <p>本项目仅供学术研究使用，所有数据均来自公开API，不涉及任何商业用途。如有任何问题，请联系作者删除。</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 20px 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.8rem;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: 600;
}

.header p {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin: 0 auto;
}

.content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 20px;
  flex: 1; /* 让内容区域占据剩余空间 */
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card h2 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 20px;
  font-weight: 600;
}

.card p {
  font-size: 1rem;
  color: #7f8c8d;
  line-height: 1.8;
}

.card ul {
  list-style-type: none;
  padding: 0;
}

.card ul li {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 10px;
  padding-left: 20px;
  position: relative;
}

.card ul li::before {
  content: '•';
  color: #FA7298;
  position: absolute;
  left: 0;
}

.card a {
  color: #FA7298;
  text-decoration: none;
  transition: color 0.3s ease;
}

.card a:hover {
  color: #FA7298;
}

.footer {
  flex: 1;
  text-align: center;
  padding: 20px;
  margin-top: auto; /* 让 footer 始终位于底部 */
}
</style>
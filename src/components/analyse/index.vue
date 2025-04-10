<template>
  <div class="video-detail">
    <div class="video-container">
      <!-- 侧边栏菜单 -->
      <div class="sidebar">
        <div class="menu-item" @click="switchChart('wordCloud')" :class="{ active: activeChart === 'wordCloud' }">
          <span>词云图</span>
        </div>
        <div class="menu-item" @click="switchChart('genderPie')" :class="{ active: activeChart === 'genderPie' }">
          <span>性别分布</span>
        </div>
        <div class="menu-item" @click="switchChart('dateLine')" :class="{ active: activeChart === 'dateLine' }">
          <span>评论趋势</span>
        </div>
        <div class="menu-item" @click="switchChart('sentimentBar')" :class="{ active: activeChart === 'sentimentBar' }">
          <span>情感分析</span>
        </div>
        <div class="menu-item" @click="switchChart('regionMap')" :class="{ active: activeChart === 'regionMap' }">
          <span>地区分布</span>
        </div>
        <div class="menu-item" @click="switchChart('kmeansCluster')" :class="{ active: activeChart === 'kmeansCluster' }">
          <span>KMeans 聚类</span>
        </div>
        <div class="menu-item" @click="switchChart('topLikedComments')" :class="{ active: activeChart === 'topLikedComments' }">
          <span>点赞排行</span>
        </div>
      </div>

      <div class="content-container">
        <div v-if="loading" class="loading">
          <p>加载中...</p>
        </div>
        <!-- 图表容器 -->
        <div v-else class="chart-container">
          <!-- 词云图 -->
          <div v-if="activeChart === 'wordCloud'" ref="wordCloudChart" style="width: 100%; aspect-ratio: 3 / 2;margin: 20px;"></div>

          <!-- 性别分布饼图 -->
          <div v-if="activeChart === 'genderPie'" ref="genderPieChart" style="width: 100%; height: 100%;"></div>

          <!-- 评论趋势折线图 -->
          <div v-if="activeChart === 'dateLine'" ref="dateLineChart" style="width: 100%; aspect-ratio: 3 / 2;"></div>

          <!-- 情感分析柱状图 -->
          <div v-if="activeChart === 'sentimentBar'" ref="sentimentBarChart" style="width: 100%; aspect-ratio: 3 / 2;"></div>

          <!-- 地区分布图 -->
          <div v-if="activeChart === 'regionMap'" ref="regionMapChart" style="width: 100%; aspect-ratio: 3 / 2;"></div>

          <!-- KMeans 聚类图 -->
          <div v-if="activeChart === 'kmeansCluster'" ref="kmeansClusterChart" style="width: 100%; aspect-ratio: 3 / 2; "></div>

          <!-- 点赞排行表格 -->
          <div v-if="activeChart === 'topLikedComments'" ref="topLikedCommentsChart" style="width: 100%; aspect-ratio: 3 / 2;"></div>

        </div>

        <!-- 评论列表 -->
        <div class="comment-section" @scroll="handleCommentScroll">

          

          <div class="comment-count">
            评论数量: {{ commentData.length }}
          </div>
          <div v-if="commentData.length > 0" class="comments">
            <div 
              v-for="(comment, index) in commentData" 
              :key="index" 
              class="comment-item"
            >
              <div class="user-info">
                <img 
                  :src="proxyImage(comment.member.avatar)" 
                  class="avatar"
                  alt="用户头像"
                >
                <span class="username">{{ comment.member.uname }}</span>
              </div>
              <p class="content">{{ comment.content.message }}</p>
              <div class="meta">
                <span class="likes">👍 {{ comment.like }}</span>
                <span class="time">{{ formatTime(comment.ctime) }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-comments">
            <p>暂无评论</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from 'echarts';
import 'echarts-wordcloud'; // 引入 echarts-wordcloud 插件
import china from '@/assets/china.json'; // 手动引入中国地图的 GeoJSON 数据

export default {
  name: 'Analyse',
  data() {
    return {
      video: {},
      commentData: [],
      activeChart: 'wordCloud', // 默认显示词云图
      commentPage: 1,
      commentHasMore: true,
      commentLoading: false,
      wordCloudChart: null,
      genderPieChart: null,
      dateLineChart: null,
      sentimentBarChart: null,
      regionMapChart: null,
      kmeansClusterChart: null,
      loading: true // 添加 loading 状态
    };
  },
  mounted() {
    echarts.registerMap('china', china); // 注册中国地图的 GeoJSON 数据
    this.fetchAllVideoComments(this.$route.params.aid);
  },
  methods: {
    // 获取所有评论数据
    async fetchAllVideoComments(videoId) {
      try {
        if (!document.cookie.includes('SESSDATA')) {
          alert("请先登录！");
          return this.$router.push('/login');
        }
        const startTime = Date.now(); // 记录请求开始时间
        const res = await axios.get("http://localhost:3000/api/all_video_comments", {
          params: { oid: videoId },
          withCredentials: true,
          headers: {
            'Cookie': document.cookie
          }
        });
        const endTime = Date.now(); // 记录请求结束时间
        const duration = endTime - startTime; // 计算耗时
        console.log(`请求所有评论耗时: ${duration}ms`); // 输出耗时
        if (res.data.code === 0) {
          this.commentData = res.data.data?.replies || [];
          this.generateChart();
        } else {
          alert(res.data.message || "评论获取失败");
        }
      } catch (error) {
        if (error.response?.status === 401) {
          alert("登录过期，请重新登录");
          this.$router.push('/login');
        } else {
          alert("获取评论数据时发生错误"+error.message);
        }
      } finally {
        this.loading = false; // 关闭 loading
      }
    },
    // 切换图表
    switchChart(chartType) {
      this.activeChart = chartType;
      this.$nextTick(() => {
        this.generateChart();
      });
    },
    // 生成图表
    async generateChart() {
      try {
        let apiUrl = '';
        switch (this.activeChart) {
          case 'wordCloud':
            apiUrl = '/api/generate_wordcloud';
            break;
          case 'genderPie':
            apiUrl = '/api/generate_gender_pie';
            break;
          case 'dateLine':
            apiUrl = '/api/generate_date_line';
            break;
          case 'sentimentBar':
            apiUrl = '/api/generate_sentiment_bar';
            break;
          case 'regionMap':
            apiUrl = '/api/generate_region_map';
            break;
          case 'kmeansCluster':
            apiUrl = '/api/generate_kmeans_cluster';
            break;
          case 'topLikedComments':
            apiUrl = '/api/top_liked_comments';
            break;
        
        }

        const res = await axios.get(`http://localhost:3000${apiUrl}`, {
          params: {
            oid: this.$route.params.aid
          }
        });

        if (res.data.code === 0) {
          this.$nextTick(() => {
            switch (this.activeChart) {
              case 'topLikedComments':
                this.renderTopLikedComments(res.data.data);
                break;
              case 'wordCloud':
                this.renderWordCloud(res.data.data);
                break;
              case 'genderPie':
                this.renderGenderPie(res.data.data);
                break;
              case 'dateLine':
                this.renderDateLine(res.data.data);
                break;
              case 'sentimentBar':
                this.renderSentimentBar(res.data.data);
                break;
              case 'regionMap':
                this.renderRegionMap(res.data.data);
                break;
              case 'kmeansCluster':
                this.renderKMeansCluster(res.data.data);
                break;
            }
          });
        } else {
          alert(`生成${this.activeChart}失败: ` + res.data.error);
        }
      } catch (error) {
        alert(`生成${this.activeChart}时发生错误: ` + error.message);
      }
    },

    // 渲染图表
    renderChart(data) {
      switch (this.activeChart) {
        case 'wordCloud':
          this.renderWordCloud(data);
          break;
        case 'genderPie':
          this.renderGenderPie(data);
          break;
        case 'dateLine':
          this.renderDateLine(data);
          break;
        case 'sentimentBar':
          this.renderSentimentBar(data);
          break;
        case 'regionMap':
          this.renderRegionMap(data);
          break;
        case 'kmeansCluster':
          this.renderKMeansCluster(data);
          break;
      }
    },

    // 渲染词云图
    renderWordCloud(data) {
      if (this.wordCloudChart) {
        this.wordCloudChart.dispose();
      }
      const wordCloudContainer = this.$refs.wordCloudChart;
      wordCloudContainer.innerHTML = `<img src="${data.plt_url}" alt="词云图" style="width: 100%; height: 100%;" />`;
    },

    // 渲染性别分布饼图
    renderGenderPie(data) {
      if (this.genderPieChart) {
        this.genderPieChart.dispose();
      }
      this.genderPieChart = echarts.init(this.$refs.genderPieChart);
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [{
          name: '性别分布',
          type: 'pie',
          radius: '50%',
          data: data.genders,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
      this.genderPieChart.setOption(option);
    },

    // 渲染评论趋势折线图
    renderDateLine(data) {
      if (this.dateLineChart) {
        this.dateLineChart.dispose();
      }
      this.dateLineChart = echarts.init(this.$refs.dateLineChart);
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: data.dates
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: data.counts,
          type: 'line',
          smooth: true
        }]
      };
      this.dateLineChart.setOption(option);
    },

    // 渲染情感分析柱状图
    renderSentimentBar(data) {
      if (this.sentimentBarChart) {
        this.sentimentBarChart.dispose();
      }
      this.sentimentBarChart = echarts.init(this.$refs.sentimentBarChart);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: data.sentiments
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: data.counts,
          type: 'bar',
          barWidth: '60%'
        }]
      };
      this.sentimentBarChart.setOption(option);
    },

    // 渲染地区分布图
    renderRegionMap(data) {
      if (this.regionMapChart) {
        this.regionMapChart.dispose();
      }
      this.regionMapChart = echarts.init(this.$refs.regionMapChart);
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}'
        },
        visualMap: {
          min: 0,
          max: Math.max(...data.values),
          left: 'left',
          top: 'bottom',
          text: ['高', '低'],
          calculable: true
        },
        series: [{
          name: '地区分布',
          type: 'map',
          mapType: 'china',
          roam: false,
          label: {
            show: false
          },
          data: data.regions
        }]
      };
      this.regionMapChart.setOption(option);
    },

    // 渲染 KMeans 聚类图
    renderKMeansCluster(data) {
      if (this.kmeansClusterChart) {
        this.kmeansClusterChart.dispose();
      }
      this.kmeansClusterChart = echarts.init(this.$refs.kmeansClusterChart);
      const option = {
        tooltip: {
          formatter: function (params) {
            return params.data.name;
          }
        },
        xAxis: {},
        yAxis: {},
        series: [{
          symbolSize: 10,
          data: data.points,
          type: 'scatter',
          itemStyle: {
            color: function (params) {
              const colorList = ['#5470C6', '#91CC75', '#EE6666', '#73C0DE', '#3BA272'];
              return colorList[params.data.value[2]];
            }
          }
        }]
      };
      this.kmeansClusterChart.setOption(option);
    },

    // 渲染点赞排行表格
    renderTopLikedComments(data) {
      if (this.topLikedCommentsChart) {
        this.topLikedCommentsChart.dispose();
      }
      this.topLikedCommentsChart = echarts.init(this.$refs.topLikedCommentsChart);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: data.map(item => item['评论内容'].substring(0, 20) + '...')
        },
        series: [{
          data: data.map(item => item['点赞数']),
          type: 'bar',
          label: {
            show: true,
            position: 'right'
          }
        }]
      };
      this.topLikedCommentsChart.setOption(option);
    },



    // 代理图片地址
    proxyImage(url) {
      return `http://localhost:3000/api/proxy_image?url=${encodeURIComponent(url)}`;
    },

    // 格式化时间戳
    formatTime(timestamp) {
      return new Date(timestamp * 1000).toLocaleString();
    }
  }
};
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 18px;
  color: #666;
}

.video-detail {
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.video-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.video-player {
  flex: 1;
  max-height: 100%; /* 限制视频区域的最大高度 */
  overflow: hidden; /* 禁止视频区域滚动 */
}

.video-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.author-name {
  font-size: 18px;
  font-weight: 500;
  color: #fa7298;
}

.video-title {
  font-weight: 500;
  font-size: 20px;
  /* padding-top: 10px;*/
  padding-bottom: 8px; 
  color: #1a1a1a;
}

.description {
  font-size: 14px;
  color: black;
  line-height: 1.6;
  
}
.videoView{
  width: 100%;
  aspect-ratio: 668 / 376;
}

.sidebar {
  width: 240px; 
  position: fixed;
  height: calc(100vh - 20px);
  overflow-y: auto;
  border-right: 1px solid #ddd;
  background-color: #f8f9fa;
  padding: 10px;
  z-index: 1000; /* 确保侧边栏在最上层 */
}

.menu-item {
  padding: 12px 15px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  border-radius: 8px;
}

.menu-item:hover {
  background-color: #e9ecef;
}

.menu-item.active {
  background-color: #e9ecef;
  color: #fa7290;
  font-weight: bold;
}

.content-container {
  display: flex;
  flex: 1;
  margin-left: 240px;
}

.chart-container {
  flex: 3;
  /* display: flex;              */
  justify-content: center;    /* 水平居中 */
  /* align-items: center;        */
}


.comment-section {
  flex: 2;
  background-color: #fff;
  overflow-y: auto;
  padding: 10px;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.comment-section::-webkit-scrollbar {
  width: 8px;
}

.comment-section::-webkit-scrollbar-track {
  background: transparent;
}

.comment-section::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.comment-item {
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  background: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.username {
  font-weight: 500;
  color: #2d2d2d;
}

.content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 10px;
}

.meta {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.9em;
}

.likes::before {
  content: '👍 ';
}

.no-comments {
  text-align: center;
  color: #999;
  padding: 30px;
}

.comment-count {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}
</style>
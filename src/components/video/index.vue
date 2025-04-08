<template>
  <div class="video-detail">
    <div class="video-container">
      <!-- 视频播放器 -->
      <div class="video-player">
        <div class="video-header">
          <img :src="proxyImage(video.owner.face)" alt="作者头像" class="author-avatar" />
          <span class="author-name" >{{ video.owner.name }}</span>
          <button class="analyse" @click.prevent="router.push({ name: 'Analyse' })">评论分析</button>
        </div>
        <h1 class="video-title">{{ video.title }}</h1>
        <video class="videoView" :src="proxyVideoUrl" controls width="100%" :muted="false" autoplay></video>
      </div>

      <!-- 评论列表 -->
      <div class="comment-section" @scroll="handleCommentScroll">
        <p class="description">{{ video.desc }}</p>
        <h2>评论（{{ commentData.length }}条）</h2>
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
</template>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';
export default {
  name: 'VideoDetail',
  setup(){
    const router = useRouter();
    return {
      router // 返回 router 对象以便在模板中使用
    };
  },
  data() {
    return {
      video: {},
      commentData: [],
      commentPage: 1,
      commentHasMore: true,
      commentLoading: false
    };
  },
  computed: {
    proxyVideoUrl() {
      if (!this.video.playurl) return '';
      const playurl = this.video.playurl.startsWith('http') ? this.video.playurl : `https:${this.video.playurl}`;
      return `http://localhost:3000/api/proxy_video?url=${encodeURIComponent(playurl)}`;
    }
  },
  async created() {
    const videoId = this.$route.params.aid;
    await this.fetchVideoDetails(videoId);
    await this.fetchVideoComments(videoId);
  },
  methods: {
    // 获取视频详情
    async fetchVideoDetails(videoId) {
      try {
        const res = await axios.get("http://localhost:3000/api/video_details", {
          params: { aid: videoId },
          withCredentials: true
        });
        if (res.data.code === 0) this.video = res.data.data;
      } catch (error) {
        alert("视频详情获取失败");
      }
    },

    // 获取评论数据
    async fetchVideoComments(videoId) {
      try {
        if (!document.cookie.includes('SESSDATA')) {
          alert("请先登录！");
          return this.$router.push('/login');
        }

        const res = await axios.get("http://localhost:3000/api/video_comments", {
          params: { oid: videoId, sort: 1, pn: this.commentPage, ps: 20 },
          withCredentials: true,
          headers: {
            'Cookie': document.cookie
          }
        });

        if (res.data.code === 0) {
          this.commentData = [...this.commentData, ...(res.data.data?.replies || [])];
          this.commentHasMore = res.data.data?.replies.length > 0;
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
        this.commentLoading = false;
      }
    },

    // 处理评论区域滚动事件
    handleCommentScroll(event) {
      const { scrollTop, scrollHeight, clientHeight } = event.target;
      if (scrollHeight - scrollTop <= clientHeight + 50 && !this.commentLoading && this.commentHasMore) {
        this.commentLoading = true;
        this.commentPage += 1;
        this.fetchVideoComments(this.$route.params.aid);
      }
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
.video-detail {
  padding: 10px;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 100vh; /* 设置高度为视口高度 */
}

.video-container {
  display: flex;
  gap: 20px;
  flex: 1; /* 占据剩余空间 */
  overflow: hidden; /* 禁止外部滚动 */
}
.analyse{
  margin-right: 0;
  margin-left: auto;
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

.comment-section {
  flex: 1;
  max-width: 400px;
  overflow-y: auto;
  scrollbar-width: thin; /* 美化滚动条 */
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent; /* 滚动条颜色 */
}

.comment-section::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
}

.comment-section::-webkit-scrollbar-track {
  background: transparent; /* 滚动条背景透明 */
}

.comment-section::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2); /* 滚动条颜色 */
  border-radius: 4px; /* 滚动条圆角 */
}

/* 评论项样式 */
.comment-item {
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  background: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
</style>
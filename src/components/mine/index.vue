<!-- src/components/home/index.vue -->
<template>
   <div class="search-container">
    <div class="content" @scroll="handleScroll">
      <div class="video-grid">
        <div v-for="(video, index) in videoData" :key="index" class="video-item" @click="navigateToVideo(video.aid)">
          <img :src="`http://localhost:3000/api/proxy_image?url=${encodeURIComponent(video.pic)}`" :alt="video.title" class="video-thumbnail" @error="handleImageError" />
          <h2>{{ video.title }}</h2>
        </div>
      </div>
    </div>
   </div>
</template>
  
  <script>
  import axios from "axios";
  import { useRouter } from 'vue-router';
  import { useStore } from 'vuex';
  import { computed } from 'vue';
  
  export default {
    name: 'Mine',
    setup() {
      const router = useRouter();
      const store = useStore();
  
      // 从 Vuex store 获取用户信息
      const userInfo = computed(() => store.getters.userInfo);
  
      return {
        userInfo,
        videoData: [],
        commentData: [],
        router,
        loading: false,
        page: 1,
        hasMore: true
      };
    },
    async created() {
      await this.fetchUserVideos();
    },
    methods: {
      async fetchUserVideos() {
        try {
          const cacheKey = `videoData_${this.userInfo.mid}`;
          const cachedData = localStorage.getItem(cacheKey);
          if (cachedData) {
            this.videoData = JSON.parse(cachedData);
            console.log("使用缓存数据");
          }
  
          const response = await axios.get("http://localhost:3000/api/user_videos", {
            params: {
              mid: this.userInfo.mid, // 用户 ID
              pn: this.page, // 页码
              ps: 10, // 每页数量
            },
          });
  
          if (response.data.code === 0) {
            this.videoData = response.data.data.list?.vlist || []; // 更新视频数据
            console.log("获取到的视频数据:", this.videoData); // 添加调试信息
            localStorage.setItem(cacheKey, JSON.stringify(this.videoData)); // 保存缓存
            console.log("保存缓存数据");
          } else {
            console.error("获取视频数据失败:", response.data.message);
            alert(response.data.message); // 提示用户错误信息
          }
        } catch (error) {
          if (error.response && error.response.status === 429) {
            // 处理请求过于频繁的情况
            alert("请求过于频繁，请稍后再试");
          } else {
            console.error("获取视频数据失败:", error);
            alert("获取视频数据失败，请检查网络或稍后再试");
          }
  
          // 请求失败时使用缓存数据
          const cacheKey = `videoData_${this.userInfo.mid}`;
          const cachedData = localStorage.getItem(cacheKey);
          if (cachedData) {
            this.videoData = JSON.parse(cachedData);
            console.log("使用缓存数据（请求失败）");
          }
        }
      },
      // 获取评论数据
      async fetchVideoComments(videoId) {
        try {
          const response = await axios.get("http://localhost:3000/api/video_comments", {
            params: {
              oid: videoId, // 视频 ID
              pn: 1, // 页码
              ps: 10, // 每页数量
            },
          });
  
          if (response.data.code === 0) {
            this.commentData = response.data.data.replies; // 评论数据
            console.log("获取到的评论数据:", this.commentData);
          } else {
            console.error("获取评论数据失败:", response.data.message);
          }
        } catch (error) {
          console.error("获取评论数据失败:", error);
        }
      },
      handleScroll(event) {
      const { scrollTop, scrollHeight, clientHeight } = event.target;
      if (scrollHeight - scrollTop <= clientHeight + 50 && !this.loading && this.hasMore) {
        this.loading = true;
        this.page += 1;
        this.fetchUserVideos();
        
      }
    },
      handleImageError(event) {
        console.error("图片加载失败:", event.target.src);
        console.log("尝试加载默认图片");
        event.target.src = "https://via.placeholder.com/400"; // 使用默认图片
      },
      navigateToVideo(videoId) {
        this.router.push({ name: 'VideoDetail', params: { aid: videoId } });
      }
    }
  }
  </script>
  
  <style scoped>
  .search-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}


.content {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.content::-webkit-scrollbar {
  width: 8px;
}

.content::-webkit-scrollbar-track {
  background: transparent;
}

.content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}
.video-grid {
  display: flex;
  flex-wrap: wrap;
  /* gap: 20px; */
  
}

.video-item {
  flex: 0 0 calc(25%);
  width: 100%;
  aspect-ratio: 240 / 208;
  /* border: 1px solid #ddd; */
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
  cursor: pointer;
  padding: 10px;
  
}

.video-item .video-thumbnail {
  aspect-ratio: 240 / 135;
  width: 100%;
  object-fit: cover;
  margin-bottom: 10px;
  border-radius: 4px;
}

.video-item h2 {
  width: 100%;
  font-size: 16px;
  margin-bottom: 10px;
  color: black;
  white-space: normal;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  font-weight: 500; /* 加粗字体 */
}
  </style>
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import DouyinLogin from '../components//douyin/DouyinLogin.vue'; // 确认路径是否正确
import Analyse from '../components/analyse/index.vue'; //分析主页面
import About from '../components/about/index.vue';
import Home from '../components/home/index.vue'
const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'DouyinLogin',
    component: DouyinLogin,
  },
  {
    path: '/analyse',
    name: 'Analyse',
    component: Analyse,
  },
  {
    path:'/about',
    name:'About',
    component:About
  },

];

const router = createRouter({
  history: createWebHistory(import.meta.env.VUE_APP_BASE_URL||'/'),
  routes,
});

export default router;
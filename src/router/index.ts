// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import store from '../store'; // 导入 Vuex Store

import Analyse from '../components/analyse/index.vue'; // 分析主页面
import About from '../components/about/index.vue';
import Home from '../components/home/index.vue';
import BilibiliLogin from '../components/bilibili/index.vue'; // 修改为 Bilibili 登录组件
import Main from '../components/main/index.vue';
import VideoDetail from '../components/video/index.vue'; // 视频详情页面
import Mine from '../components/mine/index.vue';

import Search from '../components/search/index.vue';
const routes = [
  {
    path: '/login',
    name: 'BilibiliLogin',
    component: BilibiliLogin,
  },
  {
    path: '/',
    name: 'Main',
    component: Main,
    meta: { requiresAuth: true }, // 需要身份验证
    children: [
      {
        path: '', // 默认子路由
        name: 'Home',
        component: Home,
      },
      {
        path: 'about',
        name: 'About',
        component: About,
      },
      {
        path: 'analyse/:aid',
        name: 'Analyse',
        component: Analyse,
        meta: { requiresAuth: true }, // 需要身份验证
      },
      {
        path: 'video/:aid',
        name: 'VideoDetail',
        component: VideoDetail,
        meta: { requiresAuth: true }, // 需要身份验证
      },
      {
        path: 'search/:keyword',
        name: 'Search',
        component: Search,
        meta: { requiresAuth: true }, // 需要身份验证
      },
      {
        path: '/mine',
        name: 'Mine',
        component: Mine,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'BilibiliLogin' }); // 如果未登录，重定向到 Bilibili 登录页面
    } else {
      next(); // 如果已登录，继续导航
    }
  } else {
    next(); // 如果不需要身份验证，继续导航
  }
});

export default router;
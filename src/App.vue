<template>
  <div id="app">
    <router-view class="page"></router-view>
  </div>

</template>

<script setup lang="ts">
//导入bilibili登录
import BiliBiliView from './components/bilibili/index.vue';


import { onMounted } from 'vue';

const colors = [
  'linear-gradient(to right, #fbc2eb, #a6c1ee)',
  'linear-gradient(to right, #ff9a9e, #fad0c4)',
  'linear-gradient(to right, #a1c4fd, #c2e9fb)',
  'linear-gradient(to right, #ffdde1, #ee9ca7)'
];

let index = 0;

function changeBackground() {
  document.getElementById('app').style.backgroundImage = colors[index];
  index = (index + 1) % colors.length;
}

onMounted(() => {
  setInterval(changeBackground, 5000); // 每5秒切换背景
});
</script>


<style scoped>
#app {
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-image 2s ease-in-out;
}
.page {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

</style>

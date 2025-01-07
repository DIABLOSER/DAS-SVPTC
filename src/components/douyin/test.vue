<template>
  <div>
    <button @click="goToHome">Go to Home</button>

    
    <RouterLink to="/home">go to home</RouterLink>
  </div>
  <div>
    <router-view></router-view>
  </div>

</template>

<script setup>
import {RouterLink, useRouter }  from 'vue-router';

const router = useRouter();

const goToHome = () => {
  console.log('Navigating to Home'); // 调试信息
  try {
    router.push('/home')
  //this.$router.push('Home'); // 跳转到 /about 页面
  } catch (error) {
    console.error('Error navigating to Home:', error);
  }
};
</script>
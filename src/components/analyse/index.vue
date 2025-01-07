<template>
    <div class="sidebar">
      <ul class="nav">
        <li v-for="(item, index) in navItems" :key="index" class="nav-item">
          <a href="#" class="nav-link" @click.prevent="handleClick(item)">
            {{ item.title }}
          </a>
          <ul v-if="item.children && item.children.length > 0" class="sub-nav" v-show="item.isExpanded">
            <li v-for="(child, childIndex) in item.children" :key="childIndex" class="sub-nav-item">
              <a href="#" class="sub-nav-link">{{ child }}</a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Sidebar',
    data() {
      return {
        navItems: [
          {
            title: '首页',
            children: [],
            isExpanded: false,
          },
          {
            title: '产品',
            children: ['产品1', '产品2', '产品3'],
            isExpanded: false,
          },
          {
            title: '服务',
            children: ['服务1', '服务2'],
            isExpanded: false,
          },
          {
            title: '关于我们',
            children: [],
            isExpanded: false,
          },
        ],
      };
    },
    methods: {
      handleClick(item) {
        if (item.children && item.children.length > 0) {
          item.isExpanded = !item.isExpanded;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 200px;
    background-color: #333;
    color: #fff;
    height: auto;
    display: flex;
    padding-top: 20px;
  }
  
  .nav {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .nav-item {
    position: relative;
  }
  
  .nav-link {
    display: block;
    padding: 10px 15px;
    text-decoration: none;
    color: #fff;
    transition: background-color 0.3s;
  }
  
  .nav-link:hover {
    background-color: #555;
  }
  
  .sub-nav {
    list-style-type: none;
    padding-left: 20px;
    margin: 0;
    background-color: #444;
  }
  
  .sub-nav-item {
    position: relative;
  }
  
  .sub-nav-link {
    display: block;
    padding: 10px 15px;
    text-decoration: none;
    color: #fff;
    transition: background-color 0.3s;
  }
  
  .sub-nav-link:hover {
    background-color: #666;
  }
  </style>
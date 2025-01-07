<template>
    <li class="nav-item" :class="{ expanded: isExpanded }" @click="toggleExpand">
      {{ title }}
      <ul class="nav-submenu" v-if="children.length > 0">
        <li v-for="(child, index) in children" :key="index">
          {{ child }}
        </li>
      </ul>
    </li>
  </template>
  
  <script>
  export default {
    name: 'NavItem',
    props: {
      title: String,
      children: Array,
      isExpanded: Boolean,
    },
    methods: {
      toggleExpand() {
        this.$emit('toggle-expand');
      },
    },
  };
  </script>
  
  <style scoped>
  .nav-item {
    cursor: pointer;
    padding: 10px;
    border-bottom: 1px solid #ddd;
    background-color: #fff;
  }
  
  .nav-item:hover {
    background-color: #e0e0e0;
  }
  
  .nav-item.expanded {
    background-color: #e0e0e0;
  }
  
  .nav-submenu {
    list-style-type: none;
    padding-left: 20px;
    margin: 0;
    display: none;
  }
  
  .nav-item.expanded .nav-submenu {
    display: block;
  }
  
  .nav-submenu li {
    padding: 5px 0;
    cursor: pointer;
  }
  
  .nav-submenu li:hover {
    color: #007bff;
  }
  </style>
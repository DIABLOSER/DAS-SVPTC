<template>
  <div class="full-screen-background">
    <p>短视频平台文本评论动态分析系统</p>
    <div class="suipin">
      <button>
    Sign up
    <div class="arrow-wrapper">
        <div class="arrow"></div>

    </div>
</button>
      <a>点击注册</a>
      <a href="src/assets/readme.html">Readme</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.full-screen-background {
  position: fixed;
  flex-direction: column;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #003973;
  background: -webkit-linear-gradient(90deg, #556270 10%, #FF6B6B 90%); /* Chrome 10+, Saf5.1+ */
  background:    -moz-linear-gradient(90deg, #556270 10%, #FF6B6B 90%); /* FF3.6+ */
  background:     -ms-linear-gradient(90deg, #556270 10%, #FF6B6B 90%); /* IE10 */
  background:      -o-linear-gradient(90deg, #556270 10%, #FF6B6B 90%); /* Opera 11.10+ */
  background:         linear-gradient(90deg, #556270 10%, #FF6B6B 90%); /* W3C */
  /* background-image: url('src/assets/img/background.jpg'); */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  /* 水平居中 */
  justify-content: center;
  /* 垂直居中 */
  align-items: center;
  display: flex;
  gap: 10px;
  
}
p {
  font-size: 50px;
  color: white;
  font-weight: bold;
  text-align: center;
  letter-spacing: 4px;
}
.suipin {
  display: flex;
  flex-direction: row;
  width: 100%;
  /* 水平居中 */
  justify-content: center;
  height: 100px;
  gap: 10px;
}
a {
  height: 40px;
  width: 80px;
  text-align: center;
  align-content: center;
  border-color: black;
  border-width: 2px;
  border-style: solid;
  background-color: white;
  border-radius: 40px;
  
}
/* From Uiverse.io by satyamchaudharydev */ 
button {
  --primary-color: #645bff;
  --secondary-color: #fff;
  --hover-color: #111;
  --arrow-width: 10px;
  --arrow-stroke: 2px;
  box-sizing: border-box;
  border: 0;
  border-radius: 20px;
  color: var(--secondary-color);
  padding: 1em 1.8em;
  background: var(--primary-color);
  display: flex;
  transition: 0.2s background;
  align-items: center;
  gap: 0.6em;
  font-weight: bold;
}

button .arrow-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

button .arrow {
  margin-top: 1px;
  width: var(--arrow-width);
  background: var(--primary-color);
  height: var(--arrow-stroke);
  position: relative;
  transition: 0.2s;
}

button .arrow::before {
  content: "";
  box-sizing: border-box;
  position: absolute;
  border: solid var(--secondary-color);
  border-width: 0 var(--arrow-stroke) var(--arrow-stroke) 0;
  display: inline-block;
  top: -3px;
  right: 3px;
  transition: 0.2s;
  padding: 3px;
  transform: rotate(-45deg);
}

button:hover {
  background-color: var(--hover-color);
}

button:hover .arrow {
  background: var(--secondary-color);
}

button:hover .arrow:before {
  right: 0;
}
</style>
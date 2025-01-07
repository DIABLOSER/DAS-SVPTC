<!-- 登录页面 -->
<template>
<div class="gradient-bg">
    <div class="login-box">
        <div class="login-header">请你登录</div>
        <div class="form-content">
            <input type="text" name="username" placeholder="账号" class="input-field">
            <input type="password" name="password" placeholder="密码" class="input-field">
            <div class="login-button">登录</div>
        </div>
        <div class="message"> 如果没有账户? <a href="#">请先注册</a> </div>
    </div>
</div>
</template>
<script>
export default {
  name: 'Login',
};
</script>
<style scoped>


   

        .gradient-bg {
            height: 100%; /* 确保容器有高度 */
            width: 100%;
            /* 水平剧中 */
            justify-content: center;
            /* 垂直居中 */
            align-items: center;
        }

        .login-box {
            background-color: #fff;
            width: auto;
            height: 60%;
            border-radius: 15px;
            padding: 0 50px;
        }

        .login-header {
            font-size: 38px;
            font-weight: bold;
            text-align: center;
            line-height: 200px;
        }

        .input-field {
            width: 100%;
            margin-bottom: 20px;
            border: 0;
            padding: 10px;
            border-bottom: 1px solid rgb(128, 125, 125);
            font-size: 15px;
            outline: none;
        }

        .input-field::placeholder {
            text-transform: uppercase;
        }

        .login-button {
            text-align: center;
            padding: 10px;
            width: 100%;
            margin-top: 40px;
            background-image: linear-gradient(to right, #a6c1ee, #fbc2eb);
            color: #fff;
            border-radius: 8px;
        }

        .message {
            text-align: center;
            line-height: 88px;
        }

        a {
            text-decoration-line: none;
            color: #abc1ee;
        }
</style>
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // 移除 https 配置
  // server: {
  //   https: {
  //     key: fs.readFileSync('ssl/server.key'),
  //     cert: fs.readFileSync('ssl/server.crt')
  //   },
  //   proxy: {
  //     '/api': {
  //       target: 'https://open.douyin.com',
  //       changeOrigin: true,
  //       rewrite: (path) => path.replace(/^\/api/, ''),
  //     },
  //   },
  // },
});

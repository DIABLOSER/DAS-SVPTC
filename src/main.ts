// main.ts
// main.ts
import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import globalVariables from './plugins/globalVariables';
import router from './router/index';

const app = createApp(App);
app.use(globalVariables);
app.use(router);
app.mount('#app');
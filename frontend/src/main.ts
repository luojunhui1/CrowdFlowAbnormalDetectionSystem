import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

const app = createApp(App);

import ElementPlus, { ElMessage } from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';

app.config.globalProperties.$message = ElMessage;
app.config.globalProperties.$http = axios;

app.use(store)
  .use(router)
  .use(ElementPlus)
app.mount('#app');

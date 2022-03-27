import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import * as echarts from 'echarts'

const app = createApp(App);

import ElementPlus, { ElMessage } from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';

app.use(store)
  .use(router)
  .use(ElementPlus);
  
app.config.globalProperties.$message = ElMessage;
app.config.globalProperties.$http = axios;
app.config.globalProperties.$echarts = echarts

app.mount('#app');

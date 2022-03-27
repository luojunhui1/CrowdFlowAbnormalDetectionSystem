import axios from 'axios';
import store from '../store/index'; // 追加token

const service = axios.create({
  timeout: 50000 // 请求超时时间
});

service.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

service.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'

let requestCount = 0;
service.interceptors.request.use(
  config => {
      requestCount++;
      store.commit('handleLoading', true); // 接口请求loading
      return config
  },
  error => {
      console.log(error) // for debug
      Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    requestCount--;
      if(requestCount<=0){ // 如果接口请求累加值小于0 那么关闭loading
          store.commit('handleLoading', false);
      }
      const res = response.data;
      return res;
  },
  error => {
    requestCount--;
      if(requestCount<=0){
          store.commit('handleLoading', false);
      }
      Promise.reject(error);
  }
)
export default service;
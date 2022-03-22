import axios from 'axios';
import { inject } from './index';
import Config from '../config';

const service = axios.create({
  baseURL: Config.unionService, // api的base_url
  timeout: 50000 // 请求超时时间
});

service.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

service.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'

inject(service);

export default service;
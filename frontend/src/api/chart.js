//本来想用mock模拟数据的，但是地图数据不好模拟，特别是这里要一级级下钻
//不可能把所有的市县都写上去，那样功能量太大了，所以这里用promise  假装模拟调接口

import { getMapInfo } from "@/utils";
import axios from 'axios'
/**
 *  获取最近5年的城市销售额度    模拟数据，这里year属性就不用了
 *  @param {string}  abcode  城市code
 *  @param {number}  year       年份
 *  @returns {Array}
 */
export function selectCityData({ abcode, year } = params) {
  return new Promise((resolve, reject) => {
    getMapInfo(abcode)
      .then((data) => {
        const mapData = data.map((item) => {
          return {
            name: item.name,
            value: (Math.random() * 3000).toFixed(2),
            adcode: item.adcode,
          };
        });
        resolve({
          code: 200,
          data: mapData,
        });
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function getRankData({meunIndex} = param)
{
  return new Promise((resolve, reject) => {
    const backend_url='http://127.0.0.1:5003';
    axios
    .post(backend_url + '/meun', {meunIndex: meunIndex.value})
    .then(response=>{
      resolve(response.data)
    })
    .catch((error) => {
      reject(error);
    });
  })
}

export function getGridMapData({meunIndex} = param)
{
  return new Promise((resolve, reject) => {
    const backend_url='http://127.0.0.1:5003';
    axios
    .post(backend_url + '/map', {meunIndex: meunIndex.value})
    .then(response=>{
      resolve(response.data)
    })
    .catch((error) => {
      reject(error);
    });
  })
}

export function getRight1Data({areaIndex, meunIndex} = param)
{
  return new Promise((resolve, reject) => {
    const backend_url='http://127.0.0.1:5003';
    axios
    .post(backend_url + '/right1', {areaIndex:areaIndex.value, meunIndex: meunIndex.value})
    .then(response=>{
      resolve(response.data)
    })
    .catch((error) => {
      reject(error);
    });
  })
}

export function getRight2Data({areaIndex, meunIndex} = param)
{
  return new Promise((resolve, reject) => {
    const backend_url='http://127.0.0.1:5003';
    axios
    .post(backend_url + '/right2', {areaIndex:areaIndex.value, meunIndex: meunIndex.value})
    .then(response=>{
      resolve(response.data)
    })
    .catch((error) => {
      reject(error);
    });
  })
}

export function getRight3Data({areaIndex, meunIndex} = param)
{
  return new Promise((resolve, reject) => {
    const backend_url='http://127.0.0.1:5003';
    axios
    .post(backend_url + '/right3', {areaIndex:areaIndex.value, meunIndex: meunIndex.value})
    .then(response=>{
      resolve(response.data)
    })
    .catch((error) => {
      reject(error);
    });
  })
}



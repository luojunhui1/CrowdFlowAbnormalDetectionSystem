<template>
  <div class="chart-wrapper" ref="rankChart"></div>
</template>

<script>
import echarts from "echarts";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { debounce } from "@/utils/index.js";
import useResize from "@/componentApi/useResize.js";
import {getRankData} from "@/api/chart.js";

export default {
  name: "rankChart",
  setup() {
    let {meunIndex} = useResize();

    const rankChart = ref(null);
    let myChart = ref(null);

    const resizeHandler = debounce(() => {
      if (myChart) {
        myChart.resize();
      }
    }, 200);

    onMounted(() => {
      getChartData();
      window.addEventListener("resize", resizeHandler);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("resize", resizeHandler);
    });

    //模拟接口，获取echarts数据
    const getChartData = async () => {
      let data = await getRankData({meunIndex});
      
      let cur = [];
      for(var i in data){
        cur.push({'id':i, 'value':data[i]})
      }

      cur.sort(function(a, b){
        return b.value - a.value
      });

      let xData = [], yData = [];

      for(var i in cur){
        xData.push("(" + Math.floor(cur[i].id/32) + "," + cur[i].id%32 + ")");
        yData.push(cur[i].value);
      }

      initEcharts(meunIndex, xData, yData);
    };
    const xLables = ['流量值', '预测值', '异常值']
    //渲染echarts图 
    const initEcharts = (meunIndex, xData, yData) => {
      myChart = echarts.init(rankChart.value);
      myChart.setOption(
        {
          grid: {
            left: "18%",
            right: "8%",
            bottom: "18%",
            top: "0%",
          },
          title: {
            show: xData.length === 0,
            top: "center",
            left: "center",
            text: "暂无数据",
            textStyle: {
              color: "rgb(179, 239, 255)",
              fontSize: 12,
            },
          },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow",
            },
            formatter: (params) => {
              return "区域编号：" + params[0].name + "<br>实时流量：" + params[0].value;
            },
          },
          xAxis: {
            name: xLables[meunIndex.value],
            nameLocation: 'middle',
            nameTextStyle:{
              color: '#ffffff',
              verticalAlign:'top',
              lineHeight:40,
            },
            type: "value",
            //网格线
              splitLine: {
                lineStyle: {
                  color: "#11366e",
                },
              },
              //轴线上的字
              axisLabel: {
                textStyle: {
                  fontSize: 12,
                  color: "#cecece",
                },
              },
              axisLine: {
                lineStyle: {
                  color: "#397cbc",
                },
              },
              axisTick: {
                show: true
              },
          },
          yAxis: {
              type: "category",
              name: '坐标',
              nameLocation: 'middle',
              nameTextStyle:{
                color: '#ffffff',
                verticalAlign:'bottom',
                lineHeight:65,
              },
              inverse: true,
              data:xData,
              axisLine: {
              lineStyle: {
                color: "#397cbc",
              },
            },
            //轴线上的字
            axisLabel: {
              show: true,
              textStyle: {
                color: "#cecece",
                fontSize: 12,
              },
              rotate: 35,
            }
            },
          series: [
            {
              name: "排名图",
              type: "bar",
              data: yData,
              barWidth: "60%",
              color: '#0421A2',
              showBackground: true,
            },

          ],
        },
        true
      );
    };

    watch(
      meunIndex,
      (nl, ol) => {
        getChartData();
      },
      { lazy: false }
    );

    return {
      rankChart,
    };
  },
};
</script>

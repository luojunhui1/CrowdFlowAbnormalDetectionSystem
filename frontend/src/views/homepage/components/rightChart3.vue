<template>
  <div class="chart-wrapper" ref="rightChart3"></div>
</template>

<script>
import echarts from "echarts";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { debounce} from "@/utils/index.js";
import useResize from "@/componentApi/useResize.js";
import {getRight3Data} from "@/api/chart.js";
import {getTime} from "@/utils/date.js";

export default {
  name: "rightChart3",
  setup() {
    let {meunIndex, areaIndex} = useResize();

    const rightChart3 = ref(null);
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
        let data = await getRight3Data({areaIndex, meunIndex});

        if(meunIndex.value == 0)
        {
            initEchartsFlow(data['xData'], data['inflow'], data['outflow']);
        }
        else if(meunIndex.value == 1)
        {
            initEchartsPred(data['xData'], data['inflow'], data['outflow']);
        }
        else
        {
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

            initEchartsAds(xData, yData);
        }
    };

    //渲染echarts Flow图
    const initEchartsFlow = (xData, inflow, outflow) => {
        myChart = echarts.init(rightChart3.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "20%",
                top: "15%",
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "shadow",
                },
                formatter: (params) => {
                    return  "流入值：" + params[0].value + "<br> 流出值:" +  params[1].value;
                },
            },
            legend: {
                show: true,
                right: "15",
                top: "0",
                itemWidth: 15,
                itemHeight: 11,
                textStyle: {
                    color: "#ffffff",
                },
            },
            xAxis: {
                type: 'category',
                name: xLables[meunIndex.value],
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
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
                data: xData
            },
            yAxis: {
                type: 'value',
                name: yLables[meunIndex.value],
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'bottom',
                    lineHeight:5,
                },
                axisLine: {
                    lineStyle: {
                        color: "#397cbc",
                    },
                },
                splitLine: {
                    lineStyle: {
                    color: "#11366e",
                    },
                },
                //轴线上的字
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: "#cecece",
                        fontSize: 12,
                    },
                    rotate: 0,
                }
                },
            series: [
                {
                    data: inflow,
                    name: "人群入流",
                    type: 'bar',
                    barWidth: '28%',
                    itemStyle: {
                        color: "#05D9E4",
                        opacity:0.8
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
                {
                    data: outflow,
                    name: "人群出流",
                    type: 'bar',
                    barWidth: '28%',
                    itemStyle: {
                        color: "#C46868",
                        opacity:0.8
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    labelLayout:{
                        aligin: 'right'
                    }
                },
            ]
        },
        true
        );
    };


    const initEchartsPred = (xData, pred_inflow, pred_outflow) => {
        myChart = echarts.init(rightChart3.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "20%",
                top: "15%",
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "shadow",
                },
                formatter: (params) => {
                    return  "预测流入值：" + params[0].value + "<br> 预测流出值:" +  params[1].value;
                },
            },
            legend: {
                show: true,
                right: "15",
                top: "0",
                itemWidth: 15,
                itemHeight: 11,
                textStyle: {
                    color: "#ffffff",
                },
            },
            xAxis: {
                type: 'category',
                name: xLables[meunIndex.value],
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
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
                data: xData
            },
            yAxis: {
                type: 'value',
                name: yLables[meunIndex.value],
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'bottom',
                    lineHeight:5,
                },
                axisLine: {
                    lineStyle: {
                        color: "#397cbc",
                    },
                },
                splitLine: {
                    lineStyle: {
                    color: "#11366e",
                    },
                },
                //轴线上的字
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: "#cecece",
                        fontSize: 12,
                    },
                    rotate: 0,
                }
                },
            series: [
                {
                    data: pred_inflow,
                    name: "预测人群入流",
                    type: 'bar',
                    barWidth: '28%',
                    itemStyle: {
                        color: "#05D9E4",
                        opacity:0.8
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
                {
                    data: pred_outflow,
                    name: "预测人群出流",
                    type: 'bar',
                    barWidth: '28%',
                    itemStyle: {
                        color: "#C46868",
                        opacity:0.8
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    labelLayout:{
                        aligin: 'right'
                    }
                },
            ]
        },
        true
        );
    };

    const xLables = ['区域', '区域', '异常值'];
    const yLables = ['流量', '流量', '坐标'];

    const initEchartsAds = (xData, ads) => {
        myChart = echarts.init(rightChart3.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "20%",
                top: "15%",
            },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow",
            },
            formatter: (params) => {
              return "区域编号：" + params[0].name + "<br>空间异常：" + params[0].value;
            },
          },
          xAxis: {
            type: "value",
            name: xLables[meunIndex.value],
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
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
              name: yLables[meunIndex.value],
                nameLocation: 'start',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'bottom',
                    lineHeight:5,
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
              }
            }
            },
          series: [
            {
                name: "空间异常排名",
                type: "bar",
                data: ads,
                barWidth: "70%",
                itemStyle: {
                    color: "#05D9E4",
                    opacity:0.6
                },
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
    
    watch(
      areaIndex,
      (nl, ol) => {
        getChartData();
      },
      { lazy: false }
    );

    return {
      rightChart3,
    };
  },
};
</script>

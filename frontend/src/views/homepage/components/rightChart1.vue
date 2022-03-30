<template>
  <div class="chart-wrapper" ref="rightChart1"></div>
</template>

<script>
import echarts from "echarts";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { debounce} from "@/utils/index.js";
import useResize from "@/componentApi/useResize.js";
import {getRight1Data} from "@/api/chart.js";
import {getTime} from "@/utils/date.js";

export default {
  name: "rightChart1",
  setup() {
    let {meunIndex, areaIndex} = useResize();

    const rightChart1 = ref(null);
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
        let data = await getRight1Data({areaIndex, meunIndex});

        if(meunIndex.value == 0)
        {
            initEchartsFlow(meunIndex, data['xData'], data['inflow'], data['outflow']);
        }
        else if(meunIndex.value == 1)
        {
            initEchartsPred(meunIndex, data['xData'], data['pred'], data['real']);
        }
        else
        {
            initEchartsAds(meunIndex, data['xData'], data['ads']);
        }
    };
    const yLables = ['流量值', '流量值', '异常值'];
    //渲染echarts Flow图
    const initEchartsFlow = (meunIndex, xData, inflow, outflow) => {
        myChart = echarts.init(rightChart1.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "10%",
                top: "10%",
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "line",
                },
                formatter: (params) => {
                    return "时间：" + params[0].name + "<br>入流值：" + params[0].value + "<br>出流值：" + params[1].value;
                },
            },
            legend: {
                show: true,
                right: "20",
                top: "0",
                itemWidth: 15,
                itemHeight: 11,
                textStyle: {
                    color: "#ffffff",
                },
            },
            xAxis: {
                type: 'category',
                name: '时间',
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
                boundaryGap: false,
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
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                        normal: {
                            color: "#05D9E4",
                            shadowColor: "rgba(53,142,215, 0.9)", //阴影颜色
                            shadowBlur: 20,
                            opacity:0.2
                        },
                    },
                    showSymbol: false,
                    itemStyle: {
                        color: "#05D9E4",
                    },
                    lineStyle: {
                        normal: {
                        width: 1,
                        color: "#05D9E4", // 线条颜色
                        },
                        borderColor: "#f0f",
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
                {
                    data: outflow,
                    name: "人群出流",
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                            normal: {
                            color: "#C46868",
                            shadowColor: "rgba(196,104,104, 0.9)", //阴影颜色
                            shadowBlur: 20,
                            opacity: 0.2
                        },
                    },
                    showSymbol: false,
                    itemStyle: {
                        color: "#05D9E4",
                    },
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: "#C46868", // 线条颜色
                        },
                        borderColor: "#f0f",
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
            ]
        },
        true
        );

    };

    const initEchartsPred = (meunIndex, xData, pred, real) => {
        myChart = echarts.init(rightChart1.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "10%",
                top: "15%",
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "line",
                },
                formatter: (params) => {
                    console.log(params)
                    return "时间：" + params[0].name + "<br>预测值：" + params[0].value + "<br>真实值：" + params[1].value;
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
                name: '时间',
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
                boundaryGap: false,
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
                    data: pred,
                    name: "预测值",
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                        normal: {
                        color: "#05D9E4",
                        shadowColor: "rgba(53,142,215, 0.9)", //阴影颜色
                        shadowBlur: 20,
                        opacity:0.2
                        },
                    },
                    showSymbol: false,
                    itemStyle: {
                        color: "#05D9E4",
                    },
                    lineStyle: {
                        normal: {
                        width: 1,
                        color: "#05D9E4", // 线条颜色
                        },
                        borderColor: "#f0f",
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
                {
                    data: real,
                    name: "真实值",
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                            normal: {
                            color: "#3fbbee",
                            shadowColor: "rgba(196,104,104, 0.9)", //阴影颜色
                            shadowBlur: 20,
                            opacity: 0.2
                        },
                    },
                    showSymbol: false,
                    itemStyle: {
                        color: "#05D9E4",
                    },
                    lineStyle: {
                        normal: {
                            width: 1,
                            color: "#3fbbee", // 线条颜色
                        },
                        borderColor: "#f0f",
                    },
                    emphasis: {
                        focus: 'series'
                    },
                },
            ]
        },
        true
        );
    };

    const initEchartsAds = (meunIndex, xData, ads) => {
        myChart = echarts.init(rightChart1.value);
        myChart.setOption({
            grid: {
                left: "13%",
                right: "13%",
                bottom: "10%",
                top: "15%",
            },
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    type: "line",
                },
                formatter: (params) => {
                    console.log(params)
                    return "时间：" + params[0].name + "<br>异常值：" + params[0].value.toFixed(2);
                },
            },
            xAxis: {
                type: 'category',
                name: '时间',
                nameLocation: 'end',
                nameTextStyle:{
                    color: '#ffffff',
                    verticalAlign:'middle',
                    lineHeight:50,
                },
                nameGap: 10,
                boundaryGap: false,
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
                    data: ads,
                    name: "异常值",
                    type: 'line',
                    smooth: true,
                    areaStyle: {
                        normal: {
                        color: "#C46868",
                        shadowColor: "rgba(53,142,215, 0.9)", //阴影颜色
                        shadowBlur: 20,
                        opacity:0.2
                        },
                    },
                    showSymbol: false,
                    itemStyle: {
                        color: "#C46868",
                    },
                    lineStyle: {
                        normal: {
                        width: 1,
                        color: "#C46868", // 线条颜色
                        },
                        borderColor: "#f0f",
                    },
                    emphasis: {
                        focus: 'series'
                    },
                }
            ]
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
      rightChart1,
    };
  },
};
</script>

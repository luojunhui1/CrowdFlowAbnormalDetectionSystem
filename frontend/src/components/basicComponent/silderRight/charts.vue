<template>
    <div class="charts">
        <div class="chart" id="chart1"></div>
        <div class="chart" id="chart2"></div> 
        <div class="chart" id="chart3"></div>
    </div>
</template>
<script lang="ts">
import * as echarts from 'echarts'
export default {
    setup() {
        const myChart = echarts.init(document.getElementById('chart1'), null,{
            width:200,
            height:200
        });
        

        // 使用刚指定的配置项和数据显示图表。
        const option = {
            title: {
                text: '实时人流占比',
                textStyle: {
                    color: '#ffffff',
                },
                left:'center',

            },
            color: [
                    '#0670ec',
                    '#2f4554',
                ],
            legend: {
                top: '17%',
                data:['入流','出流'],
                textStyle: { color: '#fff' },
            },
            tooltip: {
                showContent: false
            },
            dataset: {
                source: [
                ['number', 'real time'],
                ['入流', 86.5],
                ['出流', 41.1]
                ]
            },
            series: [
                {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                encode: {
                    itemName: 'number',
                    value: 'real time'
                },
                label: {
                show: false
                },
                }
            ]
            };
            
        myChart.setOption(option);

        const myChart2 = echarts.init(document.getElementById('chart2'), null,{
            width:200,
            height:200
        });
        // 使用刚指定的配置项和数据显示图表。
        const option2 = {
            title:{
                text:'历史人流数据',
                textStyle: {
                    color: '#ffffff',
                },
                left:'center',
            },
            color: [
                    '#0670ec',
                    '#2f4554',
                ],
            legend: {
                data: ['入流', '出流'],
                top:'13%',
                textStyle: { color: '#fff' },
            },
            grid: {
                left: '3%',
                right: '5%',
                bottom: '3%',
                containLabel: true
            },
              xAxis: [
                {
                type: 'category',
                boundaryGap: false,
                data: ['一', '二', '三', '四', '五', '六', '日']
                }
            ],
            yAxis: [
                {
                type: 'value'
                }
            ],
            series: [
                {
                name: '入流',
                type: 'line',
                stack: 'Total',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: [120, 132, 101, 134, 90, 230, 210]
                },
                {
                name: '出流',
                type: 'line',
                stack: 'Total',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: [220, 182, 191, 234, 290, 330, 310]
                },
            ]
            };
        myChart2.setOption(option2);   

        const myChart3 = echarts.init(document.getElementById('chart3'), null,{
            width:200,
            height:230
        });

        function getVirtulData(year) {
            year = year || '2017';
            const date = +echarts.number.parseDate(year + '-01-01');
            const end = +echarts.number.parseDate(+year + 1 + '-01-01');
            const dayTime = 3600 * 24 * 1000;
            const data = [];
            for (let time = date; time < end; time += dayTime) {
                data.push([
                echarts.format.formatTime('yyyy-MM-dd', time),
                Math.floor(Math.random() * 1000)
                ]);
            }
            console.log(data[data.length - 1]);
            return data;
        }

        const option3 = {
            title:{
                text:'历史异常程度',
                textStyle: {
                    color: '#ffffff',
                },
                left:'center',
            },
            visualMap: [
                {
                min: 0,
                max: 1000,
                calculable: true,
                seriesIndex: [0],
                orient: 'horizontal',
                left: '13%',
                bottom: 5,
                inRange: {
                color: ["#95e7fa", "#75d2f8", "#54b3f1", "#3691e7", "#2179df", "#1368da", "#0457d5"]
                },
                textStyle:{
                    color: '#ffffff'
                }
                }
            ],
            calendar: [
                {
                orient: 'vertical',
                yearLabel: {
                    margin: 40,
                    show: false
                },
                dayLabel: {
                    firstDay: 0,
                    nameMap: ['一', '二', '三', '四', '五', '六', '日'],
                    color: '#ffffff'
                },
                monthLabel: {
                    nameMap: 'cn',
                    margin: 1,
                    show: false,
                },
                cellSize: 20,
                top: '25%',
                left: 'center',
                range: '2017-04'
                }
            ],
            series: [
                {
                type: 'heatmap',
                coordinateSystem: 'calendar',
                calendarIndex: 0,
                data: getVirtulData('2017')
                }
            ]
        }
        myChart3.setOption(option3); 
    }
}
</script>
<style scoped>
.charts{
    width: 90%;
    height: 80%;
    padding-top: 5%;
    padding-bottom: 5%;
    padding-left: 5%;
    padding-right: 5%;
}

.chart{
    width: 100%;
    height: 40%;
}
</style>

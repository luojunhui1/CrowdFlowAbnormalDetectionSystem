<template>
<el-container :direction="vertical">
    <el-header height="60px" :direction="horizontal">
        <el-container>
            <div style="width: 50px; height: 40px; align-top:2px">
                <el-image :src="require('../../assets/logo.png')" fit="fit" :lazy="true"></el-image>
            </div>
            <div class="title-container">
                <p class="system-title">
                    <span class="span-z">人群流动异常检测系统</span>
                    <br>
                    <span class="span-e"> Crowd Flow Abnormal Detection System</span>
                </p>
            </div>

            <div style="display:inline-block">
                <el-row>
                    <el-col :span="8" :offset="9">{{nowTime}}</el-col>
                    <el-col :span="6" :offset="1">全市人群流量异常值:{{totalAbmormalDegree}}</el-col>
                </el-row>
            </div>
        </el-container>
    </el-header>

    <el-container :direction="horizontal">
        <el-aside width="180px">
            <Menu></Menu>
        </el-aside>
        <el-container :direction="vertical">
            <el-main height="">      
                <iframe :src="mapHtmlPath"></iframe>
            </el-main>
            <el-footer height="">
                <!-- Footer content -->
            </el-footer>
        </el-container>
        <el-aside width="235px">
           <div class="charts">
                <div class="chart" id="chart1"></div>
                <div class="chart" id="chart2"></div> 
                <div class="chart" id="chart3"></div>
           </div>
        </el-aside>
    </el-container>
</el-container>
</template>

<script lang="ts">

import axios from 'axios'
import Menu from './slider/menu.vue'
import * as echarts from 'echarts'

export default {
    methods:
    {
        nowTimes()
        {
            this.timeFormate(new Date());
            setInterval(this.nowTimes,1000);
        },
        timeFormate(timeStamp) {
            const year = new Date(timeStamp).getFullYear();
            const month =new Date(timeStamp).getMonth() + 1 < 10? "0" + (new Date(timeStamp).getMonth() + 1): new Date(timeStamp).getMonth() + 1;
            const date =new Date(timeStamp).getDate() < 10? "0" + new Date(timeStamp).getDate(): new Date(timeStamp).getDate();
            const hh =new Date(timeStamp).getHours() < 10? "0" + new Date(timeStamp).getHours(): new Date(timeStamp).getHours();
            const mm =new Date(timeStamp).getMinutes() < 10? "0" + new Date(timeStamp).getMinutes(): new Date(timeStamp).getMinutes();
            const ss =new Date(timeStamp).getSeconds() < 10? "0" + new Date(timeStamp).getSeconds(): new Date(timeStamp).getSeconds();
            const week = new Date(timeStamp).getDay();
            const weeks = ["日","一","二","三","四","五","六"];
            const getWeek = "星期" + weeks[week];
            this.nowTime = year + "年" + month + "月" + date +"日"+" "+hh+":"+mm+':'+ss+getWeek;
        },
    },
    data(){
       return {
            serverUrl: "http://127.0.0.1:5003",
            nowTime:'',
            totalAbmormalDegree:1.67,
            mapHtmlPath:"map.html",
            tabelData:'',
            inflowHist:Array<number>(7),
            outflowHJist:Array<number>(7),
            adHist:Array<number>(7)
       }
   },
   created:function(){
        const param = new FormData();
        param.append('state', 'init')
        const config = {
            headers: {'content-Type': 'multipart/form-data'},
        }
        axios
        .post(this.serverUrl + '/state', param, config)
        .then((res)=>{
            console.log(res)
        })
    },
    mounted()
    {
        this.nowTimes();

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
    },
    components: {
    Menu,
    }
}
</script>

<style scoped>
.mainContainer {
    display: flex;
    flex-direction: row;
    flex: 1;
    flex-basis: auto;
    box-sizing: border-box;
    min-width: 0;
}

.el-header{
    background-color:#2f3447;
    padding: 8px 20px
}

/deep/ .el-card{
    background-color: #2f3447;
    padding: 0 10px;
    border-style: none;
    color:#ffffff;
}

.el-aside{
    width: 174px;
    background-color: #2f3447;
    text-align: center;
    box-sizing: border-box;
}

.title-container{
    max-height: 50px; 
    overflow: hidden; 
    margin: 0px 10px; 
    width:350px; 
    padding-top:0px; 
    display: flex;
}

.system-title{
    color:#0670EC; 
    margin: 0; 
    padding: 2px 0px;
    text-align-last: justify;
    text-align: justify;
}
.span-z{
    font-size: 20px;
    font-weight: bold;
    display: inline;
    line-height: 20px;

}
.span-e{
    font-size: 10px;
    font-weight: bold;
    display: inline;
}
.el-col{
    margin-top:10px; 
    font-size: 16px; 
    font-weight: bold;
    color:#0670EC; 
}
.el-menu {
  border-right: none;
}
.el-main{
    padding: 0px;
    width: 100%;
    overflow: hidden;
}
.area_b{
    border-radius: 0px;
    border-color: #2f3447;
    border-width: 1px;
    background-color: aquamarine;
    opacity: 0.4;
    width:22px; 
    height:22px;
}

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
.el-footer{
    height:20px;
    flex-shrink: 0;
    background-color: #2f3447;
}
</style>
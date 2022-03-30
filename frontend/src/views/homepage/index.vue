<template>
  <div class="home-container">
    <z-row :gutter="15">
      <z-col :span="7">
        <div class="echartList">
          <div class="MeunList">
            <div class="MeunListTitle">功能菜单</div>
            <div class="MeunItem">
                <div class="MeunTitle">
                  <button class="MeunButton" @click="CrowdPerception">人群流动态势感知</button>
                </div>
            </div>
            <div class="MeunItem">
              <div class="MeunTitle">
                <button class="MeunButton" @click="CrowdPrediction">区域人群流量预测</button>
              </div>
            </div>
            <div class="MeunItem">
              <div class="MeunTitle">
                <button class="MeunButton" @click="CrowdAD">区域人群异常检测</button>
              </div>
            </div>
          </div>
          <div class="divideLine"></div>
          <div class="chartLeft">
            <box-container :boxTitle=rankNames[meunIndex]>
              <rank-chart />
            </box-container>
          </div>
        </div>
      </z-col>
      <z-col :span="10">
        <div class="mapBox" style="width:100%;height:85%">
          <grid-map />
        </div>
        <div class="bottomImage"></div>
      </z-col>
      <z-col :span="7">
        <div class="echartList">
          <div class="chart-item">
            <box-container :boxTitle=right1Names[meunIndex]>
              <right-chart-1 />
            </box-container>
          </div>
          <div class="chart-item">
            <box-container :boxTitle=right2Names[meunIndex]>
              <right-chart-2 />
            </box-container>
          </div>
          <div class="chart-item">
            <box-container :boxTitle=right3Names[meunIndex]>
              <right-chart-3 />
            </box-container>
          </div>
        </div>
      </z-col>
    </z-row>
  </div>
</template>

<script>
import { ZRow, ZCol } from "@UI/components";
import boxContainer from "@/components/boxContainer/index";
import fourAngel from "@/components/fourAngel/index";
import countTo from "@/components/countTo/index";

import {
  cityCount,
  typeCount,
  scatterMap,
  wordChart,
  funnelChart,
  lineChart,
  liquidChart,
  rankChart,
  gridMap,
  rightChart1,
  rightChart2,
  rightChart3
} from "./components";
import useResize from "@/componentApi/useResize.js";
import { useStore } from "vuex";
import { ref } from "vue";

export default {
  name: "homepage",
  components: {
    ZRow,
    ZCol,
    boxContainer,
    cityCount,
    typeCount,
    scatterMap,
    wordChart,
    funnelChart,
    lineChart,
    liquidChart,
    rankChart,
    gridMap,
    rightChart1,
    rightChart2,
    rightChart3,
    fourAngel,
    countTo,
  },
  setup(props, context) {
    const {sum, year, areaIndex, meunIndex, setCommitMeunIndex } = useResize();
    const rankNames = ["城市区域流量排名", "流量增长预测排名", "城市区域异常排名"]
    const right1Names = ["区域流量变化", "模型拟合曲线", "区域历史异常"]
    const right2Names = ["实时出入流量比例", "区域流量预测", "区域空间异常排名"]
    const right3Names = ["实时区域流量转移", "区域流量转移预测", "区域时间异常排名"]
    const CrowdPerception=()=>{
      setCommitMeunIndex(0)
    }

    const CrowdPrediction=()=>{
      setCommitMeunIndex(1)
    }

    const CrowdAD=()=>{
      setCommitMeunIndex(2)
    }
    
    return {
      year,
      sum,
      areaIndex,
      meunIndex,
      rankNames,
      right1Names,
      right2Names,
      right3Names,
      CrowdPerception,
      CrowdPrediction,
      CrowdAD
    };
  },
};
</script>

<style lang="scss" scoped>
.home-container {
  width: 100%;
  height: 100%;
  position: relative;
  // padding-left: 2%;
  .echartList {
    width: 80%;
    height: 100%;
    display: flex;
    flex-wrap: wrap;
    margin: 0 auto;
    align-content: space-between;
    background: url("~@/assets/image/border_lb.gif") no-repeat bottom left/60%,
                url("~@/assets/image/border_ru.gif") no-repeat top right/60%;
    
    .MeunList{
      width: 100%;
      height: 40%;
      padding-top: 5%;
      .MeunListTitle{
        font-size: 1.4rem;
        font-family: "PangMen";
        text-align: center;
        color: #ffffff;
        letter-spacing: 0.2em;
        margin-top: 5%;
      }
      .MeunItem{
        width: 80%;
        height: 25%;  
        margin: 2.5% auto;
        background: url("~@/assets/image/meun_item_bg.png") no-repeat center center/70%;
        .MeunTitle{
          text-align: center;
          padding-top: 9%;
          .MeunButton{
            font-size: 1.3rem;
            font-family: "PangMen";
            text-align: center;
            color: #ffffff;
            background-color:transparent;
            border-style:none;
            letter-spacing: 0.2em;
          }
        }
      }
    }
    .divideLine{
      width: 100%;
      height: 5%;
      background: url("~@/assets/image/divide.png") no-repeat center center/70%;
    }
    .chartLeft{
      width: 100%;
      height: 52%
    }
    .chart-item {
      height: 30.1%;
      width: 100%;
      margin: 4% 0;
    }
  }
  .mapBox{
      padding-top: 1.3%;
    }
  .bottomImage{
    height: 6%;
    background: url("~@/assets/image/map_bottom.png") no-repeat center center/100%,
  }
}
</style>

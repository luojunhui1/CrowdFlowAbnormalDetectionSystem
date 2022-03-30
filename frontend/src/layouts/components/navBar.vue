<template>
  <div class="nav-wrapper">
    <div class="bar-title" @click.stop="toHome">人群流动异常检测系统</div>
    <div class="abnormal-index">全市人群流动异常指数
      <div class="adIndex">{{abnormalIndex}}</div>
    </div>
    <div class="time">{{ date }} {{ time }} {{weekDay}}</div>
  </div>
</template>

<script>
import { setup, ref, onMounted, computed } from "vue";
import { getDate, getTime, getWeekDay} from "@/utils/date.js";
import useResize from "@/componentApi/useResize.js";
import { useRoute, useRouter } from "vue-router";

export default {
  name: "navBar",

  setup(props, context) {
    //年月日
    const date = getDate();
    const weekDay = getWeekDay();
    const abnormalIndex = 0.37;
    //时分秒
    const time = ref(getTime());
    const router = useRouter();
    const route = useRoute();
    const { parentInfo, removeCommitMapInfo } = useResize();
    let isHome = computed(() => route.path == "/homepage");

    const chooseArea = (item, index) => {
      if (parentInfo.value.length === index + 1) {
        return;
      }
      removeCommitMapInfo(index + 1);
    };

    const toHome = () => {
      if (route.path == "/homepage") {
        return;
      }
      router.push("/homepage");
    };

    onMounted: {
      setInterval(() => {
        time.value = getTime();
      }, 1000);
    }

    return {
      date,
      time,
      weekDay,
      abnormalIndex,
      parentInfo,
      chooseArea,
      toHome,
      isHome,
    };
  },
};
</script>

<style lang="scss" scoped>
@font-face {
	font-family: 'PangMen';
	src: url('../../assets/font/PangMen.ttf')  format('truetype'), /* Safari, Android, iOS */
  }
.nav-wrapper {
  height: 65px;
  line-height: 50px;
  width: 100%;
  background: url("../../assets/image/nav_bg.png") no-repeat;
  background-size: 100% 100%;
  text-align: center;
  position: relative;
  color: #0670EC;

  .bar-title {
    font-size: 1.6rem;
    font-family: "PangMen";
    letter-spacing: 0.5em;
    padding-top: 0.8%;
    cursor: pointer;
  }

  .time {
    position: absolute;
    right: 10%;
    top: 50%;
    transform: translateY(-45%);
    font-family: "PangMen";
    font-weight: normal;
    font-size: 1.4rem;
  }
  .mapChoose {
    position: absolute;
    left: 10px;
    bottom: -40px;

    .title {
      padding: 4px;
      border-top: 1px solid rgba(147, 235, 248, 0.8);
      border-bottom: 1px solid rgba(147, 235, 248, 0.8);
      cursor: pointer;
      font-size: 14px;
    }

    .icon {
      font-family: "PangMen";
      font-size: 25px;
      margin: 0 11px;
    }
  }
  .abnormal-index{
    position: absolute;
    font-family: "PangMen";
    left: 11%;
    top: 50%;
    transform: translateY(-45%);
    font-weight: normal;
    font-size: 1.4rem;
    display: block;
    white-space: nowrap;
  }
  .adIndex{
    display: inline-block;
    color: #ffffff;
    font-size: 1.6rem;
  }
}
</style>

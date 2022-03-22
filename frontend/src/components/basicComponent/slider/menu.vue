<template>
	<!--左侧菜单组件-->
  <el-menu
    default-active="0"
    class="el-menu-vertical-demo"
    @select="menuSelected"
    background-color="#2f3447"
    text-color="#fff"
    active-text-color="#ffd04b">
    <nav-menu :navMenus="menu"></nav-menu>
  </el-menu>
</template>

<script lang="ts">
  import NavMenu from './SliderMenu.vue';
	export default{
		components:{
			NavMenu
		},
		setup() {
      const menu = [
        {
          name: "重点区域人群异常",
          route: "/crowdFlowAnomalyDetection"
        },
        {
          name: "重点区域人群监测",
          route: "/crowdFlowMonitor"
        }
      ]
      const menuSelected = (key: string, keyPath: string[]) => {
           console.log(key, keyPath)
      }
      return {
        menu,
        menuSelected,
      }
    }
	}
</script>
 
<style>
</style>
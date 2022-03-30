<template>
  <div class="box-container">
      <div class="boxTitle">{{ boxTitle }}</div>
      <div class="main-content">
        <slot></slot>
      </div>
  </div>
</template>

<script>
export default {
  name: "boxContainer",
  props: {
    boxTitle: {
      type: String,
      default: "",
    },
  },
  components: {
  },
};
</script>

<style lang="scss" scoped>
@font-face {
	font-family: 'PangMen';
	src: url('../../assets/font/PangMen.ttf')  format('truetype'), /* Safari, Android, iOS */
  }

.box-container {
  width: 100%;
  height: 100%;
  .boxTitle {
    height: 28px;
    line-height: 28px;
    text-align: center;
    width: 100%;
    font-size: 1.2rem;
    color: #ffffff;
    font-family: "PangMen";
  }
  .main-content {
    height: calc(100% - 28px);
    width: 100%;
  }
}
</style>

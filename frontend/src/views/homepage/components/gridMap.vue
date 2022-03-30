<template>
  <div class="chart-wrapper" ref="gridMap"></div>
</template>

<script>
import echarts from "echarts";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { debounce } from "@/utils/index.js";
import useResize from "@/componentApi/useResize.js";
import { getGridMapData } from "@/api/chart";
import 'echarts/extension/bmap/bmap'

export default {
  name: "gridMap",
  setup() {
    let {meunIndex, setCommitAreaIndex} = useResize();

    var COLORS = ['#b4e0f3', '#70b4eb', '#1482e5', '#1c3fbf', '#070093', '#ea1807'];
    var lngExtent = [116.2045, 116.5794];
    var latExtent = [40.0666, 39.7781];
    var cellCount = [32, 32];

    var cellSizeCoord = [
      (latExtent[0] - latExtent[1]) / cellCount[0],
      (lngExtent[1] - lngExtent[0]) / cellCount[1]
    ];

    function renderItem(params, api) {
      var lngIndex = api.value(0);
      var latIndex = api.value(1);
      var pointLeftTop = getCoord(params, api, lngIndex, latIndex);
      var pointRightBottom = getCoord(params, api, lngIndex + 1, latIndex + 1);
      return {
        type: 'rect',
        shape: {
          x: pointLeftTop[0],
          y: pointLeftTop[1],
          width: pointRightBottom[0] - pointLeftTop[0],
          height: pointRightBottom[1] - pointLeftTop[1]
        },
        style: api.style({
          stroke: 'rgba(0,0,0,0.1)'
        }),
        styleEmphasis: api.styleEmphasis()
      };
    }

    function getCoord(params, api, lngIndex, latIndex) {
      var coords = params.context.coords || (params.context.coords = []);
      var key = lngIndex + '-' + latIndex;
      // bmap returns point in integer, which makes cell width unstable.
      // So we have to use right bottom point.
      return (
        coords[key] ||
        (coords[key] = api.coord([
          +(lngExtent[0] + lngIndex * cellSizeCoord[1]).toFixed(6),
          +(latExtent[0] - latIndex * cellSizeCoord[0]).toFixed(6)
        ]))
      );
    }

    let myChart = ref(null);
    const gridMap = ref(null);
    
    const resizeHandler = debounce(() => {
      if (myChart) {
        myChart.resize();
      }
    }, 200);

    onMounted(() => {
      getMapJson();
      window.addEventListener("resize", resizeHandler);
    });
    onBeforeUnmount(() => {
      window.removeEventListener("resize", resizeHandler);
    });

    //通过百度获取geoJson数据
    const getMapJson = async () => {
      let data = await getGridMapData({meunIndex})

      let map_data = []
      for(var i in data)
      {
        map_data.push([Math.floor((i)/32), i%32, data[i]])
      }

      initEcharts(map_data);
    };


    //渲染echarts图
    const initEcharts = (data) => {
      myChart = echarts.init(gridMap.value || gridMap);

      myChart.setOption(
      {
        mapOptions: {enableMapClick: false},
        tooltip: {
				trigger: 'item',
				formatter: function(params) {
					return ("坐标：(" + 
						params.value[0] + ", " + params.value[1] + ")" + 
						'<br />' + "等级：" +
						params.value[2]
					);
				},
				enterable: true,
				alwaysShowContent: true,
				position: function(point) {
					return [point[0] + 5, point[1] + 5];
				}
			},
        visualMap: {
        type: 'piecewise',
        inverse: true,
        top: 10,
        left: 10,
        pieces: [
          {
            value: 0,
            color: COLORS[0]
          },
          {
            value: 1,
            color: COLORS[1]
          },
          {
            value: 2,
            color: COLORS[2]
          },
          {
            value: 3,
            color: COLORS[3]
          },
          {
            value: 4,
            color: COLORS[4]
          },
          {
            value: 5,
            color: COLORS[5]
          }
        ],
        borderColor: '#ccc',
        borderWidth: 2,
        backgroundColor: '#eee',
        dimension: 2,
        inRange: {
          color: COLORS,
          opacity: 0.6
        }
      },
      series: [
        {
          type: 'custom',
          coordinateSystem: 'bmap',
          renderItem: renderItem,
          animation: false,
          emphasis: {
            itemStyle: {
              color: 'yellow'
            }
          },
          encode: {
            tooltip: 2
          },
          data: data
        }
      ],
      bmap: {
        center: [116.391958, 39.922353],
        zoom: 12,
        key: 'TWnZ8qr6nheOeePhhsPSc55wTwckG7E2',
        roam: true,
        mapStyle: {
          styleJson: [{
    "featureType": "land",
    "elementType": "geometry",
    "stylers": {
        "color": "#f5f6f7ff"
    }
}, {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": {
        "color": "#c4d7f5ff"
    }
}, {
    "featureType": "green",
    "elementType": "geometry",
    "stylers": {
        "color": "#dcf2d5ff"
    }
}, {
    "featureType": "highway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffe59eff"
    }
}, {
    "featureType": "highway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#f5d48cff"
    }
}, {
    "featureType": "nationalway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#fff6ccff"
    }
}, {
    "featureType": "provincialway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#fff6ccff"
    }
}, {
    "featureType": "cityhighway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#fff6ccff"
    }
}, {
    "featureType": "arterial",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#fff6ccff"
    }
}, {
    "featureType": "nationalway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#f2dc9dff"
    }
}, {
    "featureType": "provincialway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#f2dc9dff"
    }
}, {
    "featureType": "cityhighway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#f2dc9dff"
    }
}, {
    "featureType": "arterial",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#f2dc9dff"
    }
}, {
    "featureType": "building",
    "elementType": "geometry.sidefill",
    "stylers": {
        "color": "#e6ebf0ff"
    }
}, {
    "featureType": "building",
    "elementType": "geometry.topfill",
    "stylers": {
        "color": "#e6ebf0ff"
    }
}, {
    "featureType": "building",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#d8e2ebff"
    }
}, {
    "featureType": "tertiaryway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "tertiaryway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "fourlevelway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "fourlevelway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "local",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "local",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "scenicspotsway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "scenicspotsway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "universityway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "universityway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "vacationway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#dfe4ebff"
    }
}, {
    "featureType": "vacationway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "town",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 18
    }
}, {
    "featureType": "town",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "town",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "highway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#c0792dff"
    }
}, {
    "featureType": "highway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "nationalway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#c0792dff"
    }
}, {
    "featureType": "nationalway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff60"
    }
}, {
    "featureType": "provincialway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#c0792dff"
    }
}, {
    "featureType": "provincialway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "cityhighway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#c0792dff"
    }
}, {
    "featureType": "cityhighway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#c0792dff"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "cityhighway",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "provincialway",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "nationalway",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "highway",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "companylabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "companylabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "companylabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "lifeservicelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "lifeservicelabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "lifeservicelabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "carservicelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "carservicelabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "carservicelabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "financelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "financelabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "financelabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "tertiaryway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "tertiaryway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "tertiaryway",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "fourlevelway",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "fourlevelway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "fourlevelway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "local",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "local",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "local",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "companylabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "lifeservicelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "carservicelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "financelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "manmade",
    "elementType": "geometry",
    "stylers": {
        "color": "#f5f6f7ff"
    }
}, {
    "featureType": "subway",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "12"
    }
}, {
    "featureType": "subway",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "13"
    }
}, {
    "featureType": "subway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "12"
    }
}, {
    "featureType": "subway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "13"
    }
}, {
    "featureType": "subwaylabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,13",
        "level": "13"
    }
}, {
    "featureType": "subwaylabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,13",
        "level": "13"
    }
}, {
    "featureType": "subwaylabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,13",
        "level": "13"
    }
}, {
    "featureType": "railway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "10"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "11"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "12"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "13"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "14"
    }
}, {
    "featureType": "scenicspotslabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "15"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "10"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "11"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "12"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "13"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "14"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "15"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "10"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "11"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "12"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "13"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "14"
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "10,15",
        "level": "15"
    }
}, {
    "featureType": "district",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "district",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "city",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "city",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "city",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "country",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "country",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "continent",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#a77726ff"
    }
}, {
    "featureType": "continent",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "medicallabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "medicallabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "medicallabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "medicallabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "12"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "13"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "14"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "15"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "16"
    }
}, {
    "featureType": "entertainmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "17"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "12"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "13"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "14"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "15"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "16"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "17"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "12"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "13"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "14"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "15"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "16"
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,17",
        "level": "17"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "estatelabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "estatelabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "estatelabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "estatelabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "13"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "14"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "15"
    }
}, {
    "featureType": "estatelabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,16",
        "level": "16"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "businesstowerlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "12"
    }
}, {
    "featureType": "businesstowerlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "13"
    }
}, {
    "featureType": "businesstowerlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "14"
    }
}, {
    "featureType": "businesstowerlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "15"
    }
}, {
    "featureType": "businesstowerlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "16"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "12"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "13"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "14"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "15"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "16"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "12"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "13"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "14"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "15"
    }
}, {
    "featureType": "businesstowerlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,16",
        "level": "16"
    }
}, {
    "featureType": "governmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "13"
    }
}, {
    "featureType": "governmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "14"
    }
}, {
    "featureType": "governmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "15"
    }
}, {
    "featureType": "governmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "16"
    }
}, {
    "featureType": "governmentlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "17"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "13"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "14"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "15"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "16"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "17"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "13"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "14"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "15"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "16"
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,17",
        "level": "17"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "13"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "14"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "15"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "16"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "17"
    }
}, {
    "featureType": "restaurantlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "18"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "13"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "14"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "15"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "16"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "17"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "18"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "13"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "14"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "15"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "16"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "17"
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "13,18",
        "level": "18"
    }
}, {
    "featureType": "hotellabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "14"
    }
}, {
    "featureType": "hotellabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "15"
    }
}, {
    "featureType": "hotellabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "16"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 22,
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "14"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 22,
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "15"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 22,
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "16"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "14"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "15"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "16"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "14"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "15"
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "14,16",
        "level": "16"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "11"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "12"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "13"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "14"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "15"
    }
}, {
    "featureType": "shoppinglabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "16"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "11"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "12"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "13"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "14"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "15"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "16"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "11"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "12"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "13"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "14"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "15"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,16",
        "level": "16"
    }
}, {
    "featureType": "shoppinglabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "hotellabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "restaurantlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "governmentlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "companylabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 24
    }
}, {
    "featureType": "entertainmentlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "medicallabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "scenicspotslabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "airportlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "water",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "manmade",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#9ca0a3ff"
    }
}, {
    "featureType": "manmade",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "education",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "transportationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "12"
    }
}, {
    "featureType": "transportationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "13"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "12"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "13"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "12"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "12,13",
        "level": "13"
    }
}, {
    "featureType": "educationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "11"
    }
}, {
    "featureType": "educationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "12"
    }
}, {
    "featureType": "educationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "13"
    }
}, {
    "featureType": "educationlabel",
    "stylers": {
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "14"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "11"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "12"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "13"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "14"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "11"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "12"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "13"
    }
}, {
    "featureType": "educationlabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off",
        "curZoomRegionId": "0",
        "curZoomRegion": "11,14",
        "level": "14"
    }
}, {
    "featureType": "transportationlabel",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "manmade",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
}, {
    "featureType": "scenicspots",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#ab76b6ff"
    }
}, {
    "featureType": "scenicspots",
    "elementType": "labels.text",
    "stylers": {
        "fontsize": 23
    }
      }],
        }
      }
      }     
      );

      myChart.getZr().off("click");
      myChart.getZr().on("click", (params) => {
        const areaIndex = 32*(params.target.dataIndex % 32) + Math.floor(params.target.dataIndex / 32);
        setCommitAreaIndex(areaIndex)
      });
    };
    watch(
      meunIndex,
      (nl, ol) => {
        getMapJson();
      },
      { lazy: false }
    );
    return {
      gridMap,
      myChart,
    };
  },
};
</script>

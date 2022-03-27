import folium
from flask import *
from datetime import datetime, timedelta
from src.utils import *
from src.geo import *
from src.temp import *
import numpy as np

app = Flask(__name__)
app.secret_key = 'secret!'

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)

hist_data = get_data()
temp_d = Temp()
geo_d = Geo()
colors_map = ['#5AC7F5', '#ff9900', '#ff4600', '#ff0500']# normal, mildly abnormal, moderately abnormal, severely abnormal
polygons = get_polygons()
center_lat = 39.922353
center_lon = 116.391958

def ad2color(ad):
    if ad < 0:
        return colors_map[1]
    elif ad<=2:
        return colors_map[2]
    return colors_map[3]

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/init', methods=['GET', 'POST'])
def init_map():
    return jsonify({'html_map_path': "map.html"})


@app.route('/cal', methods=['GET', 'POST'])
def get_html():
    bj_map = folium.Map(location=[center_lat , center_lon], zoom_start=12, tiles='CartoDB positron')
    folium.TileLayer(
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr="&copy; <a href=http://ditu.amap.com/>高德地图</a>",
        min_zoom=0,
        max_zoom=19,
        control=True,
        show=True,
        overlay=False,
        name="aMAP"
    ).add_to(bj_map)

    real_now = datetime.now()
    now_time = datetime(year=2017, month=real_now.month + 6, day=real_now.day, hour=real_now.hour)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds()//3600)
    cur_inflow = hist_data[td, 0, :, :].reshape(1024, 1)
    cur_outflow = hist_data[td, 1, :, :].reshape(1024, 1)

    t_ad = temp_d.get_temp_ad(cur_inflow, cur_outflow, now_time)
    g_ad = geo_d.get_geo_ad(cur_inflow, cur_outflow, method='ifroest')

    ads = np.concatenate([t_ad, g_ad], axis=1)

    # skyline algorithm
    ad_points = []
    domains = 0
    for i in range(0, 1024):
        for j in range(0, 1024):
            domains = 0
            for k in range(0, ads.shape[1]):
                if ads[j][k] > ads[i][k]:
                    domains += 1
            if domains == ads.shape[1]:
                domains = -1
                break
        if domains != -1:
            ad_points.append(i)

    # calcalute the minimum euclidean distance between abormal point and each
    # normal point as the abnormal degree
    ed = []
    for i in range(0, 1024):
        if i not in ad_points:
            ed.append([np.sum((ads[i] - ads[j])**2) for j in ad_points])
    
    ad = np.max(ed, axis=0)
    ad_std =  np.std(ad, ddof=1)
    ad_lower = np.mean(ad) - np.std(ad, ddof=1)

    colors = [colors_map[0] for _ in range(0, 1024)]

    for i in range(0, len(ad_points)):
        colors[ad_points[i]] = ad2color((ad[i] - ad_lower)/ad_std)

    i = 0
    for grid in list(polygons):
        _curr_ = folium.Polygon(
            locations=grid,
            color='black',
            weight=0.1,
            fill_color=colors[i],
            fill_opacity=0.8 if i in ad_points else 0.3,
            fill=True,
        )
        _curr_.add_to(bj_map)
        i = i + 1

    bj_map.save("../frontend/public/ad_map.html")

    return jsonify({'html_map_path': "map.html"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
import folium
from flask import *
from datetime import datetime, timedelta
from src.utils import *
from src.geo import *
from src.temp import *

app = Flask(__name__)
app.secret_key = 'secret!'

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)

hist_data = get_data()
temp_d = Temp()
geo_d = Geo()
colors = ['#e0f2a8', '#9ad486', '#369c53', '#0d723b', '#005c32', '#004629']
polygons = get_polygons()

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/state', methods=['GET', 'POST'])
def get_html():
    print("get post")
    center_lat = 39.922353
    center_lon = 116.391958
    
    bj_map = folium.Map(location=[center_lat , center_lon], zoom_start=12, tiles='CartoDB positron')

    now_time = datetime(2017, 10, 1, 0)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds()//3600)
    cur_inflow = hist_data[td, 0, :, :].reshape(1024, 1)
    cur_outflow = hist_data[td, 1, :, :].reshape(1024, 1)

    ads_t = temp_d.get_temp_ad(cur_inflow, cur_outflow, now_time)
    ads_g = geo_d.get_geo_ad(cur_inflow, cur_outflow)
    ads = np.concatenate([ads_t, ads_g], axis=1)
    ad = np.sum(ads, axis=1)
    ad = [1 if i > 0.7 else i for i in ad]

    i = 0
    for grid in list(polygons):
        _curr_ = folium.Polygon(
            locations=grid,
            color='black',
            weight=0.1,
            fill_color='#ff0000' if ad[i] == 1 else colors[
                math.floor(ad[i]/ 0.15)],
            fill_opacity=0.3,
            fill=True,
        )
        _curr_.add_to(bj_map)
        i = i + 1

    bj_map.save("../frontend/public/map.html")

    return jsonify({'html_map_path': "map.html"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
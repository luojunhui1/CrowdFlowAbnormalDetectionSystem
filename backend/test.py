import torch
from src.geo import *
from src.temp import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data

if __name__ == '__main__':
    hist_data = get_data()
    temp_d = Temp()
    geo_d = Geo()

    center_lat = 39.922353
    center_lon = 116.391958

    bj_map = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')

    now_time = datetime(2017, 10, 1, 0)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)
    cur_inflow = hist_data[td, 0, :, :].reshape(1024, 1)
    cur_outflow = hist_data[td, 1, :, :].reshape(1024, 1)

    ads_t = temp_d.get_temp_ad(cur_inflow, cur_outflow, now_time)
    ads_g = geo_d.get_geo_ad(cur_inflow, cur_outflow)

    ads = np.concatenate([ads_t, ads_g], axis=1)
    ad = np.sum(ads, axis=1)
    ad.sort()
    print(ad[int(ad.shape[0] * 0.75)])
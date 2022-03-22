import torch
from src.geo import *
from src.temp import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)  # 设置打印选项：输出数组元素数目上限为无穷

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

    # 绘制ads三维度数据折线图
    # ig = plt.figure(figsize=(15, 20))
    # colors = ['#2B8CE0', '#E04841', '#8E942B']
    # for i in range(0, ads.shape[1]):
    #     ad = ads[:, i]
    #     ax = fig.add_subplot(3, 1, i + 1)
    #     plt.plot(range(0, 1024), ad, c=colors[i])

    fig = plt.figure(figsize=(10, 10))
    pred = temp_d.predict(now_time)
    cur_x = ad_points[:5] + [np.random.randint(1024) for _ in range(5)]

    ax = fig.add_subplot(2, 2, 1)
    ax.bar(range(0, 10), cur_inflow[cur_x, 0], color='#4192F5', label='origin')
    ax.bar(range(0, 10), pred[cur_x, 0], color='#5AC7F5', label='pred')
    ax.set_title('inflow abnormal detection')
    plt.xticks(range(0, 10), cur_x)
    ax.legend()

    ax = fig.add_subplot(2, 2, 2)
    ax.bar(range(0, 10), cur_outflow[cur_x, 0], color='#4192F5', label='origin')
    ax.bar(range(0, 10), pred[cur_x, 1], color='#5AC7F5', label='pred')
    ax.set_title('outflow abnormal detection')
    plt.xticks(range(0, 10), cur_x)
    ax.legend()

    # 绘制热力图
    def get_agg_class_areas(interval):
        # 将实时输入流、输出流作为二维数据进行异常值检测
        agg_class_fp = h5py.File("data/agg_interval.hdf5", "r")["%s" % interval]
        agg_class_areas = []
        for key in agg_class_fp.keys():
            agg_class_areas.append(agg_class_fp[key])
        return agg_class_areas


    agg_class_areas = get_agg_class_areas(1)

    gradient = np.linspace(0, 1, 6)[1:]

    ax = fig.add_subplot(2, 2, 3)
    colors = np.zeros(shape=(32, 32))

    eax = ad_points[1]

    for c in agg_class_areas:
        if eax in c:
            for i in c:
                colors[i // 32, i % 32] = gradient[int(g_ad[i] / 0.2)]
    ax.imshow(colors, aspect='auto', cmap='Blues')
    ax.axhline(y=eax//32, c='#F24F3F', ls='--')
    ax.axvline(x=eax % 32, c='#F24F3F', ls='--')

    # 绘制三维散点图
    colors = []
    for i in range(0, 1024):
        if i in ad_points:
            colors.append('#F24F3F')
        else:
            colors.append('#4192F5')

    ax = fig.add_subplot(2, 2, 4, projection='3d')  # 设置三维轴
    ax.scatter3D(ads[:, 0], ads[:, 1], ads[:, 2], c=colors)  # 三个数组对应三个维度（三个数组中的数一一对应）

    plt.show()

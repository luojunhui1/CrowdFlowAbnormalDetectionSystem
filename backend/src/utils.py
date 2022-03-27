import math
import numpy as np
import h5py
import folium
from tqdm import tqdm


def get_polygons(clat=39.922353, clon=116.391958, acc=1000):
    """将区域划分成32*32网格
    Param
    ------
    clat: float

    center latitude, 划分区域的中心纬度

    clat: float

    center longitude, 划分区域的中心经度

    acc: int

    accuracy, 精度, 单位为m
    """
    polar_radius = 6356908.8  # 地球极半径
    lat_perimeter = 2 * math.pi * 1000 / math.sqrt(
        1 / (6377.830 ** 2) + (math.tan(math.radians(clat)) / 6377.830) ** 2)  # 区域所在纬半径

    lon_delta = 360 * acc / lat_perimeter  # 精度划分精度
    lat_delta = 360 * acc / (polar_radius * math.pi * 2)  # 维度划分精度

    lats = np.linspace(clat + 16 * lat_delta, clat - 16 * lat_delta, 33)
    lons = np.linspace(clon - 16 * lon_delta, clon + 16 * lon_delta, 33)

    polygons = []

    for i in range(0, 32):
        for j in range(0, 32):
            polygons.append([
                [lats[i], lons[j]],
                [lats[i], lons[j + 1]],
                [lats[i + 1], lons[j + 1]],
                [lats[i + 1], lons[j]]
            ])
    return polygons


def latlon2index(lat, lon, clat, clon, lat_delta, lon_delta):
    row_index = 16 + math.floor((lon - clon) / lon_delta)
    col_index = math.floor(16 - (lat - clat) / lat_delta)
    return row_index, col_index


def get_data(fname='data/UnicomBJ_flows.h5'):
    hp = h5py.File(fname, 'r')
    data = np.array(hp['data'])
    return data


def rgb2hex(rgbcolor):
    r, g, b, a = rgbcolor
    r = math.floor(r * 255)
    g = math.floor(g * 255)
    b = math.floor(b * 255)
    result = np.left_shift(r, 16) + np.left_shift(g, 8) + b
    return '#' + hex(result)[2:]


def get_map(clat=39.922353, clon=116.391958, polygons=None, colors=None, show=False, save=False):
    bj_map = folium.Map(location=[clat, clon], zoom_start=12, tiles='CartoDB positron', png_enabled=False)

    index = 0
    for grid in list(polygons):
        _curr_ = folium.Polygon(
            locations=grid,
            color='white',
            weight=1,
            fill_color=colors[index] if isinstance(colors[index], str) else rgb2hex(colors[index]),
            fill_opacity=0.4,
            fill=True,
        )
        _curr_.add_to(bj_map)
        index = index + 1

    if save:
        bj_map.save('../statics/bj.html')
    if show:
        return bj_map

    return None


def aggregate_by_time(data, time_intervel, row_index, col_index):
    """aggregate the crowd flow data for a specific gride [row_index, col_index] by time_interval
    and return an np.array() which has 2 dimensions representing the inflow and outflow, respectively.
    """
    res = []
    index_list = range(0, len(data), time_intervel)
    for in_out in [0, 1]:
        flow_list = []
        for i in index_list:
            flow_list.append(np.sum(data[i:i + time_intervel, in_out, row_index, col_index]))
        if index_list[-1] + 1 < len(data):
            flow_list.append(np.sum(data[index_list[-1]:len(data), in_out, row_index, col_index]))
        res.append(flow_list)
    return res[0], res[1]


def norm_by_row(data):
    # m = np.mean(data, axis = 1)
    res = (data.copy()).astype(np.float64)
    mx = np.max(data, axis=1)
    mn = np.min(data, axis=1)
    for index in range(0, len(data)):
        res[index] = (res[index] - mn[index]) / (mx[index] - mn[index])
    return res


def aggregate_by_geo(flow_data, method='kmeans', center_spec=False, **args):
    '''the input parameter 'flow_data' should be formated as [record_numbers, feature_numbers]

    parameter
    ---------
    flow_data:
    should be formated as [record_numbers, feature_numbers]

    method:
    optional, could be 'kmeans' , 'dist' and ...

    args:
    parameters varies as the 'method' changes

    returns
    -------
    kclasses:
    a list, every element contains all record index aggregated as one class

    mean_center:
    center point of every class
    '''
    if method == 'kmeans':
        kclasses = {}
        if not center_spec:
            root_areas_index = np.random.randint(low=0, high=1024, size=args['k'])
            # flow_data, normalize data in every signle row in 'flow_data' to transform the connotation of element from
            # *inflow or outflow amount* to 'inflow or outflow degree
            mean_center = flow_data[root_areas_index]
        else:
            mean_center = args['center']

        index = 0
        for record in tqdm(flow_data):
            cur_class = np.argmin(np.sum((mean_center - record) ** 2, axis=1))  # determine current class of record
            if cur_class not in kclasses.keys():
                kclasses[cur_class] = [index]  # add record index to the corresponding list
            else:
                kclasses[cur_class].append(index)
            k_class_len = len(kclasses[cur_class])  # number of records which belongs to the current class
            mean_center[cur_class] = (mean_center[cur_class] * (k_class_len - 1) + record) / (
                k_class_len)  # update center point of current class
            index += 1
        return kclasses, mean_center


def near_classes(area_classes, curr_area_index, delta=0.5):
    """find the near classes of 'curr_area' (near is defined on 4-Neighborhood) and
    return the near areas' classes and corresponding coordinates

    parameter
    ---------
    area_classes
    not the aggregation results by geo, but a 2-dim matrix whose index is area_index and value is class type

    curr_area_index
    index of target area, for 32*32 grid size, index is limited from 0 to 1023

    delta
    hyper-parameter, filtering those classes whose centers are deviating to the data of 'curr_area_index'

    return
    ------
    dict, key is class, value is area_indexes
    """

    res = {}
    near_coords = [curr_area_index - 32, curr_area_index + 32, curr_area_index - 1, curr_area_index + 1]
    for coord in near_coords:
        if coord > 1023 or coord < 0:
            continue
        if area_classes[coord] in res.keys():
            res[area_classes[coord]].append(coord)
        else:
            res[area_classes[coord]] = [coord]

    return res


def area_domain_class(class_area):
    area_class = [-1] * 1024
    curr = 0
    for class_key in class_area.keys():
        for ele in class_area[class_key]:
            area_class[ele] = curr
        curr += 1
    return area_class


def class_domain_area(area_class):
    class_area = {}
    for index in range(0, 1024):
        if area_class[index] not in class_area.keys():
            class_area[area_class[index]] = [index]
        else:
            class_area[area_class[index]].append(index)
    return class_area


def refine_geo_agg(area_class, flow=None, kc=None, k_mean=None, k_std=None, strong=False):
    for i in range(0, 1024):
        curr_res = near_classes(area_class, i, 0.5)
        if area_class[i] in curr_res.keys():
            continue
        else:
            min_dis = np.inf
            min_dis_class = area_class[i]
            for key in curr_res.keys():
                curr_dis = np.sum((flow[i] - kc[key]) ** 2)
                if curr_dis < min_dis:
                    if strong:
                        if abs(curr_dis - k_mean[key]) < 3 * k_std[key]:
                            min_dis_class = key
                            min_dis = curr_dis
                    else:
                        min_dis_class = key
                        min_dis = curr_dis
            area_class[i] = min_dis_class
    return area_class


def get_class_distr_param(flow, class_area, kc):
    means = []
    stds = []
    for class_index in range(0, len(class_area)):
        class_delta = np.sum(flow[class_area[class_index]] - kc[class_index], axis=1)
        means.append(np.mean(class_delta))
        stds.append(np.std(class_delta))
    return means, stds


def get_spatiol_distr_param(data, interval, class_area, k=20):
    """data should be a 2-dimensional matrix, the first dim means the time,
    the unit could be hour, day, or week, the second dim means area, which
    is expected to be limited in [0,  1024]
    """
    spatiol = [[[] for j in range(0, interval)] for i in range(0, k)]

    for i in range(0, interval):
        for cyc_i in np.arange(0, len(data), interval):
            for curr_class in class_area.keys():
                for area in class_area[curr_class]:
                    spatiol[curr_class][i].append(data[cyc_i + i, area])

    means = [[0] * interval for i in range(0, k)]
    stds = [[0] * interval for i in range(0, k)]

    for i in range(0, k):
        for j in range(0, interval):
            if len(spatiol[i][j]) == 0:
                continue
            means[i][j] = (np.mean(spatiol[i][j]))
            stds[i][j] = (np.std(spatiol[i][j], ddof=1))
    return means, stds

def add_click_js(path):
    with open(path, 'w') as pf:

        map_name =
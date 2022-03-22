from src.utils import *
from tqdm import trange
from src.BaseSVDD import *
import h5py
from sklearn.ensemble import IsolationForest


class Geo():
    def __init__(self):
        return None

    def norm_flow(self, flow=None, interval=1):
        index_list = range(0, len(flow[1]), interval)
        flow_list = []
        for i in trange(0, len(flow)):
            flow_list.append([np.sum(flow[i, j:j + interval]) for j in index_list])
        flow = np.array(flow_list)
        flow = norm_by_row(flow)
        return flow

    def save_area_info(self, interval=1):
        data = get_data("data/UnicomBJ_flows.h5")
        f = h5py.File("data/area.hdf5", 'a')
        cur_g = f.create_group("%d" % (interval))
        for i in [0, 1]:
            flow_pre = data[:, i, :, :]
            flow = flow_pre.reshape((len(flow_pre), -1)).T
            index_list = range(0, len(flow[1]), interval)
            flow_list = []
            for k in trange(0, len(flow)):
                flow_list.append([np.sum(flow[k, j:j + interval]) for j in index_list])
            flow = np.array(flow_list)
            # history max, history min, range
            cur_d = []
            for row in flow:
                mx = np.max(row)
                mn = np.min(row)
                cur_d.append([mx, mn, mx - mn])

            cur_g.create_dataset("%d" % i, data=cur_d)

        f.close()
        return None

    def kmeans_geo(self, K=20, interval=1, save=False):
        data = get_data("data/UnicomBJ_flows.h5")
        f = h5py.File("data/flow_interval.hdf5", 'a')
        class_area = []
        for i in [0, 1]:
            flow_pre = data[:, i, :, :]
            flow = flow_pre.reshape((len(flow_pre), -1)).T
            flow = self.norm_flow(flow)
            flow_kclass, flow_kcenters = aggregate_by_geo(flow, 'kmeans', k=K)
            means, stds = get_class_distr_param(flow, flow_kclass, flow_kcenters)
            area_classes = area_domain_class(flow_kclass)
            area_classes = refine_geo_agg(area_classes, flow, flow_kcenters, means, stds)
            cur_class_area = class_domain_area(area_classes)
            class_area.append(cur_class_area)
            if save:
                print("saving dataset %d%d" % (i, interval))
                cur_g = f.create_group("%d%d" % (i, interval))
                # 保存类别区域
                for key in cur_class_area.keys():
                    print("saving class %d" % (key))
                    cur_g.create_dataset("%d" % key, data=cur_class_area[key])
                # 保存数值数据
                # 最大值 最小值 平均值 中位值 内围上界 内围下界
                cur_d = []
                for areas in cur_class_area.values():
                    cmx = np.max(flow[areas, :])
                    cmn = np.min(flow[areas, :])
                    cavg = np.average(flow[areas, :])
                    cmid = np.median(flow[areas, :])
                    cq = np.percentile(flow[areas, :], [25, 75])
                    cup = cq[1] + (cq[1] - cq[0]) * 1.5
                    cbo = cq[0] - (cq[1] - cq[0]) * 1.5
                    cur_d.append([cmx, cmn, cavg, cmid, cup, cbo])
                cur_g["param"] = np.array(cur_d)
        f.close()
        return class_area

    def jaccard(p, q):
        c = [v for v in p if v in q]
        return float(len(c)) / (len(q) + len(p) - len(c))

    def agg_geo_class(self, K=20, interval=1, agg_alpha=0.15, save=False):
        class_area = self.kmeans_geo(K, interval)

        # 出入流聚类类别相似度计算
        simi = np.array([[0] * K for i in range(0, K)]).astype(float)
        for in_key in class_area[0].keys():
            for out_key in class_area[1].keys():
                simi[in_key][out_key] = (self.jaccard(class_area[0][in_key], class_area[1][out_key]))

        in2out = []

        # 从入流到出流聚类方向进行类别匹配
        for i in range(0, simi.shape[0]):
            for j in range(0, simi.shape[1]):
                mr, mc = np.unravel_index(np.argmax(simi), simi.shape)
                print("simi[%d, %d]: %f" % (mr, mc, simi[mr, mc]))
                if simi[mr, mc] >= agg_alpha:
                    in2out.append([mr, mc])
                    simi[mr, :] = -1
                    simi[:, mc] = -1
                break

        print("total class : ", len(in2out))

        agg_class_area = {}

        # 将匹配类别中相同的区域提取出用于生成初始类别中心点
        index = 0
        for i in in2out:
            # 类别重新命名为[0, len(in2out))
            agg_class_area[index] = [area for area in class_area[0][i[0]] if area in class_area[1][i[1]]]
            index += 1

        print(agg_class_area)

        data = get_data("data/UnicomBJ_flows.h5")
        # 生成初始类别中心点
        in_out_center = []  # 两个维度，第一个为出入流维度，第二个为类别维度
        # 该函数不会在线运行，所以为了代码的简洁性，这一循环会出现多次
        for in_out in [0, 1]:
            agg_kernel_center = []

            flow_pre = data[:, in_out, :, :]
            flow = flow_pre.reshape((len(flow_pre), -1)).T
            flow = self.norm_flow(flow)

            for cur_class in agg_class_area.values():
                cur_flow = flow[cur_class]
                agg_kernel_center.append(np.sum(cur_flow, axis=0) / len(cur_flow))

            in_out_center.append(agg_kernel_center)

        flows = []

        for i in [0, 1]:
            flow_pre = data[:, i, :, :]
            flow = flow_pre.reshape((len(flow_pre), -1)).T
            flow = self.norm_flow(flow)
            flows.append(flow)

        # 计算每个点到类别的出入流合并距离
        # 获取每个区域最终类别
        area_class = []

        for i in range(0, 1024):
            dis = []
            for j in range(0, len(in2out)):
                dis.append(np.sum((flows[0][i] - in_out_center[0][j]) ** 2) + \
                           np.sum((flows[1][i] - in_out_center[1][j]) ** 2))
            area_class.append(np.argmin(dis))
        class_area = class_domain_area(area_class)

        if save:
            f = h5py.File("data/agg_interval.hdf5", 'a')
            cur_g = f.create_group("%d" % (interval))
            for key in class_area.keys():
                print("saving class %d" % (key))
                cur_g.create_dataset("%d" % key, data=class_area[key])
            f.close()
        return class_area

    def get_geo_ad(self, inflow=None, outflow=None, K=20, interval=1, method='svdd'):
        # 读取每个区域的历史数据用于数据预处理
        inflow = np.array(inflow).astype(float)
        outflow = np.array(outflow).astype(float)

        area_fp = h5py.File("data/area.hdf5", "r")["%s" % interval]
        inflow_his = np.array(area_fp["0"]).astype(float)
        outflow_his = np.array(area_fp["1"]).astype(float)
        for i in range(0, 1024):
            inflow[i] = (inflow[i] - inflow_his[i][0]) / inflow_his[i][2]
            outflow[i] = (outflow[i] - outflow_his[i][0]) / outflow_his[i][2]

        anomaly_score = np.zeros(shape=(1024, 1), dtype=float)

        def get_agg_class_areas(interval):
            # 将实时输入流、输出流作为二维数据进行异常值检测
            agg_class_fp = h5py.File("data/agg_interval.hdf5", "r")["%s" % interval]
            agg_class_areas = []
            for key in agg_class_fp.keys():
                agg_class_areas.append(agg_class_fp[key])
            return agg_class_areas

        if method == 'svdd':
            # 将实时输入流、输出流作为二维数据进行异常值检测
            agg_class_areas = get_agg_class_areas(interval)
            flow = np.array([inflow, outflow]).T[0]

            svdd = BaseSVDD(C=0.8, gamma=0.3, kernel='rbf', display='off')
            for c in agg_class_areas:
                x = flow[c, :]
                svdd.C = 0.8
                svdd.fit(x)
                res = svdd.get_distance(x) - svdd.radius
                anomaly_score[c] = res
            cur_ = [0 if i < 0 else i for i in anomaly_score]
            anomaly_score = (anomaly_score-np.min(anomaly_score))/(np.max(anomaly_score)-np.min(anomaly_score))
            return anomaly_score
        elif method == 'ifroest':
            agg_class_areas = get_agg_class_areas(interval)
            flow = np.array([inflow, outflow]).T[0]

            clf = IsolationForest(contamination=0.02, max_features=2)
            for c in agg_class_areas:
                x = flow[c, :]
                clf.fit(x)
                res = clf.score_samples(x)
                anomaly_score[c] = res.reshape(res.shape[0], 1)
            anomaly_score = (anomaly_score-np.min(anomaly_score))/(np.max(anomaly_score)-np.min(anomaly_score))
            anomaly_score = 1 - anomaly_score
            return anomaly_score

        return None

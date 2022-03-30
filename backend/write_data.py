import pymysql
from src.geo import *
from src.temp import *
from src.utils import *
import numpy as np
import pandas as pd
from datetime import *
from tqdm import *
import matplotlib.pyplot as plt

host = 'localhost'
port = 3306
user = 'root'
pwd = '2479694366'
db = 'ad'


def gen_inflow_sql(inflow, k):
    sql = "insert into inflow(area, "

    for i in range(0, 2184):
        sql += "time_%d, " % i
    sql = sql[:-2]

    sql += ") values (%d, " % k
    for i in range(0, 2184):
       sql += "%d, " % inflow[k, i]
    sql = sql[:-2]
    sql += ")"

    return sql


def gen_outflow_sql(outflow, k):
    sql = "insert into outflow(area, "

    for i in range(0, 2184):
        sql += "time_%d, " % i
    sql = sql[:-2]

    sql += ") values (%d, " % k
    for i in range(0, 2184):
       sql += "%d, " % outflow[k, i]
    sql = sql[:-2]
    sql += ")"

    return sql


if __name__ == '__main__':
    # connect database
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    origin_data = get_data()

    # ordered by area
    inflow = origin_data[:, 0, :, :].reshape(len(origin_data), -1).T
    outflow = origin_data[:, 1, :, :].reshape(len(origin_data), -1).T

    # temp_d = Temp()
    # geo_d = Geo()

    # # insert data into inflow table
    # for k in range(0, 1024):
    #     sql = gen_inflow_sql(inflow, k)
    #     print(sql)
    #     cursor.execute(sql)

    # # insert data into outflow table
    # for k in range(0, 1024):
    #     sql = gen_outflow_sql(outflow, k)
    #     print(k, ": ", sql)
    #     cursor.execute(sql)

    # insert data into flow_rank table
    # flow = (inflow + outflow).T
    # print(flow.shape)
    #
    # for i in range(0, 2184):
    #     max_flow_num = []
    #     max_flow_arg = []
    #     for j in range(0, 7):
    #         num = np.max(flow[i, :])
    #         max_flow_num.append(num)
    #         arg = np.argmax(flow[i, :])
    #         max_flow_arg.append(arg)
    #         flow[i, arg] = 0
    #     sql = "insert into flow_rank("
    #
    #     for j in range(0, 7):
    #         sql += "area_%d, " % j
    #     for j in range(0, 7):
    #         sql += "flow_%d, " % j
    #     sql = sql[:-2] + ") values ("
    #
    #     for j in range(0, 7):
    #         sql += "%d, " % max_flow_arg[j]
    #     for j in range(0, 7):
    #         sql += "%d, " % max_flow_num[j]
    #
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # insert into table predict_inflow and predict_outflow
    # inflow_pred = [[0]*2184] * 1024
    # outflow_pred = [[0] * 2184] * 1024
    # st = datetime(2017, 9, 1, 0)

    # print("predicting:......")
    # for i in trange(24, 2184):
    #     cur_time = st + timedelta(hours=i)
    #     cur = temp_d.predict(cur_time)
    #     for j in range(0, 1024):
    #         inflow_pred[j][i] = cur[j, 0]
    #         outflow_pred[j][i] = cur[j, 1]
    #
    # np_pred_inflow = np.array(inflow_pred)
    # np.save("inflow_pred.npy", np_pred_inflow)
    #
    # np_pred_outflow = np.array(outflow_pred)
    # np.save("outflow_pred.npy", np_pred_outflow)

    # np_pred_inflow = np.load("inflow_pred.npy")
    # np_pred_outflow = np.load("outflow_pred.npy")
    #
    # print("insert into predict_inflow:......")
    # for i in trange(0, 1024):
    #     sql = "insert into predict_inflow(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     for j in range(0, 2184):
    #         sql += "%d, " % np_pred_inflow[i, j]
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)
    #
    # print("insert into predict_outflow:......")
    # for i in trange(0, 1024):
    #     sql = "insert into predict_outflow(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     for j in range(0, 2184):
    #         sql += "%d, " % np_pred_outflow[i, j]
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # cursor.execute("select * from predict_inflow")
    # pred_inflow_dict = cursor.fetchall()
    # print("insert into inflow_incre:......")
    # for i in trange(0, 1024):
    #     sql = "insert into inflow_incre(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     cur_preds = list(pred_inflow_dict[i].values())
    #
    #     for j in range(0, 2184):
    #         sql += "%d, " % (0 if j < 24 else (cur_preds[j] - inflow[i, j]))
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # cursor.execute("select * from predict_outflow")
    # pred_outflow_dict = cursor.fetchall()
    # print("insert into outflow_incre:......")
    # for i in trange(0, 1024):
    #     sql = "insert into outflow_incre(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     cur_preds = list(pred_outflow_dict[i].values())
    #
    #     for j in range(0, 2184):
    #         sql += "%d, " % (0 if j < 24 else (cur_preds[j] - outflow[i, j]))
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # cursor.execute("select * from inflow_incre where area=0")
    # values = list(cursor.fetchone().values())[1:]
    #
    # cursor.execute("select * from predict_inflow where area=0")
    # values1 = list(cursor.fetchone().values())[1:]
    #
    # plt.plot(range(0, 100), np.log(values[:100]), c='b')
    # plt.plot(range(0, 100), np.log(values1[:100]), c='y')
    # plt.plot(range(0, 100), np.log(inflow[0, :100]), c='r')
    #
    # plt.show()

    # cursor.execute("select * from inflow_incre")
    # inflow_incre_dict = cursor.fetchall()
    #
    # cursor.execute("select * from outflow_incre")
    # outflow_incre_dict = cursor.fetchall()
    #
    # incres = []
    # for i in range(0, 1024):
    #     cur_inflow_incre = list(inflow_incre_dict[i].values())
    #     cur_outflow_incre = list(outflow_incre_dict[i].values())
    #     cur_incre = cur_inflow_incre + cur_outflow_incre
    #     incres.append(cur_incre)
    #
    # incres_np = np.array(incres).T
    #
    # incre_rank = []
    # for i in trange(0, 2184):
    #     incre_max_num = []
    #     incre_max_arg = []
    #     for j in range(0, 7):
    #         num = np.max(incres_np[i, :])
    #         incre_max_num.append(num)
    #         arg = np.argmax(incres_np[i, :])
    #         incre_max_arg.append(arg)
    #         incres_np[i, arg] = 0
    #     sql = "insert into incre_rank("
    #
    #     for j in range(0, 7):
    #         sql += "area_%d, " % j
    #     for j in range(0, 7):
    #         sql += "incre_%d, " % j
    #     sql = sql[:-2] + ") values ("
    #
    #     for j in range(0, 7):
    #         sql += "%d, " % incre_max_arg[j]
    #     for j in range(0, 7):
    #         sql += "%f, " % incre_max_num[j]
    #
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # temp_d = Temp()
    # geo_d = Geo()

    # st = datetime(2017, 9, 1, 0)
    # ad_temps = [[0]*1024] * 2184
    # for i in trange(24, 2184):
    #     cur_time = st + timedelta(hours=i)
    #     cur_inflow = inflow[:, i].reshape(1024, 1)
    #     cur_outflow = outflow[:, i].reshape(1024, 1)
    #     cur = temp_d.get_temp_ad(cur_inflow, cur_outflow, cur_time)
    #     ad_temp = []
    #     for j in range(0, 1024):
    #         ad_temp.append(math.sqrt(cur[j][0]**2 + cur[j][1]**2))
    #     ad_temps[i] = ad_temp

    # temps = np.array(ad_temps, dtype=float).T
    # np.save("ad_temp.npy", temps)
    # temps = np.load("ad_temp.npy")
    #
    # for i in trange(0, 1024):
    #     sql = "insert into ad_temporal(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     for j in range(0, 2184):
    #         sql += "%f, " % temps[i, j]
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)
    # ad_geos = [[0] * 1024] * 2184
    # for i in trange(0, 2184):
    #     cur_inflow = inflow[:, i].reshape(1024, 1)
    #     cur_outflow = outflow[:, i].reshape(1024, 1)
    #     cur = geo_d.get_geo_ad(cur_inflow, cur_outflow, method='iforest')
    #     ad_geos[i] = cur.tolist()
    #
    # geos = np.array(ad_geos, dtype=float).T
    # np.save("ad_geo.npy", geos)

    # geos = np.load("ad_geo.npy")[0]
    #
    # for i in trange(0, 1024):
    #     sql = "insert into ad_spatial(area, "
    #     for j in range(0, 2184):
    #         sql += "time_%d, " % j
    #
    #     sql = sql[:-2] + ") values (%d, " % i
    #
    #     for j in range(0, 2184):
    #         sql += "%f, " % geos[i, j]
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # cursor.execute("select * from ad_spatial")
    # ad_spatial_dict = cursor.fetchall()
    #
    # cursor.execute("select * from ad_temporal")
    # ad_temporal_dict = cursor.fetchall()
    #
    # ads = []
    # for i in range(0, 1024):
    #     ad = []
    #     cur_ad_spatial = list(ad_spatial_dict[i].values())
    #     cur_ad_temporal = list(ad_temporal_dict[i].values())
    #     for j in range(0, 2184):
    #         cur_ad = math.sqrt(cur_ad_spatial[j]**2 + cur_ad_temporal[j]**2)
    #         ad.append(cur_ad)
    #     ads.append(ad)
    #
    # ads_np = np.array(ads).T
    #
    # ad_rank = []
    # for i in trange(0, 2184):
    #     ad_max_num = []
    #     ad_max_arg = []
    #     for j in range(0, 7):
    #         num = np.max(ads_np[i, :])
    #         ad_max_num.append(num)
    #         arg = np.argmax(ads_np[i, :])
    #         ad_max_arg.append(arg)
    #         ads_np[i, arg] = -1
    #     sql = "insert into ad_rank("
    #
    #     for j in range(0, 7):
    #         sql += "area_%d, " % j
    #     for j in range(0, 7):
    #         sql += "ad_%d, " % j
    #     sql = sql[:-2] + ") values ("
    #
    #     for j in range(0, 7):
    #         sql += "%d, " % ad_max_arg[j]
    #     for j in range(0, 7):
    #         sql += "%f, " % ad_max_num[j]
    #
    #     sql = sql[:-2] + ")"
    #     print(i, ": ", sql)
    #     cursor.execute(sql)

    # ad spatial or temporal rank
    cursor.execute("select * from ad_temporal")
    ad_temporal_dict = cursor.fetchall()

    ads = []
    for i in range(0, 1024):
        ad = []
        cur_ad_temporal = list(ad_temporal_dict[i].values())
        for j in range(0, 2184):
            cur_ad = cur_ad_temporal[j]
            ad.append(cur_ad)
        ads.append(ad)

    ads_np = np.array(ads).T

    ad_rank = []
    for i in trange(0, 2184):
        ad_max_num = []
        ad_max_arg = []
        for j in range(0, 7):
            num = np.max(ads_np[i, :])
            ad_max_num.append(num)
            arg = np.argmax(ads_np[i, :])
            ad_max_arg.append(arg)
            ads_np[i, arg] = -1
        sql = "insert into ad_temporal_rank("

        for j in range(0, 7):
            sql += "area_%d, " % j
        for j in range(0, 7):
            sql += "ad_%d, " % j
        sql = sql[:-2] + ") values ("

        for j in range(0, 7):
            sql += "%d, " % ad_max_arg[j]
        for j in range(0, 7):
            sql += "%f, " % ad_max_num[j]

        sql = sql[:-2] + ")"
        print(i, ": ", sql)
        cursor.execute(sql)

    # def sql_gen(td, tn, ai):
    #     sql = "select "
    #     for i in range(6, -1, -1):
    #         sql += ("time_%d, " % (td-i))
    #     return sql[:-2] + " from " + tn + " where area=" + str(ai)
    #
    # sql = sql_gen(32, "inflow", 1)
    # print(sql)
    # cursor.execute(sql)
    # res = cursor.fetchone()
    # print([i['time_0'] for i in res])
    # print(list(res.values()))

    cursor.close()
    conn.close()

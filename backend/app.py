import folium
from flask import *
from flask import request
import pymysql
from datetime import *
import math
import numpy as np

host = 'localhost'
port = 3306
user = 'root'
pwd = '2479694366'
db = 'ad'

sub_time_days = -1600

app = Flask(__name__)
app.secret_key = 'secret!'

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

@app.route('/meun', methods=['GET', 'POST'])
def meun_changed():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    param = request.get_json(silent=True)
    meunIndex = param['meunIndex']
    now_time = datetime.now() + timedelta(days=sub_time_days)
    
    # 数据库id自增默认从1开始
    db_names = ['flow_rank', 'incre_rank', 'ad_rank']
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600) + 1

    sql = "select * from " + db_names[meunIndex] + " where id=" + str(td)
    cursor.execute(sql)

    rank = list(cursor.fetchone().values())
    res = {}
    for i in range(0, 7):
        res['%d' % rank[1 + i]] = rank[8 + i]

    cursor.close()
    conn.close()

    return res

@app.route('/map', methods=['GET', 'POST'])
def map_changed():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    param = request.get_json(silent=True)
    meunIndex = param['meunIndex']
    now_time = datetime.now() + timedelta(days=sub_time_days)

    db_names = ['inflow', 'outflow', 'inflow_incre', 'outflow_incre', 'ad_spatial', 'ad_temporal']
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)

    if meunIndex == 0:
        sql = "select time_" + str(td) + " from " + db_names[0]
        cursor.execute(sql)
        inflow = [i["time_%d" % td] for i in cursor.fetchall()]

        sql = "select time_" + str(td) + " from " + db_names[1]
        cursor.execute(sql)
        outflow = [i["time_%d" % td] for i in cursor.fetchall()]

        res = [inflow[i] - outflow[i] for i in range(0, len(inflow))]
    elif meunIndex == 1:
        sql = "select time_" + str(td) + " from " + db_names[2]
        cursor.execute(sql)
        inflow_incre = [i["time_%d" % td] for i in cursor.fetchall()]

        sql = "select time_" + str(td) + " from " + db_names[3]
        cursor.execute(sql)
        outflow_incre = [i["time_%d" % td] for i in cursor.fetchall()]

        res = [inflow_incre[i] - outflow_incre[i] for i in range(0, len(inflow_incre))]

    else:
        sql = "select time_" + str(td) + " from " + db_names[4]
        cursor.execute(sql)
        ad_spatial = [i["time_%d" % td] for i in cursor.fetchall()]

        sql = "select time_" + str(td) + " from " + db_names[5]
        cursor.execute(sql)
        ad_temporal = [i["time_%d" % td] for i in cursor.fetchall()]

        res = [math.sqrt(ad_spatial[i]**2 + ad_temporal[i]**2) for i in range(0, len(ad_spatial))]
    cursor.close()
    conn.close()

    percent = np.percentile(res, [0, 17, 34, 51, 68, 85, 100])

    ret = {}

    for i in range(0, len(res)):
        for j in range(1, 7):
            if res[i] < percent[j]:
                ret[i] = j - 1
                break
    
    return ret

@app.route('/right1', methods=['GET', 'POST'])
def right1_changed():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    param = request.get_json(silent=True)
    areaIndex = param['areaIndex']
    meunIndex = param['meunIndex']

    now_time = datetime.now() + timedelta(days=sub_time_days)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)

    xData = [str((now_time.hour + i)%24) + ":00" for i in range(0, 25)]
    
    res = {}

    def sql_gen(td, tn, ai):
        sql = "select "
        for i in range(24, -1, -1):
            sql += ("time_%d, " % (td-i))
        return sql[:-2] + " from " + tn + " where area=" + str(ai)

    if meunIndex == 0:
        sql = sql_gen(td, "inflow", areaIndex)
        cursor.execute(sql)
        inflow_list = list(cursor.fetchone().values())

        sql = sql_gen(td, "outflow", areaIndex)
        cursor.execute(sql)
        outflow_list = list(cursor.fetchone().values())
        
        res = {'inflow': inflow_list, 'outflow': outflow_list}
    elif meunIndex == 1:
        sql = sql_gen(td, "predict_inflow", areaIndex)
        cursor.execute(sql)
        pred_list = list(cursor.fetchone().values())

        sql = sql_gen(td, "inflow", areaIndex)
        cursor.execute(sql)
        real_list = list(cursor.fetchone().values())
        
        res = {'pred': pred_list, 'real': real_list}
    else:
        sql = sql_gen(td, "ad_spatial", areaIndex)
        cursor.execute(sql)
        ad_spatial_list = list(cursor.fetchone().values())

        sql = sql_gen(td, "ad_temporal", areaIndex)
        cursor.execute(sql)
        ad_temporal_list = list(cursor.fetchone().values())
        
        ads = [math.sqrt(ad_spatial_list[i]**2 + ad_temporal_list[i]**2) for i in range(0, len(ad_spatial_list))]
        res = {"ads": ads}

    res['xData'] = xData

    cursor.close()
    conn.close()

    return res

@app.route('/right2', methods=['GET', 'POST'])
def right2_changed():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    param = request.get_json(silent=True)
    areaIndex = param['areaIndex']
    meunIndex = param['meunIndex']

    now_time = datetime.now() + timedelta(days=sub_time_days)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)
    xData = [str((now_time.hour + i)%24) + ":00" for i in range(1, 5)]
    res = {}

    if meunIndex == 0:
        sql = ("select time_%d" % td) + (" from inflow where area=%d" % areaIndex)
        cursor.execute(sql)
        res['inflow'] = list(cursor.fetchone().values())[0]
        
        sql = ("select time_%d" % td) + (" from outflow where area=%d" % areaIndex)
        cursor.execute(sql)
        res['outflow'] = list(cursor.fetchone().values())[0]
    elif meunIndex == 1:

        def sql_gen(td, tn, ai):
            sql = "select "
            for i in range(1, 5):
                sql += ("time_%d, " % (td+i))
            return sql[:-2] + " from " + tn + " where area=" + str(ai)

        sql = sql_gen(td, "inflow", areaIndex)
        cursor.execute(sql)
        res['pred_inflow'] = list(cursor.fetchone().values())
        
        sql = sql_gen(td, "outflow", areaIndex)
        cursor.execute(sql)
        res['pred_outflow'] = list(cursor.fetchone().values())

        res['xData'] = xData
    else:
        sql = "select * from ad_spatial_rank" + " where id=" + str(td + 1)
        cursor.execute(sql)

        rank = list(cursor.fetchone().values())
        for i in range(0, 7):
            res['%d' % rank[1 + i]] = rank[8 + i]
    cursor.close()
    conn.close()

    return res

@app.route('/right3', methods=['GET', 'POST'])
def right3_changed():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    param = request.get_json(silent=True)
    areaIndex = param['areaIndex']
    meunIndex = param['meunIndex']

    now_time = datetime.now() + timedelta(days=sub_time_days)
    td = int((now_time - datetime(2017, 9, 1, 0)).total_seconds() // 3600)
    xData = [str((now_time.hour + i)%24) + ":00" for i in range(1, 5)]
    nearAreaIncres = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]
    db_names = ["inflow", "outflow"]
    xNames = ["本域", "上邻域", "下邻域", "左邻域", "右邻域"]
    res = {}

    if meunIndex == 0:
        sql = ("select time_%d from " % td)
        flows = [[], []]
        xnames = []
        for i in range(0, 2):
            cur_s = sql + "%s where area=" % db_names[i]
            for j in range(0, len(nearAreaIncres)):
                cur_s = sql + "%s where area=" % db_names[i]
            for j in range(0, len(nearAreaIncres)):
                if (areaIndex < 32 and j == 1) or \
                    (areaIndex > 991 and j == 2) or \
                    (areaIndex%32 == 0 and j == 3) or\
                    (areaIndex%31 == 0 and areaIndex > 0 and j == 4):
                    continue

                cur_sql = cur_s + "%d" % (areaIndex + nearAreaIncres[j][0]*32 + nearAreaIncres[j][1])
                cursor.execute(cur_sql)
                flows[i].append(list(cursor.fetchone().values())[0])
                if i == 0:
                    xnames.append(xNames[j])

        res['inflow'] = flows[0]
        res['outflow'] = flows[1]
        res['xData'] = xnames
    elif meunIndex == 1:
        sql = ("select time_%d from " % (td + 1))
        flows = [[], []]
        xnames = []
        for i in range(0, 2):
            cur_s = sql + "%s where area=" % db_names[i]
            for j in range(0, len(nearAreaIncres)):
                if (areaIndex < 32 and j == 1) or \
                    (areaIndex > 991 and j == 2) or \
                    (areaIndex%32 == 0 and j == 3) or\
                    (areaIndex%31 == 0 and j == 4):
                    continue
                cur_sql = cur_s + "%d" % (areaIndex + nearAreaIncres[j][0]*32 + nearAreaIncres[j][1])
                cursor.execute(cur_sql)
                flows[i].append(list(cursor.fetchone().values())[0])
                if i == 0:
                    xnames.append(xNames[j])

        res['inflow'] = flows[0]
        res['outflow'] = flows[1]
        res['xData'] = xnames
    else:
        sql = "select * from ad_temporal_rank" + " where id=" + str(td + 1)
        cursor.execute(sql)

        rank = list(cursor.fetchone().values())
        for i in range(0, 7):
            res['%d' % rank[1 + i]] = rank[8 + i]

    cursor.close()
    conn.close()

    return res

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
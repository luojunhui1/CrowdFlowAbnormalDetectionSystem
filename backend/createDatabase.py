import pymysql
host = 'localhost'
port = 3306
user = 'root'
pwd = '2479694366'
db = 'ad'


'''
create inflow
'''
def create_inflow_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table inflow
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()


'''
create outflow
'''
def create_outflow_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table outflow
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

def create_predict_inflow_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table predict_inflow
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()


'''
create outflow
'''
def create_predict_outflow_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table predict_outflow
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()


'''
create rank flow rank
'''
def create_flow_rank_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table flow_rank
        (
            id int auto_increment primary key,
    """
    for i in range(0, 7):
        sql += 'area_%d int,' % i

    for i in range(0, 7):
        sql += 'flow_%d int,' % i

    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

'''
create inflow
'''
def create_inflow_incre_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table inflow_incre
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()


'''
create inflow
'''
def create_outflow_incre_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table outflow_incre
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d int,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()


'''
create outflow
'''
def create_incre_rank_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
            create table incre_rank
            (
                id int auto_increment primary key,
        """
    for i in range(0, 7):
        sql += 'area_%d int,' % i
    for i in range(0, 7):
        sql += 'incre_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

'''
create inflow
'''
def create_ad_temporal_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table ad_temporal
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

def create_ad_spatial_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table ad_spatial
        (
            area int primary key,
    """
    for i in range(0, 2184):
        sql += 'time_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

def create_ad_rank_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table ad_rank
        (
            id int auto_increment primary key,
    """
    for i in range(0, 7):
        sql += 'area_%d int,' % i
    for i in range(0, 7):
        sql += 'ad_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

def create_ad_spatial_rank_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table ad_spatial_rank
        (
            id int auto_increment primary key,
    """
    for i in range(0, 7):
        sql += 'area_%d int,' % i
    for i in range(0, 7):
        sql += 'ad_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

def create_ad_temporal_rank_database():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=pwd)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        create table ad_temporal_rank
        (
            id int auto_increment primary key,
    """
    for i in range(0, 7):
        sql += 'area_%d int,' % i
    for i in range(0, 7):
        sql += 'ad_%d float,' % i
    sql = sql[:-1]
    sql += ')engine=MYISAM;'
    # print(sql)
    cursor.execute(sql)

    cursor.close()
    conn.close()

# create_inflow_database()
# create_outflow_database()
# create_flow_rank_database()
#
# create_predict_inflow_database()
# create_predict_outflow_database()
# create_inflow_incre_database()
# create_outflow_incre_database()
# create_incre_rank_database()

# create_ad_temporal_database()
# create_ad_spatial_database()
# create_ad_rank_database()

# create_ad_spatial_rank_database()
create_ad_temporal_rank_database()

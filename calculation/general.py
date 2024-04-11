import traceback
from decimal import Decimal

from sqlalchemy import Table, MetaData

from extensions import db
from models.crossings import Crossings
from models.gateways import Gateways
from models.sensors import Sensors


GATEWAY_RADIUS = 0.0006226


def getData(name):
    metadata = MetaData()
    try:
        if name == 'default':
            result = db.session.query(Sensors).all()
            sensors = [li.asdict() for li in result]
            result = db.session.query(Gateways).all()
            gateways = [li.asdict() for li in result]
            result = db.session.query(Crossings).all()
            crossings = [li.asdict() for li in result]
        else:
            # 查询传感器
            sensor_table = Table(name + "_sensors", metadata, autoload_with=db.engine)
            result = db.session.query(sensor_table).all()
            sensors = []
            for row in result:
                data = {column.name: getattr(row, column.name) for column in sensor_table.columns}
                sensors.append(data)

            # 查询网关
            gateway_table = Table(name + "_gateways", metadata, autoload_with=db.engine)
            result = db.session.query(gateway_table).all()
            gateways = []
            for row in result:
                data = {column.name: getattr(row, column.name) for column in gateway_table.columns}
                gateways.append(data)

            # 查询路口
            crossing_table = Table(name + "_crossings", metadata, autoload_with=db.engine)
            result = db.session.query(crossing_table).all()
            crossings = []
            for row in result:
                data = {column.name: getattr(row, column.name) for column in crossing_table.columns}
                crossings.append(data)
        # print(sensors)
        return {
            'sensors': sensors,
            'gateways': gateways,
            'crossings': crossings,
        }

    except Exception:
        traceback.print_exc()
        return 444
    finally:
        db.session.close()


# 计算点距离
def calc_distance(x1, y1, x2, y2):
    b_x1 = Decimal(str(x1))
    b_x2 = Decimal(str(x2))
    b_y1 = Decimal(str(y1))
    b_y2 = Decimal(str(y2))

    # 勾股定理
    distance = ((b_x1 - b_x2) ** 2 + (b_y1 - b_y2) ** 2).sqrt()
    return float(distance)


# 计算每个网关覆盖的所有Sensor
def calc_covered(sensor, gateway):
    cover = []
    be_covered_set = set()
    for i, g in enumerate(gateway):
        g_cover = []
        for j, s in enumerate(sensor):
            dis = calc_distance(g[1][0], g[1][1], s[1][0], s[1][1])
            if dis < GATEWAY_RADIUS:
                g_cover.append((j, s[0], s[1]))
                be_covered_set.add(s[0])
        cover.append((g[0], g[1], g_cover))
    return cover, be_covered_set


#   生成用于Matlab计算的矩阵
def create_matrix(d):
    all_set = set()
    s = []
    for index, item in enumerate(d['sensors']):
        s.append(((item['group'], item['group_number']), (item['lng'], item['lat'])))
        all_set.add(s[index][0])
    g = []
    for item in d['gateways']:
        g.append(((item['group'], item['group_number']), (item['lng'], item['lat'])))
    # print(s)
    cover, be_covered_set = calc_covered(s, g)
    if len(all_set) != len(be_covered_set):
        return 444, '传感器没有被全部覆盖到！'

#     如果全部覆盖
    matrix = [[0 for _ in range(len(g))] for _ in range(len(s))]
    for i, c in enumerate(cover):
        for it in c[2]:
            matrix[it[0]][i] = 1

    # for row in matrix:
    #     print(' '.join(map(str, row)))
    return 0, matrix,


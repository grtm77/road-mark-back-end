import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import Table, MetaData

from extensions import db
from models.crossings import Crossings
from models.datasets import Datasets
from models.gateways import Gateways
from models.sensors import Sensors
from utils.status_code import *

read_data_bp = Blueprint('read_data', __name__)


@read_data_bp.route('/loadDatasets', methods=["GET"])
def load_datasets_list():
    try:
        lists = db.session.query(Datasets).all()
        lists = [li.asdict() for li in lists]
        return jsonify({
            'success': True,
            'code': HTTP_SUCCESS,
            'msg': '查询成功！',
            'data': lists,
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '数据库错误！',
            'data': None,
        })
    finally:
        db.session.close()


@read_data_bp.route('/loadData', methods=["GET"])
def load_data():
    metadata = MetaData()
    name = request.args.get('table_name')
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
        return jsonify({
            'success': True,
            'code': HTTP_SUCCESS,
            'msg': '查询成功！',
            'data': {
                'sensors': sensors,
                'gateways': gateways,
                'crossings': crossings,
            },
        })

    except Exception:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '数据库错误！',
            'data': None,
        })
    finally:
        db.session.close()

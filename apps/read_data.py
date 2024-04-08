import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text

from extensions import db
from models.crossings import Crossings
from models.gateways import Gateways
from models.sensors import Sensors
from utils.status_code import *

read_data_bp = Blueprint('read_data', __name__)


@read_data_bp.route('/loadDatasets', methods=["GET"])
def add_marks():
    # 整理前端数据
    sensors = request.get_json()['sensors']
    gateways = request.get_json()['gateways']
    crossings = request.get_json()['crossings']

    # 先截断表
    db.session.execute(text('TRUNCATE TABLE sensors'))
    db.session.execute(text('TRUNCATE TABLE gateways'))
    db.session.execute(text('TRUNCATE TABLE crossings'))

    try:
        # 传感器存入
        for index, group in enumerate(sensors):
            for i, s in enumerate(group):
                db.session.add(Sensors(lng=s['lng'], lat=s['lat'], group=index + 1, group_number=i + 1))
        # 网关存入
        for index, group in enumerate(gateways):
            for i, s in enumerate(group):
                db.session.add(Gateways(lng=s['lng'], lat=s['lat'], group=index + 1, group_number=i + 1))
        # 路口存入
        for c in crossings:
            db.session.add(Crossings(lng=c['lng'], lat=c['lat']))

        # 提交事务
        db.session.commit()
        return jsonify({
            'success': True,
            'code': HTTP_SUCCESS,
            'msg': '保存成功！',
            'data': None,
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


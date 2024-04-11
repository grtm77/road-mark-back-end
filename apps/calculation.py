import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text, Table, Column, Integer, String, inspect

from calculation.calc_by_matlab import calc_lin_prog
from calculation.general import getData, create_matrix
from extensions import db
from models.crossings import Crossings
from models.datasets import Datasets
from models.gateways import Gateways
from models.sensors import Sensors
from utils.status_code import *

calc_bp = Blueprint('calculation', __name__)


@calc_bp.route('/calc', methods=['GET'])
def calc():
    name = request.args.get('table_name')
    try:
        algorithm = int(request.args.get('algorithm'))
    except Exception:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您选择了不合法的算法！',
            'data': None,
        })
    if not db.session.query(Datasets).filter_by(table_name=name).first():
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您发送了不合法的表名！',
            'data': None,
        })
    if algorithm == 0:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您还未选择算法！',
            'data': None,
        })
    data = getData(name)
    status, matrix = create_matrix(data)
    if status != 0:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': matrix,
            'data': None,
        })

    # 如果数据合法，则计算
    rs_list = calc_lin_prog(matrix)
    rt_g = []
    for i, g in enumerate(rs_list):
        if g[0] == 1:
            rt_g.append({'lng': data['gateways'][i]['lng'], 'lat': data['gateways'][i]['lat']})

    return jsonify({
        'success': True,
        'code': HTTP_SUCCESS,
        'msg': '计算成功！',
        'data': {
            'sensors': data['sensors'],
            'gateways': rt_g
        },
    })



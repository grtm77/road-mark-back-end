import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text, Table, Column, Integer, String, inspect

from calculation.calc_by_matlab import calc_lin_prog, calc_ran_greedy, calc_bba, calc_ga
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
    rt_g = []
    # 线性规划算法的返回数据结构和其他不同，单独处理
    if algorithm == 3:
        rs_list = calc_lin_prog(matrix)
        for i, g in enumerate(rs_list):
            if g[0] == 1:
                rt_g.append({'lng': data['gateways'][i]['lng'], 'lat': data['gateways'][i]['lat']})
        print(rs_list)
        return jsonify({
            'success': True,
            'code': HTTP_SUCCESS,
            'msg': '计算成功！',
            'data': {
                'sensors': data['sensors'],
                'gateways': rt_g
            },
        })
    # 朴素贪心
    elif algorithm == 1:
        rs_list = calc_ran_greedy(matrix)
    # 遗传
    elif algorithm == 5:
        rs_list = calc_ga(matrix)
    # 分支定界
    elif algorithm == 6:
        rs_list = calc_bba(matrix)
    print(rs_list)
    for i, g in enumerate(rs_list[0]):
        if g == 1:
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



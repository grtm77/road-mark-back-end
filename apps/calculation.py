import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text, Table, Column, Integer, String, inspect

from extensions import db
from models.crossings import Crossings
from models.datasets import Datasets
from models.gateways import Gateways
from models.sensors import Sensors
from utils.status_code import *

calc_bp = Blueprint('calculation', __name__)


@calc_bp.route('/calc', method=['GET'])
def calc():
    name = request.args.get('name')
    algorithm = request.args.get('algorithm')
    if not db.session.query(Datasets).filter_by(table_name=name).first():
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您发送了不合法的数据！',
            'data': None,
        })
    if algorithm == 0:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您还未选择算法！',
            'data': None,
        })
    elif algorithm == 1:
        pass
    else:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_REC_DATA,
            'msg': '您发送了不合法的数据！',
            'data': None,
        })

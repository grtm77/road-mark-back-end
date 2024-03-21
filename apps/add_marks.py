from flask import Blueprint, jsonify
from sqlalchemy import text

from extensions import db
from models.sensors import Sensors
from utils.status_code import *


add_marks_bp = Blueprint('add_marks', __name__)


@add_marks_bp.route('/')
def hello():
    return "这是道路停车节点覆盖计算系统的后端接口！请访问具体接口获取具体功能！"


@add_marks_bp.route('/addMarks', methods=["POST", "GET"])
def add_marks():
    # 传感器存入
    db.session.execute(text('TRUNCATE TABLE sensors'))
    db.session.add(Sensors)
    # 提交事务
    db.session.commit()
    if rst:
        return jsonify({
            'success': True,
            'code': HTTP_SUCCESS,
            'msg': '查询成功！',
            'data': rst[0].asdict(),
        })
    return jsonify({
        'success': False,
        'code': HTTP_ERROR_OPERATION,
        'msg': '未查询到数据！',
        'data': None,
    })





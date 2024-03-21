import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy import text

from extensions import db
from models.crossings import Crossings
from models.gateways import Gateways
from models.sensors import Sensors
from utils.status_code import *

add_marks_bp = Blueprint('add_marks', __name__)


@add_marks_bp.route('/')
def hello():
    return "这是道路停车节点覆盖计算系统的后端接口！请访问具体接口获取具体功能！"


@add_marks_bp.route('/addMarks', methods=["POST"])
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


@add_marks_bp.route('/saveDS', methods=['POST'])
def save_as_datasets():
    # 整理前端数据
    table_name = request.get_json()['table_name']
    sensors = request.get_json()['sensors']
    gateways = request.get_json()['gateways']
    crossings = request.get_json()['crossings']

    try:
        # 创建数据表
        db.session.execute(text(
            'CREATE TABLE `road-mark`.`c_' + table_name + '_sensors`  (\
            `id` int NOT NULL AUTO_INCREMENT,\
            `lng` varchar(60) NULL DEFAULT NULL,\
            `lat` varchar(60) NULL DEFAULT NULL,\
            `group` int NULL DEFAULT NULL,\
            `group_number` int NULL DEFAULT NULL,\
            PRIMARY KEY (`id`))'))

        db.session.execute(text(
            'CREATE TABLE `road-mark`.`c_' + table_name + '_gateways`  (\
            `id` int NOT NULL AUTO_INCREMENT,\
            `lng` varchar(60) NULL DEFAULT NULL,\
            `lat` varchar(60) NULL DEFAULT NULL,\
            `group` int NULL DEFAULT NULL,\
            `group_number` int NULL DEFAULT NULL,\
            PRIMARY KEY (`id`))'))

        db.session.execute(text(
            'CREATE TABLE `road-mark`.`c_' + table_name + '_crossings`  (\
            `id` int NOT NULL AUTO_INCREMENT,\
            `lng` varchar(60) NULL DEFAULT NULL,\
            `lat` varchar(60) NULL DEFAULT NULL,\
            PRIMARY KEY (`id`))'))

    except Exception:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '数据库中有同名数据表，请修改名称！',
            'data': None,
        })


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

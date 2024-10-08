import traceback

from flask import Blueprint, jsonify, request

from calculation.general import getData
from extensions import db
from models.datasets import Datasets
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
    name = request.args.get('table_name')
    result = getData(name)
    if result == 444:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '数据库错误！',
            'data': None,
        })
    return jsonify({
        'success': True,
        'code': HTTP_SUCCESS,
        'msg': '查询成功！',
        'data': result,
    })


@read_data_bp.route('/delete', methods=["DELETE"])
def delete_datasets():
    table_id = request.args.get('id')
    if table_id == 1:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '删除失败，默认数据库不允许删除！',
            'data': None,
        })
    rs = db.session.query(Datasets).filter_by(id=table_id).delete()
    db.session.commit()
    if rs != 1:
        return jsonify({
            'success': False,
            'code': HTTP_ERROR_OPERATION,
            'msg': '删除失败，数据库错误！',
            'data': None,
        })
    return jsonify({
        'success': True,
        'code': HTTP_SUCCESS,
        'msg': '删除成功！',
        'data': None,
    })

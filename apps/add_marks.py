from flask import Blueprint


add_marks_bp = Blueprint('add_marks', __name__)


@add_marks_bp.route('/')
def hw():
    return "HW"


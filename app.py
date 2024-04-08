from apps.read_data import read_data_bp
from apps.add_marks import add_marks_bp
from extensions import app


app.register_blueprint(add_marks_bp)
app.register_blueprint(read_data_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12002)

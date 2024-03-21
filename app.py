from extensions import app
from apps.add_marks import add_marks_bp


app.register_blueprint(add_marks_bp)

if __name__ == '__main__':
    app.run()

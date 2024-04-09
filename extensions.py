from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import config

app = Flask(__name__)
app.config.from_object(config)
CORS(app)
db = SQLAlchemy(app)


from flask import Flask

from app.main.bot import main
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


def create_app(config_name):
    app.config.from_object(config[config_name])
    app.register_blueprint(main)

    return app

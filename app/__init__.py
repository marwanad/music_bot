from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
db_inst = None

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    db_inst = db

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

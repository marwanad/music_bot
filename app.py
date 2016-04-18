from importlib import import_module
from api.message import api
import os
import sys
from flask import Flask

from kik import KikApi, Configuration

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

USER_NAME = os.environ["USER_NAME"]
API_KEY = os.environ["API_KEY"]
WEB_HOOK = os.environ["FLASK_WEBHOOK"]

app = Flask(__name__)
app.register_blueprint(api)
kik = KikApi(USER_NAME, API_KEY)

kik.set_configuration(Configuration(webhook=WEB_HOOK + '/receive'))

for file_name in os.listdir('{}/api'.format(os.path.dirname(os.path.realpath(__file__)))):
    if not file_name.startswith('.') and file_name.endswith('.py') and file_name != '__init__.py':
        import_module('api.{}'.format(file_name[:-3]))

if __name__ == "__main__":
    app.run(port=8080, debug=True)

__all__ = ['app']

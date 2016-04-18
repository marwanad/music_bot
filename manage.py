#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager
import requests
import json
from setup import bot_config

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

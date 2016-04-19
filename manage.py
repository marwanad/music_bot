#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager
import requests
import json
from setup import bot_config

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
@manager.command
def hookMeBro():
	requests.post(
		'https://api.kik.com/v1/config',
		auth=(bot_config["username"], bot_config["key"]),
		headers={
        'Content-Type': 'application/json'
        },
        data=json.dumps({
        	"webhook": "https://950746d8.ngrok.io/receive",
        	"features": {
        	"manuallySendReadReceipts": False,
        	"receiveReadReceipts": False,
            "receiveDeliveryReceipts": False,
            "receiveIsTyping": False
        }
    })
)

if __name__ == '__main__':
    manager.run()

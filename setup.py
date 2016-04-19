import os

from kik import KikApi

BOT_USERNAME = os.environ.get('MUSIK_USERNAME')
BOT_API_KEY = os.environ.get('MUSIK_API_KEY')

bot_config = {
	"username" : BOT_USERNAME,
	"key" : BOT_API_KEY
}

kik = KikApi(bot_config["username"], bot_config["key"])

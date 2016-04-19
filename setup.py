import os

from kik import KikApi
import spotipy.util as util

BOT_USERNAME = os.environ.get('MUSIK_USERNAME')
BOT_API_KEY = os.environ.get('MUSIK_API_KEY')
SPOTIFY_USERNAME = os.environ.get('SPOTIFY_USERNAME')

bot_config = {
	"username" : BOT_USERNAME,
	"key" : BOT_API_KEY
}

spotify_scope = 'user-library-read'

token = util.prompt_for_user_token(SPOTIFY_USERNAME, scope)

sp = spotipy.Spotify(auth=token)

kik = KikApi(bot_config["username"], bot_config["key"])

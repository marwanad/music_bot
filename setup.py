import os

from kik import KikApi
import spotipy.util as util

BOT_USERNAME = os.environ.get('MUSIK_USERNAME')
BOT_API_KEY = os.environ.get('MUSIK_API_KEY')
SPOTIFY_USERNAME = os.environ.get('SPOTIFY_USERNAME')
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')

bot_config = {
	"username" : BOT_USERNAME,
	"key" : BOT_API_KEY
}

spotify_scope = 'user-library-read'

token = util.prompt_for_user_token(SPOTIFY_USERNAME, spotify_scope, client_id=SPOTIFY_CLIENT_ID, client_secret= SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

kik = KikApi(bot_config["username"], bot_config["key"])

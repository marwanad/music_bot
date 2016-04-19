import os

from kik import KikApi
from spotipy import oauth2
import spotipy.util as util
import logging

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

CACHE = '.spotipyoauthcache'
spotify_scope = 'user-library-read'

sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,scope=spotify_scope,cache_path=CACHE)

url = sp_oauth.get_authorize_url()

logging.debug("auth url is ", url)
sp = spotipy.Spotify(access_token)

kik = KikApi(bot_config["username"], bot_config["key"])



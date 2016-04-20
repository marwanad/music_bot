import os

from kik import KikApi
import requests, base64
import spotipy.util as util
import spotipy

BOT_USERNAME = os.environ.get('MUSIK_USERNAME')
BOT_API_KEY = os.environ.get('MUSIK_API_KEY')

bot_config = {
	"username" : BOT_USERNAME,
	"key" : BOT_API_KEY
}

kik = KikApi(bot_config["username"], bot_config["key"])

spotify_scope = 'user-library-read'
SPOTIFY_USERNAME = os.environ.get('SPOTIFY_USERNAME')

token_data = {
    'grant_type':'refresh_token',
    'refresh_token': os.environ.get('SPOTIPY_REFRESH_TOKEN'),
}

clientID = os.environ.get('SPOTIPY_CLIENT_ID') + ":" + os.environ.get('SPOTIPY_CLIENT_SECRET')
b64Val = base64.b64encode(clientID)

r = requests.post('https://accounts.spotify.com/api/token', 
    headers={'Authorization': 'Basic ' + b64Val}
    , data=token_data)

token_response_json = r.json()

sp = spotipy.Spotify(auth=token_response_json['access_token'])

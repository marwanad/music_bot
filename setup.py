import os

from kik import KikApi
import requests, base64

BOT_USERNAME = os.environ.get('MUSIK_USERNAME')
BOT_API_KEY = os.environ.get('MUSIK_API_KEY')
token_response_json = None

bot_config = {
    "username": BOT_USERNAME,
    "key": BOT_API_KEY
}

kik = KikApi(bot_config["username"], bot_config["key"])


def get_spotify_token():
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': os.environ.get('SPOTIPY_REFRESH_TOKEN'),
    }

    clientID = os.environ.get('SPOTIPY_CLIENT_ID') + ":" + os.environ.get('SPOTIPY_CLIENT_SECRET')
    b64Val = base64.b64encode(clientID)
    r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': 'Basic ' + b64Val},
                      data=token_data)

    token_response_json = r.json()
    return token_response_json['access_token']

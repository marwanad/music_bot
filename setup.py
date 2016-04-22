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
    cached_token = os.environ.get('SPOTIPY_ACCESS_TOKEN')
    # if token is valid, no need to request a new one
    if (is_cached_token_valid()):
        print("Returning a cached token since it's valid")
        return cached_token

    # use the refresh token to get a new access token
    else:
    print("Requesting a new token!")
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': os.environ.get('SPOTIPY_REFRESH_TOKEN'),
    }

    clientID = os.environ.get('SPOTIPY_CLIENT_ID') + ":" + os.environ.get('SPOTIPY_CLIENT_SECRET')
    b64Val = base64.b64encode(clientID)
    r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': 'Basic ' + b64Val},
                      data=token_data)

    token_response_json = r.json()
    # get token from response and store
    access_token = token_response_json['access_token']
    os.environ["SPOTIPY_ACCESS_TOKEN"] = access_token

    return access_token

def is_cached_token_valid():
    cached_token = os.environ.get('SPOTIPY_ACCESS_TOKEN')
    print("Cached token is: ", cached_token)

    r = requests.post('https://api.spotify.com/v1/me', headers={'Authorization: Bearer ' + cached_token})
    return r.status_code == 200


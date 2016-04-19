import spotipy
import spotipy.util as util

scope = 'user-library-read'
username = 'rfarmaha'

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print "Can't get token for {0}".format(username)


def get_genres():
    return sp.recommendation_genre_seeds()['genres']


def get_songs_from_genre(genre, difficulty=50):
    song = sp._get('recommendations', seed_genres=genre, limit=1, min_popularity=difficulty)
    return song['tracks'][0]['preview_url']


def get_songs_from_artist(artist, difficulty=50):
    results = sp.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']
    if items:
        artist = items[0]
        id = artist['id']
        song = sp._get('recommendations', seed_artists=id, limit=1, min_popularity=difficulty)
        return song['tracks'][0]['preview_url']

print get_songs_from_artist('Drake')
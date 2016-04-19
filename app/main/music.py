# import os
# import spotipy
# import spotipy.util as util

# spotify_scope = 'user-library-read'
# SPOTIFY_USERNAME = os.environ.get('SPOTIFY_USERNAME')

# token = util.prompt_for_user_token(SPOTIFY_USERNAME, spotify_scope)

# sp = spotipy.Spotify(auth=token)

# def get_genres():
#     return sp.recommendation_genre_seeds()['genres']


# def get_song_from_genre(genre, difficulty=50):
#     song = sp._get('recommendations', seed_genres=genre, limit=1, min_popularity=difficulty)
#     if song:
#         return _get_only_id(song['tracks'][0]['preview_url'])
#     else:
#         print 'Cannot get recommendation'
#         raise Exception


# def get_song_from_artist(artist, difficulty=50):
#     results = sp.search(q='artist:' + artist, type='artist')
#     items = results['artists']['items']
#     if items:
#         artist = items[0]
#         id = artist['id']
#         song = sp._get('recommendations', seed_artists=id, limit=1, min_popularity=difficulty)
#         return _get_only_id(song['tracks'][0]['preview_url'])
#     else:
#         print 'Cannot find artist'
#         raise Exception


# def _get_only_id(url):
#     return url.split("/")[4]

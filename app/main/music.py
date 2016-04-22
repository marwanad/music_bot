import json
import random

import spotipy
import setup

preview_base_url="https://p.scdn.co/mp3-preview/"

PLAYLIST_IDS = ['5FJXhjdILmRA2z5bvz4nzf', '4hOKQuZbraPDIfaGbM3lKI', '5nPXGgfCxfRpJHGRY4sovK', '5UFRIQ89nVPcVsrWjLyjqI', '445ES7sgFV8zJHebmbUW0L']

class SP(object):
    sp = spotipy.Spotify(auth=setup.get_spotify_token())

def refresh_spotify_client():
    
    # return same instance if not none or new instance with token
    if(setup.is_cached_token_valid()):
        print("Called before request and found access token to be valid")
        return 
    print("returning new client with auth token: ", setup.get_spotify_token())
    SP.sp = spotipy.Spotify(auth=setup.get_spotify_token())

def get_genres():
    return SP.sp.recommendation_genre_seeds()['genres']

class Genre:
    GENRES = get_genres()


class Song:
    """Creates objects from Spotify music"""

    def __init__(self, album=None, artist=None, title=None, genre=None, album_art=None, preview_id=None):
        self.album = album
        self.artist = artist
        self.title = title
        self.genre = genre
        self.album_art = album_art
        self.preview_id = preview_id

    def to_json_string(self):
        return json.dumps(self, default=lambda x: x.__dict__)


def get_song_from_playlist(ownerid='spotify'):
    playlistid = random.choice(PLAYLIST_IDS)
    print "Getting song from playlist {0} owned by {1}".format(playlistid, ownerid)
    try:
        songs = SP.sp.user_playlist_tracks(ownerid, playlist_id=playlistid)['items']
        song = random.choice(songs)['track']
        final_song = Song(album=song['album']['name'],
                          artist=song['artists'][0]['name'],
                          title=song['name'],
                          album_art=song['album']['images'][1]['url'],
                          preview_id=_get_only_id(song['preview_url']))
        return final_song
    except:
        print 'Could not get playlist song'
        raise Exception


def get_song_from_genre(genre, difficulty=50):
    print ("getting song from genre ", genre)
    song_json = SP.sp._get('recommendations', seed_genres=genre, limit=1, min_popularity=difficulty)['tracks'][0]
    if song_json:
        final_song = Song(song_json['album']['name'],
                          song_json['artists'][0]['name'],
                          song_json['name'],
                          genre,
                          song_json['album']['images'][1]['url'],
                          _get_only_id(song_json['preview_url']))
        return final_song
    else:
        print 'Cannot get recommendation'
        raise Exception


def get_song_from_artist(artist, difficulty=50):
    results = SP.sp.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']
    if items:
        artist = items[0]
        artist_id = artist['id']
        song_json = SP.sp._get('recommendations', seed_artists=artist_id, limit=1, min_popularity=difficulty)['tracks'][0]
        if song_json:
            print 'Found song'
            song = Song(
                song_json['album']['name'],
                song_json['artists'][0]['name'],
                song_json['name'],
                None,
                song_json['album']['images'][1]['url'],
                _get_only_id(song_json['preview_url']))
            return song
        else:
            print 'Cannot parse song info'
            raise Exception
    else:
        print 'Cannot find artist'
        raise Exception


def _get_only_id(url):
    return url.split("/")[4]

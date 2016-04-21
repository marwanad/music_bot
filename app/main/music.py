import json
import spotipy
import setup


class Song:
    """Creates objects from Spotify music"""

    def __init__(self, album=None, artist=None, title=None, genre=None, album_art=None, preview_url=None):
        self.album = album
        self.artist = artist
        self.title = title
        self.genre = genre
        self.album_art = album_art
        self.preview_url = preview_url

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__)

    def match(self, answer):
        return self.title.strip().lower() == answer.strip().lower()


def refresh_spotify_client():
    return spotipy.Spotify(auth=setup.get_spotify_token())


sp = refresh_spotify_client()


def get_genres():
    return sp.recommendation_genre_seeds()['genres']


def get_song_from_genre(genre, difficulty=50):
    print ("getting song from genre ", genre)
    song_json = sp._get('recommendations', seed_genres=genre, limit=1, min_popularity=difficulty)['tracks'][0]
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
    results = sp.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']
    if items:
        artist = items[0]
        artist_id = artist['id']
        song_json = sp._get('recommendations', seed_artists=artist_id, limit=1, min_popularity=difficulty)['tracks'][0]
        if song_json:
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

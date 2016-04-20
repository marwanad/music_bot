import os
import spotipy
import setup


class Song:
    """Creates objects from Spotify music"""

    def __init__(self):
        self.album = None
        self.artist = None
        self.title = None
        self.genre = None
        self.album_art = None
        self.preview_url = None

    def with_album(self, album):
        self.album = album
        return self

    def with_artist(self, artist):
        self.artist = artist
        return self

    def with_title(self, title):
        self.title = title
        return self

    def with_genre(self, genre):
        self.genre = genre
        return self

    def with_album_art(self, album_art):
        self.album_art = album_art
        return self

    def with_preview_url(self, preview_url):
        self.preview_url = preview_url
        return self


def refresh_spotify_client():
    return spotipy.Spotify(auth=setup.get_spotify_token())


# sp = refresh_spotify_client()

def get_genres():
    return sp.recommendation_genre_seeds()['genres']


def get_song_from_genre(genre, difficulty=50):
    print ("getting song from genre ", genre)
    song_json = sp._get('recommendations', seed_genres=genre, limit=1, min_popularity=difficulty)['tracks'][0]
    if song_json:
        song = (Song
                .with_album(song_json['album']['name'])
                .with_artist(song_json['artists'][0]['name'])
                .with_title(song_json['name'])
                .with_genre(genre)
                .with_album_art(song_json['album']['images'][1]['url'])
                .with_preview_url(_get_only_id(song_json['preview_url'])))
        return song
    else:
        print 'Cannot get recommendation'
        raise Exception


def get_song_from_artist(artist, difficulty=50):
    results = sp.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']
    if items:
        artist = items[0]
        id = artist['id']
        song_json = sp._get('recommendations', seed_artists=id, limit=1, min_popularity=difficulty)['tracks'][0]
        if song_json:
            song = (Song
                    .with_album(song_json['album']['name'])
                    .with_artist(song_json['artists'][0]['name'])
                    .with_title(song_json['name'])
                    .with_album_art(song_json['album']['images'][1]['url'])
                    .with_preview_url(_get_only_id(song_json['preview_url'])))
            return song
        else:
            print 'Cannot parse song info'
            raise Exception
    else:
        print 'Cannot find artist'
        raise Exception


def _get_only_id(url):
    return url.split("/")[4]

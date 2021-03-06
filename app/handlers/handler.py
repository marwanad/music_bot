import random

import util
from app.xlib.responder import Responder
from app.xlib.states import StateType
from app.xlib.sr_strings import srs
from app.xlib.states import StateString
from ..main import music
from .. import db
from ..decorators import check_state
import json


class Handler(object):
    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_intro(to, game, body, response=StateString.INTRO):
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_genre(to, game, body, response=StateString.GENRE):
        game.state = StateType.GENRE_SELECT

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.GENRE_SELECT])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_artist(to, game, body, response=StateString.ARTIST):
        game.state = StateType.ARTIST_SELECT

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.ARTIST_SELECT])

    @staticmethod
    @check_state(StateType.GENRE_SELECT, StateType.ARTIST_SELECT, StateType.INITIAL)
    def handle_song(to, game, body, song=None):
        if not song:
            song = music.get_song_from_playlist()

        game.state = StateType.ANSWER_TIME
        game.song = song.to_json_string()
        print("Adding song json to the db: ", game.song)

        Responder.send_wubble_response(to, game.id, song.preview_id, keyboards=srs.grouped_srs[StateType.ANSWER_TIME])

    @staticmethod
    def handle_back(to, game, body, response=StateString.BACK):
        game.state = StateType.INITIAL
        game.song = None
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_score(to, game, body, response=StateString.SCORE):
        print 'game', game
        print 'scores', game.scores
        scores = json.loads(game.scores)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for tup in sorted_scores:
            response = response + tup[0] + ': ' + str(tup[1]) + '\n'
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_settings(to, game, body, response=StateString.DIFFICULTY):
        game.state = StateType.SETTINGS
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.SETTINGS])

    @staticmethod
    @check_state(StateType.SETTINGS)
    def handle_difficulty(to, game, body):
        game.state = StateType.INITIAL
        if body == 'easy':
            game.difficulty = 60
        elif body == 'hard':
            game.difficulty = 0
        elif body == 'medium':
            game.difficulty = 30

        response = 'Difficulty has been set to ' + body

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    def handle_fallback(to, game, body, response=None):
        if response:
            response = 'I don\'t understand what you mean by "{}"'.format(response)
        else:
            response = random.choice(StateString.FALLBACK_STRINGS)

        Responder.send_text_response(to, game.id, response,
                                     keyboards=srs.grouped_srs.get(game.state, srs.grouped_srs[StateType.INITIAL]))

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_hint(to, game, body):
        try:
            if game:
                song = json.loads(game.song)
                print 'song: %r' % song

                album_art = song['album_art'] or 'http://i.imgur.com/DUCOwkM.jpg'
                album = song['album'] or 'Album art'

                print 'album_art: %r' % album_art
                print 'album: %r' % album
                Responder.send_image_response(to, game.id, album_art, album,
                                              keyboards=srs.grouped_srs[StateType.ANSWER_TIME])
        except Exception as e:
            print 'HANDLE_HINT ERROR: %r' % e
            Handler.handle_error(to, game)
            return

    @staticmethod
    def handle_error(to, game, response=StateString.ERROR):
        game.state = StateType.INITIAL
        db.session.commit()
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_answer(to, game, body):
        hidden_sr = True

        try:
            if game:
                song = json.loads(game.song)
        except Exception as e:
            print 'HANDLE_ANSWER ERROR: %r' % e
            Handler.handle_error(to, game)
            return

        if song and util.guess_matches_answer(body, song['title'].lower()):
            game.state = StateType.INITIAL
            game.song = None

            print 'scores %r', game.scores
            scores = json.loads(game.scores)
            scores[to] = scores.get(to, 0) + 1
            game.scores = json.dumps(scores)

            response = random.choice(StateString.CORRECT)
            response += ' ' + random.choice(StateString.CORRECT_EMOJI)
            response += '\nIt\'s "{song}" by {artist}'.format(song=song['title'], artist=song['artist'])
            keyboards = srs.grouped_srs[StateType.INITIAL]
            hidden_sr = False
        else:
            if body in ['back', 'skip', 'next']:
                back_message = 'Giving up? The song was "{song}" by {artist}'.format(song=song['title'], artist=song['artist'])
                Handler.handle_back(to, game, body, back_message)
                return
            elif body == 'hint':
                Handler.handle_hint(to, game, body)
                return
            else:
                response = random.choice(StateString.INCORRECT)
                response += ' ' + random.choice(StateString.INCORRECT_EMOJI)
                keyboards = srs.grouped_srs[StateType.ANSWER_TIME]
        Responder.send_text_response(to, game.id, response, keyboards, hidden_sr)

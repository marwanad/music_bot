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
    def handle_intro(to, game, response=StateString.INTRO):
        Responder.send_text_response(to, game.id, response)

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, game, response=StateString.START_QUIZ):

        game.state = StateType.START_SELECT
        db.session.commit()
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['song_options'])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, game, response=StateString.GENRE):
        game.state = StateType.GENRE_SELECT
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['genre'])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, game, response=StateString.ARTIST):
        game.state = StateType.ARTIST_SELECT
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['artist'])

    @staticmethod
    def handle_song(to, game, song=None, response=StateString.SONG):
        track_preview = song
        if not track_preview:
            # grab a random song id (prob from popular playlist)
            song = music.get_song_from_genre('pop')

        game.state = StateType.ANSWER_TIME
        db.session.commit()
        
        game.song = song.to_json()
        db.session.commit()

        # for testing purposes
        song_details = 'title: ' + track_preview.title + '\n' + 'artist: ' + track_preview.artist + '\n';
        Responder.send_text_response(to, game.id, song_details)
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['menu'], hidden=True)

        print("Adding song json to the db: ", game.song)
        Responder.send_wubble_response(to, game.id, song, keyboards=srs.grouped_srs['answer'])

    @staticmethod
    def handle_back(to, game, response=StateString.BACK):
        game.state = StateType.INITIAL
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_share(to, game, response=StateString.SHARE):
        game.state = StateType.INITIAL
        db.session.commit()

    @staticmethod
    def handle_score(to, game, response=StateString.SCORE):
        scores = json.loads(game.scores)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for tup in sorted_scores:
            response = response + tup[0] + ': ' + str(tup[1]) + '\n'
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_settings(to, game, response=StateString.SETTINGS):
        game.state = StateType.SETTINGS
        db.session.commit()
        
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['settings'])

    @staticmethod
    def handle_difficulty(to, game, body, response=StateString.DIFFICULTY):
        game.state = StateType.DIFFICULTY
        db.session.commit()
        if body == 'easy':
            game.difficulty = 80
        elif body == 'hard':
            game.difficulty = 20

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['difficulty'])

    @staticmethod
    def handle_fallback(to, game, response=None):
        if response:
            response = 'I don\'t understand what you mean by "{}"'.format(response)
        else:
            response = 'Not a text message'

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_answer(to, game, body):

        hide_sr = True
        body = body.lower()
        # # todo hints?

        if body == 'back':
            Handler.handle_back(to, game)
            return
        elif game.song and body == json.loads(game.song)['title'].lower():
            # TODO ignore punctuation in both guess and answer
            game.state = StateType.INITIAL
            game.song = None

            # increment score
            scores = json.loads(game.scores)
            scores[to] = scores.get(to, 0) + 1
            game.scores = json.dumps(scores)
            db.session.commit()
            
            response = 'Correct!'
            keyboards = srs.grouped_srs['menu']
            hide_sr = False
        else:
            response = 'Incorrect'
            keyboards = srs.grouped_srs['answer']
        Responder.send_text_response(to, game.id, response, keyboards, hide_sr)

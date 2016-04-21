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
    def handle_intro(to, game, body=StateString.INTRO):
        Responder.send_text_response(to, game.id, body)

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, game, body=StateString.START_QUIZ):

        game.state = StateType.START_SELECT
        db.session.commit()
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['song_options'])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, game, body=StateString.GENRE):
        game.state = StateType.GENRE_SELECT
        db.session.commit()

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['genre'])
        srs.register_sr('genre', 'handle_genre')

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, game, body=StateString.ARTIST):
        game.state = StateType.ARTIST_SELECT
        db.session.commit()

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['artist'])

    @staticmethod
    def handle_song(to, game, song=None, body=StateString.SONG):
        if not song:
            # grab a random song id (prob from popular playlist)
            song = music.get_song_from_genre('pop')

        game.state = StateType.ANSWER_TIME
        db.session.commit()
        
        game.song = song.to_json()
        # db.session.commit()

        print("Adding song json to the db: ", game.song)
        Responder.send_wubble_response(to, game.id, song)

        Responder.send_text_response(to, game.id, song.title, keyboards=srs.grouped_srs['menu'], hidden=True)

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['menu'], hidden=True)

    @staticmethod
    def handle_back(to, game, body=StateString.BACK):
        game.state = StateType.INITIAL
        db.session.commit()

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_share(to, game, body=StateString.SHARE):
        game.state = StateType.INITIAL
        db.session.commit()

    @staticmethod
    def handle_score(to, game, body=StateString.SCORE):
        scores = json.loads(game.scores)[0]
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for tup in sorted_scores:
            body = body + tup[0] + ': ' + str(tup[1]) + '\n'
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_settings(to, game, body=StateString.SETTINGS):
        game.state = StateType.INITIAL
        db.session.commit()

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_fallback(to, game, body=None):
        if body:
            body = 'I don\'t understand what you mean by "{}"'.format(body)
        else:
            body = 'Not a text message'

        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_answer(to, game, body):

        hide_sr = True
        body = body.lower()
        # # todo hints?

        if body == 'back':
            Handler.handle_back(to, game)
            return
        elif game.song and util.guess_matches_answer(body, json.loads(game.song)['title']):
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

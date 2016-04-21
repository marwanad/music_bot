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
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, game, body=StateString.START_QUIZ):
        game.state = StateType.START_SELECT
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.START_SELECT])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, game, body=StateString.GENRE):
        game.state = StateType.GENRE_SELECT
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.GENRE_SELECT])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, game, body=StateString.ARTIST):
        game.state = StateType.ARTIST_SELECT
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.ARTIST_SELECT])

    @staticmethod
    @check_state(StateType.GENRE_SELECT, StateType.ARTIST_SELECT, StateType.START_SELECT)
    def handle_song(to, game, song=None, body=StateString.SONG):
        if not song:
            song = music.get_song_from_playlist()

        game.state = StateType.ANSWER_TIME
        game.song = song.to_json_string()
        print("Adding song json to the db: ", game.song)

        Responder.send_wubble_response(to, game.id, song.preview_id, keyboards=srs.grouped_srs[StateType.ANSWER_TIME])

    @staticmethod
    def handle_back(to, game, body=StateString.BACK):
        game.state = StateType.INITIAL
        game.song = None
        db.session.commit()
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_score(to, game, body=StateString.SCORE):
        print 'game', game
        print 'scores', game.scores
        scores = json.loads(game.scores)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for tup in sorted_scores:
            body = body + tup[0] + ': ' + str(tup[1]) + '\n'
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_settings(to, game, body=StateString.SETTINGS):
        #todo: need to finish settings implementation
        game.state = StateType.INITIAL
        game.song = None
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    def handle_error(to, game, body=StateString.ERROR):
        game.state = StateType.INITIAL
        game.song = None
        db.session.commit()
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    def handle_fallback(to, game, body=None, song=None):
        if body:
            body = 'I don\'t understand what you mean by "{}"'.format(body)
        else:
            body = 'Not a text message'

        Responder.send_text_response(to, game.id, body,
                                     keyboards=srs.grouped_srs.get(game.state, srs.grouped_srs[StateType.INITIAL]))

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_answer(to, game, body):
        hidden_sr = True
        # todo hints?
        try:
            song = json.loads(game.song)
        except:
            Handler.handle_error(to, game)
            return
        if body == 'back':
            back_message = 'Giving up? The song was "' + song['title'] + '" by ' + song['artist']
            Handler.handle_back(to, game, back_message)
        elif game:
            if song and util.guess_matches_answer(body, song['title'].lower()):
                game.state = StateType.INITIAL
                game.song = None

                print 'scores %r', game.scores
                scores = json.loads(game.scores)
                scores[to] = scores.get(to, 0) + 1
                game.scores = json.dumps(scores)

                response = 'Correct!'
                keyboards = srs.grouped_srs[StateType.INITIAL]
                hidden_sr = False
            else:
                response = 'Incorrect'
                keyboards = srs.grouped_srs[StateType.ANSWER_TIME]
            Responder.send_text_response(to, game.id, response, keyboards, hidden_sr)

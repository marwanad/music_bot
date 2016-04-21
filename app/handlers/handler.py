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
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, game, response=StateString.START_QUIZ):
        game.state = StateType.START_SELECT
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.START_SELECT])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, game, response=StateString.GENRE):
        game.state = StateType.GENRE_SELECT
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.GENRE_SELECT])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, game, response=StateString.ARTIST):
        game.state = StateType.ARTIST_SELECT

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.ARTIST_SELECT])

    @staticmethod
    @check_state(StateType.GENRE_SELECT, StateType.ARTIST_SELECT, StateType.START_SELECT)
    def handle_song(to, game, song=None, response=StateString.SONG):
        if not song:
            song = music.get_song_from_playlist()

        game.state = StateType.ANSWER_TIME
        game.song = song.to_json_string()
        print("Adding song json to the db: ", game.song)

        Responder.send_wubble_response(to, game.id, song.preview_url)

    @staticmethod
    def handle_back(to, game, response=StateString.BACK):
        game.state = StateType.INITIAL
        game.song = None
        db.session.commit()

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_share(to, game, response=StateString.SHARE):
        game.state = StateType.INITIAL
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
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
        
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.SETTINGS])

    @staticmethod
    def handle_difficulty(to, game, body, response=StateString.DIFFICULTY):
        game.state = StateType.DIFFICULTY
        db.session.commit()
        if body == 'easy':
            game.difficulty = 80
        elif body == 'hard':
            game.difficulty = 20

        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateString.DIFFICULTY])

    @staticmethod
    def handle_fallback(to, game, response=None):
        if response:
            response = 'I don\'t understand what you mean by "{}"'.format(response)
        else:
            response = 'Not a text message'

        Responder.send_text_response(to, game.id, response,
                                     keyboards=srs.grouped_srs.get(game.state, srs.grouped_srs[StateType.INITIAL]))

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_answer(to, game, body):
        hidden_sr = True
        # todo hints?
        if body == 'back':
            Handler.handle_back(to, game)
        elif game:
            try:
                song = json.loads(game.song)
            except:
                Handler.handle_error(to, game)
                return

            if song and body == json.loads(song)['title'].lower():
                game.state = StateType.INITIAL
                game.song = None

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

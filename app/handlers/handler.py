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
        db.session.commit()

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
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.DIFFICULTY])

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
            response = 'Not a text message'

        Responder.send_text_response(to, game.id, response,
                                     keyboards=srs.grouped_srs.get(game.state, srs.grouped_srs[StateType.INITIAL]))

    @staticmethod
    def handle_error(to, game, response=StateString.ERROR):
        game.state = StateType.INITIAL
        db.session.commit()
        Responder.send_text_response(to, game.id, response, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_answer(to, game, body):
        hidden_sr = True
        # todo hints?

        try:
            if game:
                song = json.loads(game.song)
        except Exception as e:
            print 'HANDLE_ANSWER ERROR: %r' % e
            Handler.handle_error(to, game)
            return
        
        if body == 'back':
            back_message = to + ' gave up. The song was "' + song['title'] + '" by ' + song['artist']
            Handler.handle_back(to, game, body, back_message)
        else:
            if song and util.guess_matches_answer(body, song['title'].lower()):
                game.state = StateType.INITIAL
                game.song = None
                keyboards = srs.grouped_srs[StateType.INITIAL]
                hidden_sr = False

                if game.state == StateType.ANSWER_TIME:
                    print 'scores %r', game.scores
                    scores = json.loads(game.scores)
                    high_score = max(scores, key=scores.get)
                    scores[to] = scores.get(to, 0) + 1
                    game.scores = json.dumps(scores)

                    response = 'Correct!'
                    if(high_score < scores[to]):
                        response = response + " " + to + " set a new high score with " + scores[to] + " points!"
                else:
                    response = "Too late!"

            else:
                response = 'Incorrect'
                keyboards = srs.grouped_srs[StateType.ANSWER_TIME]
            Responder.send_text_response(to, game.id, response, keyboards, hidden_sr)

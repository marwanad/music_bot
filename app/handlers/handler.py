from app.xlib.responder import Responder
from app.xlib.game import StateType
from app.xlib.sr_strings import srs
from app.xlib.states import StateString
from ..main import music
from .. import db
from ..decorators import check_state


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
            try:
                song = music.get_song_from_playlist()
            except:
                Handler.handle_error(to, game)
                return

        game.state = StateType.ANSWER_TIME
        game.song = song.to_json_string()

        Responder.send_wubble_response(to, game.id, song.preview_url)

        # for testing purposes
        song_details = 'title: ' + song.title + '\n' + 'artist: ' + song.artist + '\n'
        Responder.send_text_response(to, game.id, song_details)
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL], hidden=True)

    @staticmethod
    def handle_back(to, game, body=StateString.BACK):
        game.state = StateType.INITIAL
        game.song = '{}'
        db.session.commit()
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_share(to, game, body=StateString.SHARE):
        #todo: need to finish settings implementation
        game.state = StateType.INITIAL
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_score(to, game, body=StateString.SCORE):
        pass
        # sorted_scores = sorted(game.scores.items(), key=lambda x: x[1])
        # for tuple in sorted_scores:
        #     body = body + tuple[0] + ': ' + str(tuple[1]) + '\n'
        # Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_settings(to, game, body=StateString.SETTINGS):
        #todo: need to finish settings implementation
        game.state = StateType.INITIAL
        game.song = '{}'
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    def handle_error(to, game, body=StateString.ERROR):
        game.state = StateType.INITIAL
        game.song = '{}'
        db.session.commit()
        Responder.send_text_response(to, game.id, body, keyboards=srs.grouped_srs[StateType.INITIAL])

    @staticmethod
    def handle_fallback(to, game, body=None):
        if body:
            body = 'I don\'t understand what you mean by "{}"'.format(body)
        else:
            body = 'Not a text message'

        Responder.send_text_response(to, game.id, body,
                                     keyboards=srs.grouped_srs.get(game.state, srs.grouped_srs[StateType.INITIAL]))

    @staticmethod
    @check_state(StateType.ANSWER_TIME)
    def handle_answer(to, game, body):
        pass
        # hidden = True
        # # todo hints?
        if body.lower() == 'back':
            Handler.handle_back(to, game)
            return
            # elif game.current_song and body.lower() == game.current_song.title.lower():
            #     game.set_state(StateType.INITIAL)
            #     game.set_current_song(None)
            #     game.increment_score(to)
            #     response = 'Correct!'
            #     keyboards = srs.grouped_srs[StateType.INITIAL]
            #     hidden = False
            # else:
            #     response = 'Incorrect'
            #     keyboards = srs.grouped_srs[StateType.ANSWER_TIME]
            # Responder.send_text_response(to, game.id, response, keyboards, hidden)

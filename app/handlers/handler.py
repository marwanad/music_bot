from app.xlib.responder import Responder
from app.xlib.game import StateType, get_game
from app.xlib.sr_strings import srs
from app.xlib.states import StateString
from ..main import music
from ..decorators import check_state

class Handler(object):
    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_intro(to, chat_id, body=StateString.INTRO):
        Responder.send_text_response(to, chat_id, body)

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, chat_id, body=StateString.START_QUIZ):
        get_game(chat_id).set_state(StateType.START_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['song_options'])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, chat_id, body=StateString.GENRE):
        get_game(chat_id).set_state(StateType.GENRE_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['genre'])
        srs.register_sr('genre', 'handle_genre')

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, chat_id, body=StateString.ARTIST):
        get_game(chat_id).set_state(StateType.ARTIST_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['artist'])

    @staticmethod
    def handle_song(to, chat_id, song=None, body=StateString.SONG):
        track_preview = song
        if not track_preview:
            # grab a random song id (prob from popular playlist)
            track_preview = music.get_song_from_genre('pop')

        get_game(chat_id).set_state(StateType.ANSWER_TIME)
        get_game(chat_id).set_current_song(track_preview)
        Responder.send_wubble_response(to, chat_id, track_preview)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'], hidden=True)

    @staticmethod
    def handle_back(to, chat_id, body=StateString.BACK):
        get_game(chat_id).set_state(StateType.INITIAL)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_share(to, chat_id, body=StateString.SHARE):
        get_game(chat_id).set_state(StateType.INITIAL)

    @staticmethod
    def handle_score(to, chat_id, body=StateString.SCORE):
        game = get_game(chat_id)
        sorted_scores = sorted(game.scores.items(), key=lambda x: x[1])
        for tuple in sorted_scores:
            body = body + tuple[0] + ': ' + str(tuple[1]) + '\n'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_settings(to, chat_id, body=StateString.SETTINGS):
        get_game(chat_id).set_state(StateType.INITIAL)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_fallback(to, chat_id, body=None):
        if body:
            body = 'I don\'t understand what you mean by "{}"'.format(body)
        else:
            body = 'Not a text message'

        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_answer(to, chat_id, body):
        game = get_game(chat_id)
        hidden = True
        # todo hints?
        if body.lower() == 'back':
            Handler.handle_back(to, chat_id)
            return
        elif body.lower() == game.answer.lower():
            game.set_state(StateType.INITIAL)
            game.set_current_song(None)
            game.increment_score(to)
            response = 'Correct!'
            keyboards = srs.grouped_srs['menu']
            hidden = False
        else:
            response = 'Incorrect'
            keyboards = srs.grouped_srs['answer']
        Responder.send_text_response(to, chat_id, response, keyboards, hidden)

from app.xlib.responder import Responder
from app.xlib.game import StateType, Game
from app.xlib.sr_strings import srs
from ..main import music
from ..decorators import check_state


class Handler(object):
    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_intro(to, chat_id):
        body = 'Hi you reached the intro stage, tap a sr for more options'
        Responder.send_text_response(to, chat_id, body)

    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_start_quiz(to, chat_id):
        body = 'Select genre, artist, or random'
        Game.get_game(chat_id).set_state(StateType.START_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['song_options'])

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_genre(to, chat_id):
        body = 'Select a genre'
        Game.get_game(chat_id).set_state(StateType.GENRE_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['genre'])
        srs.register_sr('genre', 'handle_genre')

    @staticmethod
    @check_state(StateType.START_SELECT)
    def handle_artist(to, chat_id):
        body = 'Select an artist'
        Game.get_game(chat_id).set_state(StateType.ARTIST_SELECT)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['artist'])

    @staticmethod
    def handle_song(to, chat_id, song_id=None):
        track_preview_id = song_id
        if not track_preview_id:
            # grab a random song id (prob from popular playlist)
            track_preview_id = music.get_song_from_genre('pop')

        body = 'What\'s the name of this song?'
        Game.get_game(chat_id).set_state(StateType.ANSWER_TIME)
        Game.get_game(chat_id).set_answer("Ultralight Beam")
        Responder.send_wubble_response(to, chat_id, track_preview_id)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'], hidden=True)

    @staticmethod
    def handle_back(to, chat_id):
        body = 'Ok, heading back'
        Game.get_game(chat_id).set_state(StateType.INITIAL)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_custom_track(to, chat_id):
        body = 'custom track'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_share(to, chat_id):
        body = 'share'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_settings(to, chat_id):
        body = 'settings'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_fallback(to, chat_id, body=None):
        if body:
            body = body.lower()
        else:
            body = 'Not a text message'

        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

    @staticmethod
    def handle_answer(to, chat_id, body):
        game = Game.get_game(chat_id)
        hidden = False
        # todo hints?
        if body.lower() == 'back':
            Handler.handle_back(to, chat_id)
            return
        elif body.lower() == game.answer.lower():
            game.set_state(StateType.INITIAL)
            game.increment_score(to)
            response = 'Correct!'
            keyboards = srs.grouped_srs['menu']
            hidden = True
        else:
            response = 'Incorrect'
            keyboards = srs.grouped_srs['answer']
        Responder.send_text_response(to, chat_id, response, keyboards, hidden)
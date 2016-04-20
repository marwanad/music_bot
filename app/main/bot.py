from flask import request, Response, render_template
from kik.messages import messages_from_json, TextMessage, StartChattingMessage

from app.xlib.decorators import check_state
from app.xlib.game import Game, StateType
from app.xlib.responder import Responder
from app.xlib.sr_strings import srs

from . import main
from setup import kik
import music

preview_base_url = "https://p.scdn.co/mp3-preview/"

@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        to = message.from_user
        chat_id = message.chat_id
        body = message.body.lower()
        # do something with this game
        game = Game.get_game(chat_id)
        if isinstance(message, StartChattingMessage):
            Handler.handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            if body == "give track pls":
                Handler.handle_song(to, chat_id)
                return Response(status=200)

            fn = srs.srs.get(body)
            if not fn:
                if srs.match_group_sr('genre', body):
                    # enter "listening for answers" state
                    Handler.handle_song(to, chat_id, music.get_song_from_genre(body))
                elif srs.match_group_sr('artist', body):
                    # enter "listening for answers" state
                    Handler.handle_song(to, chat_id, music.get_song_from_artist(body))
                else:
                    Handler.handle_fallback(to, chat_id, body)
                return Response(status=200)
            getattr(Handler, fn)(to, chat_id)
        else:
            Handler.handle_fallback(to, chat_id)
        return Response(status=200)


@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html', preview_url=preview_base_url + id)


class Handler(object):
    @staticmethod
    @check_state(StateType.INITIAL)
    def handle_intro(to, chat_id):
        body = 'Hi you reached the intro stage, tap a sr for more options :+1:'
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
        if not song_id:
            # grab a random song id (prob from popular playlist)
            song_id = music.get_song_from_genre('pop')
        body = 'Tap song above'
        Game.get_game(chat_id).set_state(StateType.INITIAL)
        Responder.send_wubble_response(to, chat_id, song_id)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

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

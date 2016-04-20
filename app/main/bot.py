from flask import request, Response, render_template
from kik.messages import messages_from_json, TextMessage, StartChattingMessage

from app.xlib.game import Game, StateType
from app.xlib.sr_strings import srs

from . import main
from setup import kik
from ..handlers import handler
import music

preview_base_url = "https://p.scdn.co/mp3-preview/"

@main.before_request
def before_request():
    music.refresh_spotify_client()
            
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
            handler.handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            if body == "give track pls":
                handler.handle_song(to, chat_id)
                return Response(status=200)

            fn = srs.srs.get(body)
            if not fn:
                if srs.match_group_sr('genre', body):
                    # enter "listening for answers" state
                    handler.handle_song(to, chat_id, music.get_song_from_genre(body))
                elif srs.match_group_sr('artist', body):
                    # enter "listening for answers" state
                    handler.handle_song(to, chat_id, music.get_song_from_artist(body))
                else:
                    handlers.handle_fallback(to, chat_id, body)
                return Response(status=200)
        else:
            handler.handle_fallback(to, chat_id)
        return Response(status=200)


@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html', preview_url=preview_base_url + id)
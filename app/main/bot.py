from flask import request, Response, render_template
from kik.messages import messages_from_json, TextMessage, StartChattingMessage

from app.handlers.handler import Handler
from app.xlib.game import StateType, get_game
from app.xlib.sr_strings import srs
from ..models import State
from .. import db

from . import main
from setup import kik
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
        game = None
        if not db.session.query(State).filter(State.id == chat_id).count():
        	print("No game found in db, creating a new game instance and adding to db")
        	game = get_game(chat_id)
        	db.session.add(game)
        else:
        	print("Restoring existing instance from db")
        	game = db.session.query(State).filter(State.id == chat_id).first_or_

        if isinstance(message, StartChattingMessage):
            Handler.handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            print game
            print game.state

            if game.state == StateType.ANSWER_TIME:
                Handler.handle_answer(to, chat_id, body)
                return Response(status=200)

            if body == "give track pls":
                Handler.handle_song(to, chat_id)
                return Response(status=200)

            fn = srs.srs.get(body)
            if not fn:
                genres = music.get_genres()
                # genres in this list probably need to be processed before checking against body
                if body in genres:
                    Handler.handle_song(to, chat_id, music.get_song_from_genre(body))
                elif srs.match_group_sr('artist', body):
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

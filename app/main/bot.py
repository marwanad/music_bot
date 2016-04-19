from flask import request, Response, url_for, render_template
from kik.messages import messages_from_json, TextMessage, StartChattingMessage
from app.xlib.responder import Responder
from app.xlib.sr_strings import srs

from . import main
from setup import kik
from wubble import WubbleMessage
import music

preview_base_url = "https://p.scdn.co/mp3-preview/"

def match_group_sr(group_sr, message):
    # use hardcoded genres until we get spotify working
    return message in map(lambda x: x.body.lower(), srs.grouped_srs[group_sr])

def get_song_from_genre(genre):
    #handle genre search
    return '53a95c27490ea1a42e0264a57fc73dacb961f2a7'

def get_song_from_artist(genre):
    #handle genre search
    return '53a95c27490ea1a42e0264a57fc73dacb961f2a7'

@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        to = message.from_user
        chat_id = message.chat_id
        body = message.body.lower()
        if isinstance(message, StartChattingMessage):
            Handler.handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            if ((body) == "give track pls"):
                kik.send_messages([
                    WubbleMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        url=url_for("main.music_player", id="53a95c27490ea1a42e0264a57fc73dacb961f2a7", _external=True)
                    )
                ])
                return Response(status=200)

            fn = srs.srs.get(body)
            if not fn:
                if match_group_sr('genre', body):
                    # enter "listening for answers" state
                    # get random song id of that genre
                    song_id = get_song_from_genre(body)
                    Handler.handle_song(to, chat_id, song_id)
                elif match_group_sr('artist', body):
                    # enter "listening for answers" state
                    # get random song id of that artist
                    song_id = get_song_from_artist(body)
                    Handler.handle_song(to, chat_id, song_id)
                else:
                    Handler.handle_fallback(to, chat_id)
                return Response(status=200)
            getattr(Handler, fn)(to, chat_id, body)
        else:
            Handler.handle_fallback(to, chat_id)
        return Response(status=200)


@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html', preview_url=preview_base_url + id)


class Handler(object):
    @staticmethod
    def handle_intro(to, chat_id):
        body = 'Hi you reached the intro stage, tap a sr for more options :+1:'
        Responder.send_text_response(to, chat_id, body)

    @staticmethod
    def handle_start_quiz(to, chat_id):
        body = 'Select genre, artist, or random'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['song_options'])

    @staticmethod
    def handle_genre(to, chat_id):
        body = 'Select a genre'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['genre'])
        srs.register_sr('genre', 'handle_genre')

    @staticmethod
    def handle_artist(to, chat_id):
        body = 'Select an artist'
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['artist'])

    @staticmethod
    def handle_song(to, chat_id, song_id=None):
        if not song_id:
            # grab a random song id (prob from popular playlist)
            song_id = '53a95c27490ea1a42e0264a57fc73dacb961f2a7'
        body = 'Tap song above'
        Responder.send_wubble_response(to, chat_id, song_id)
        Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['skip'])

    @staticmethod
    def handle_skip(to, chat_id):
        body = 'Ok, skipping'
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

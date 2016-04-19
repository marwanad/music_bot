from flask import request, Response, url_for, render_template
from kik.messages import messages_from_json, TextMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse
from kik import KikApi, Configuration
from app.xlib.responder import Responder
from app.xlib.sr_strings import srs

from . import main
from setup import kik
from wubble import WubbleMessage
import music

MAIN_SR = [TextResponse(body=sr) for sr in ['Start a quiz', 'Custom track', 'Share', 'Settings']]

preview_base_url = "https://p.scdn.co/mp3-preview/"

@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        to = message.to
        chat_id = message.chat_id
        if isinstance(message, StartChattingMessage):
            Handler.handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            if((message.body) == "give track pls"):
                kik.send_messages([
                    WubbleMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    url="https://songiq.herokuapp.com/musicplayer/53a95c27490ea1a42e0264a57fc73dacb961f2a7"
                )
                    ])
                return Response(status=200)

            fn = srs.srs.get(message.body.lower())
            if not fn:
                Handler.handle_fallback(to, chat_id)
                return Response(status=200)
            getattr(Handler, fn)(to, chat_id)
        else:
            Handler.handle_fallback(to, chat_id)
        return Response(status=200)


@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html',
                           preview_url=preview_base_url+id)

class Handler(object):
    @staticmethod
    def handle_intro(to, chat_id):
        body = 'Hi you reached the intro stage, tap a sr for more options :+1:'
        Responder.send_text_response(to, chat_id, body)

    @staticmethod
    def handle_start_quiz(to, chat_id):
        body = 'start quiz'
        Responder.send_text_response(to, chat_id, body, keyboards=[MAIN_SR])

    @staticmethod
    def handle_custom_track(to, chat_id):
        body = 'custom track'
        Responder.send_text_response(to, chat_id, body, keyboards=[MAIN_SR])

    @staticmethod
    def handle_share(to, chat_id):
        body = 'share'
        Responder.send_text_response(to, chat_id, body, keyboards=[MAIN_SR])

    @staticmethod
    def handle_settings(to, chat_id):
        body = 'settings'
        Responder.send_text_response(to, chat_id, body, keyboards=[MAIN_SR])

    @staticmethod
    def handle_fallback(to, chat_id):
        body = 'fallback'
        Responder.send_text_response(to, chat_id, body, keyboards=[MAIN_SR])


@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html', preview_url=preview_base_url+id)

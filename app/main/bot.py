from flask import request, Response
from kik.messages import messages_from_json, TextMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse

from app.xlib.responder import Responder
from app.xlib.sr_strings import srs

from . import main
from setup import kik

INTRO_BODY = 'Hi you reached the intro stage, tap a sr for more options'
FALLBACK_BODY = 'Sorry I didn\'t understand what you said'


@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        to = message.to
        chat_id = message.chat_id
        if isinstance(message, StartChattingMessage):
            handle_intro(to, chat_id)
        elif isinstance(message, TextMessage):
            fn = srs.srs.get(message.body.lower())
            if not fn:
                handle_fallback(to, chat_id)
            fn(to, chat_id)
        else:
            handle_fallback(to, chat_id)


def handle_intro(to, chat_id):
    body = INTRO_BODY
    Responder.send_text_response(to, chat_id, body)


def handle_start_quiz(to, chat_id):
    body = 'start quiz'

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[]
            )
        ])
    return Response(status=200)


def handle_custom_track(to, chat_id):
    body = 'custom track'

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=[TextResponse(body=sr) for sr in suggested_responses.grouped_srs['main_srs']])]
            )
        ])
    return Response(status=200)


def handle_share(to, chat_id):
    body = 'share'

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=[TextResponse(body=sr) for sr in suggested_responses.grouped_srs['main_srs']])]
            )
        ])
    return Response(status=200)


def handle_settings(to, chat_id):
    body = 'settings'

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=[TextResponse(body=sr) for sr in suggested_responses.grouped_srs['main_srs']])]
            )
        ])
    return Response(status=200)


def handle_fallback(to, chat_id):
    body = FALLBACK_BODY

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=[TextResponse(body=sr) for sr in suggested_responses.grouped_srs['main_srs']])]
            )
        ])
    return Response(status=200)
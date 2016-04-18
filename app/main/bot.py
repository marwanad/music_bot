from flask import request, Response, redirect, url_for
from kik.messages import messages_from_json, TextMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse
from lib.sr_strings import suggested_responses
from lib.sr_matcher import sr_matcher
from . import main, kik

INTRO_BODY = 'Hi you reached the intro stage, tap a sr for more options'
FALLBACK_BODY = 'Sorry I didn\'t understand what you said'


@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, StartChattingMessage):
            url = '.intro'
        elif isinstance(message, TextMessage):
            url = sr_matcher.match_sr(message.body.lower())
        else:
            url = '.fallback'
        return redirect(url_for(url, to=message.from_user, chat_id=message.chat_id), code=302)


@main.route('/intro', methods=['GET'])
def intro():
    to = request.args.get('to')
    chat_id = request.args.get('chat_id')
    body = INTRO_BODY

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


@main.route('/start_quiz', methods=['GET'])
def start_quiz():
    to = request.args.get
    chat_id = request.args.get('chat_id')
    body = 'start quiz'

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


@main.route('/custom_track', methods=['GET'])
def custom_track():
    to = request.args.get
    chat_id = request.args.get('chat_id')
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


@main.route('/share', methods=['GET'])
def share():
    to = request.args.get
    chat_id = request.args.get('chat_id')
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


@main.route('/settings', methods=['GET'])
def settings():
    to = request.args.get
    chat_id = request.args.get('chat_id')
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

@main.route('/fallback', methods=['GET'])
def fallback():
    to = request.args.get
    chat_id = request.args.get('chat_id')
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
from flask import Blueprint, request, Response, redirect, url_for
from kik.messages import messages_from_json, TextMessage, VideoMessage, PictureMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse
from kik import KikApi, Configuration

from . import main, kik

MAIN_SR = [TextResponse(body=sr) for sr in ['Start a quiz', 'Custom track', 'Share', 'Settings']]
INTRO_BODY = 'Hi you reached the intro stage, tap a sr for more options :+1:'


@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, StartChattingMessage):
            kik.send_messages([
                PictureMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                pic_url="http://40.media.tumblr.com/108878995b5b74bb89618dab799ded58/tumblr_nzwkikqhcH1titub2o1_1280.jpg"
                )
                ])
        return Response(status=200)


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
                keyboards=[SuggestedResponseKeyboard(responses=MAIN_SR)]
            )
        ])
    return Response(status=200)


from flask import Blueprint, request, Response, redirect, url_for
from kik.messages import messages_from_json, TextMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse
import os
from kik import KikApi, Configuration

USER_NAME = os.environ["USER_NAME"]
API_KEY = os.environ["API_KEY"]
WEB_HOOK = os.environ["FLASK_WEBHOOK"]

api = Blueprint('api', __name__)
kik = KikApi(USER_NAME, API_KEY)


@api.route('/receive', methods=['POST'])
def receive():
    kik.set_configuration(Configuration(webhook=WEB_HOOK + '/receive'))
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        # if isinstance(message, StartChattingMessage):
        return redirect(url_for('.intro', to=message.from_user, chat_id=message.chat_id), code=302)
        # return Response(status=200)


@api.route('/intro', methods=['GET'])
def intro():
    to = request.args.get('to')
    chat_id = request.args.get('chat_id')
    srs = [TextResponse(body=sr) for sr in ['ABC', 'DEF', 'HIJ', 'LMN', 'OPQ', 'RST']]
    body = 'Hi you reached the intro stage, tap a sr for more options :+1:'

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=srs)]
            )
        ])
    return Response(status=200)


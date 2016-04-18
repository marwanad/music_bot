from flask import Blueprint, request, Response
from kik.messages import messages_from_json, TextMessage
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
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])

        return Response(status=200)
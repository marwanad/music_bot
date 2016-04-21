from flask import url_for
from kik.messages import TextMessage, SuggestedResponseKeyboard

from app.main.wubble import WubbleMessage
from setup import kik


class Responder(object):
    @staticmethod
    def send_text_response(to, chat_id, body, keyboards=None, hidden=False):
        message = TextMessage(to=to, chat_id=chat_id, body=body)
        message.keyboards.append(
            SuggestedResponseKeyboard(
                to=to,
                hidden=hidden,
                responses=keyboards
            )
        )

        kik.send_messages([
            message
        ])

    @staticmethod
    def send_wubble_response(to, chat_id, song):
        kik.send_messages([
            WubbleMessage(
                to=to,
                chat_id=chat_id,
                width=130,
                height=143,
                url=url_for("main.music_player", id=song.preview_id, _external=True)
            )
        ])

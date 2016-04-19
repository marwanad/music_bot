from kik.messages import TextMessage

from setup import kik


class Responder(object):
    @staticmethod
    def send_text_response(body, to, chat_id, keyboards=None):
        kik.send_messages([
            TextMessage(to=to, chat_id=chat_id, body=body, keyboards=keyboards)
        ])

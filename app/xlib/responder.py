from kik.messages import TextMessage, SuggestedResponseKeyboard

from setup import kik


class Responder(object):
    @staticmethod
    def send_text_response(to, chat_id, body, keyboards=None):
        message = TextMessage(to=to, chat_id=chat_id, body=body)
        message.keyboards.append(
            SuggestedResponseKeyboard(
                to=to,
                hidden=False,
                responses=keyboards
            )
        )
        kik.send_messages([
            message
        ])

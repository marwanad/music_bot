from kik.messages import TextMessage, SuggestedResponseKeyboard

from setup import kik


class Responder(object):
    @staticmethod
    def send_text_response(body, to, chat_id, keyboards=[]):
    	message = TextMessage(to=to, chat_id=chat_id, body=body)
    	# message.keyboards.append(SuggestedResponseKeyboard(
    	# 	to=to,
    	# 	hidden=True,
    	# 	responses=keyboards))
    	kik.send_messages([message])
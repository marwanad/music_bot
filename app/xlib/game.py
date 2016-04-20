from app.xlib.states import StateType

GAMES = dict()


class Game(object):
    def __init__(self, chat_id, state=StateType.INITIAL, scores=None):
        self.chat_id = chat_id
        self.state = state
        if scores is None:
            scores = dict()
        self.scores = scores
        self.answer = None

    def set_state(self, state_type):
        self.state = state_type

    def increment_score(self, username):
        self.scores[username] = self.scores.get(username, 0) + 1

    def set_answer(self, answer):
        self.answer = answer

    @classmethod
    def get_game(cls, chat_id):
        if not GAMES.get(chat_id):
            GAMES[chat_id] = cls(chat_id)
        return GAMES[chat_id]

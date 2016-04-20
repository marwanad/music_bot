GAMES = dict()

class StateType(object):
    INITIAL = 'initial'
    START_SELECT = "start_select"
    GENRE_SELECT = "genre_select"
    ARTIST_SELECT = "artist_select"
    ANSWER_TIME = "answer_time"

class Game(object):
    def __init__(self, chat_id, state=StateType.INITIAL, scores=None):
        self.chat_id = chat_id
        self.state = state
        if scores is None:
            scores = dict()
        self.scores = scores

    def set_state(self, state_type):
        self.state = state_type

    def increment_score(self, username):
        self.scores[username] = self.scores.get(username, 0) + 1

    @classmethod
    def get_game(cls, chat_id):
        if not GAMES.get(chat_id):
            GAMES[chat_id] = cls(chat_id)
        return GAMES[chat_id]

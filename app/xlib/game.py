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
        if scores == None:
            scores = dict()
        self.scores = scores

    def setState(self, stateType):
        self.state = stateType

    def incrementScore(self, username):
        if username in self.scores:
            self.scores[username] = self.scores[username] + 1
        else:
            self.scores[username] = 1
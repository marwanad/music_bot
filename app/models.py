import json
from app import db
from sqlalchemy.dialects.postgresql import JSON


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.String, primary_key=True)
    state = db.Column(db.Text)
    song = db.Column(JSON)
    scores = db.Column(JSON)


def __init__(self, chatId, state, song=None, scores=json.dumps(dict())):
    self.id = chatId
    self.state = state
    self.song = song
    self.scores = scores


def __repr__(self):
    return '<Game state is: %r>' % self.state

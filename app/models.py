from app import db


class Game(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.String, primary_key=True)
    state = db.Column(db.String(64))
    song = db.Column(db.String(64))

    def __init__(self, chatId, state, song=None):
        self.id = chatId
        self.state = state
        self.song = song

    def __repr__(self):
        return '<Game %r>' % self.state

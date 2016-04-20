from . import db_inst

class Game(db.Model):
	__tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64), unique=True)

    def __init__(self, chatId, state):
        self.id = chatId
        self.state = state

	def __repr__(self):
		return '<Game %r>' % self.id


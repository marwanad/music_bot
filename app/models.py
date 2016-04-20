from . import db

class State(db.Model):
	__tablename__ = 'states'
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(64), unique=True)

	def __init__(self, chatId, state):
		self.id = chatId
		self.state = state

	def __repr__(self):
		return '<State %r>' % state


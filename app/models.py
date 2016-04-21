from . import db
import json

class Game(db.Model):
	__tablename__ = 'games'
	id = db.Column(db.String, primary_key=True)
	state = db.Column(db.String(64))
	song = db.Column(db.String(64))
	scores = db.Column(db.Text)

	def __init__(self, chatId, state, song=None, scores=json.dumps(dict()), difficulty=50):
		self.id = chatId
		self.state = state
		self.song = song
		self.scores = scores
		self.difficulty = difficulty
	def __repr__(self):
		return '<Game %r>' % self.state

	def __repr__(self):
		return '<Game state is: %r>' % self.state

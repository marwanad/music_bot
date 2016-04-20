from ..decorators import check_state
from app.xlib.responder import Responder
from app.xlib.game import StateType

@check_state(StateType.INITIAL)
def handle_intro(to, chat_id):
	body = 'Hi you reached the intro stage, tap a sr for more options :+1:'
	Responder.send_text_response(to, chat_id, body)

@check_state(StateType.INITIAL)
def handle_start_quiz(to, chat_id):
	body = 'Select genre, artist, or random'
	Game.get_game(chat_id).set_state(StateType.START_SELECT)
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['song_options'])

@check_state(StateType.START_SELECT)
def handle_genre(to, chat_id):
	body = 'Select a genre'
	Game.get_game(chat_id).set_state(StateType.GENRE_SELECT)
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['genre'])
	srs.register_sr('genre', 'handle_genre')

@check_state(StateType.START_SELECT)
def handle_artist(to, chat_id):
	body = 'Select an artist'
	Game.get_game(chat_id).set_state(StateType.ARTIST_SELECT)
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['artist'])

def handle_song(to, chat_id, song_id=None):
	if not song_id:
		# grab a random song id (prob from popular playlist)
		song_id = music.get_song_from_genre('pop')
		body = 'Tap song above'
		Game.get_game(chat_id).set_state(StateType.INITIAL)
		Responder.send_wubble_response(to, chat_id, song_id)
		Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

def handle_back(to, chat_id):
	body = 'Ok, heading back'
	Game.get_game(chat_id).set_state(StateType.INITIAL)
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

def handle_custom_track(to, chat_id):
	body = 'custom track'
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

def handle_share(to, chat_id):
	body = 'share'
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

def handle_settings(to, chat_id):
	body = 'settings'
	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

def handle_fallback(to, chat_id, body=None):
	if body:
		body = body.lower()
	else:
		body = 'Not a text message'

	Responder.send_text_response(to, chat_id, body, keyboards=srs.grouped_srs['menu'])

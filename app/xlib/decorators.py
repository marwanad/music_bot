from app.main.bot import Handler, get_game
from app.xlib.game import StateType

STATES = [StateType.INITIAL, StateType.ANSWER_TIME, StateType.ARTIST_SELECT, StateType.GENRE_SELECT,
          StateType.START_SELECT]


def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args):
            if get_game(args[1]).state in wargs:
                fn(*args)
            else:
                Handler.handle_fallback(*args)
            return wrapper

    return wrap

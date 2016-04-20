from xlib.game import Game
import handlers.handler

def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args):
            if Game.get_game(args[1]).state in wargs:
                fn(*args)
            else:
                handler.Handler.handle_fallback(*args)
            return wrapper

    return wrap

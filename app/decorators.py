from xlib.game import Game


def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args):
            if Game.get_game(args[1]).state in wargs:
                fn(*args)
            else:
                from handlers import handler

                handler.Handler.handle_fallback(*args)

        return wrapper

    return wrap

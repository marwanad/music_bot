from xlib.game import Game


def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args, **kwargs):
            if Game.get_game(args[1]).state in wargs:
                fn(*args, **kwargs)
            else:
                from handlers import handler

                handler.Handler.handle_fallback(*args, **kwargs)

        return wrapper

    return wrap

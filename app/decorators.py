from xlib.game import get_game


def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args, **kwargs):
            print 'ARGUMENTS: ', args
            if get_game(args[1]).state in wargs:
                fn(*args, **kwargs)
            else:
                from handlers import handler

                handler.Handler.handle_fallback(*args, **kwargs)

        return wrapper

    return wrap

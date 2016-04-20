from models import Game

def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args, **kwargs):
            print 'ARGUMENTS: ', args
            game = args[1]
            if game.state in wargs:
                fn(*args, **kwargs)
            else:
                from handlers import handler

                handler.Handler.handle_fallback(*args, **kwargs)

        return wrapper

    return wrap

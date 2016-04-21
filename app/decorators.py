from app import db

def check_state(*wargs):
    def wrap(fn):
        def wrapper(*args, **kwargs):
            game = args[1]
            print 'GAME STATE', game.state
            print 'WARGS', wargs
            if game.state in wargs:
                fn(*args, **kwargs)
                db.session.commit()
            else:
                from handlers import handler

                handler.Handler.handle_fallback(*args, **kwargs)

        return wrapper

    return wrap

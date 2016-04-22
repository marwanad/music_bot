class StateType(object):
    INITIAL = 'initial'
    GENRE_SELECT = "genre_select"
    ARTIST_SELECT = "artist_select"
    ANSWER_TIME = "answer_time"
    SETTINGS = "settings"


class StateString(object):
    INTRO = 'Welcome to MusIQ! How well do you know your music? I send you music clips, and you guess the song name. ;)'
    GENRE = 'Select or type a genre'
    ARTIST = 'Select or type an artist'
    BACK = 'Ok, heading back to main menu'
    DIFFICULTY = 'Select your difficulty'
    SCORE = 'Score: \n'
    ERROR = 'Uh oh something went wrong, try again?'
    FALLBACK_STRINGS = ['Not a text message', 'Wait, why would you send me this?', 'I don\'t understand what you said']
    CORRECT = ['Correct!', 'Awesome!', 'Yeeeeee bro']
    INCORRECT = ['Incorrect', 'Wrong answer', 'Nope!', 'Nah bro.']

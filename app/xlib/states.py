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
    CORRECT = ['Correct!', 'You smart', 'You a genius!', 'Slayyy', 'Yassss', 'Feel blessed']
    CORRECT_EMOJI = [u'\U0001F525' + u'\U0001F525' + u'\U0001F525', u'\U0001F511',
                     u'\U0001F4AF', u'\U0001F44C', u'\U0001F44F', u'\U0001F606', u'\U0001F4AA', u'\U0001F44D']
    INCORRECT = ['Incorrect', 'Umm... no', 'You goofed', 'Nope',
                 'Congratulations ... You played yourself']
    INCORRECT_EMOJI = [u'\U0001F4A9', u'\U0001F3FB', u'\U0001F44E', u'\U0001F649', u'\U0001F622', u'\U0001F61F']

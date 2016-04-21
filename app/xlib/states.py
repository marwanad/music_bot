class StateType(object):
    INITIAL = 'initial'
    START_SELECT = "start_select"
    GENRE_SELECT = "genre_select"
    ARTIST_SELECT = "artist_select"
    ANSWER_TIME = "answer_time"


class StateString(object):
    INTRO = 'Hi you reached the intro stage, tap a sr for more options'
    START_QUIZ = 'Select genre, artist, or random'
    GENRE = 'Select or type a genre'
    ARTIST = 'Select or type an artist'
    SONG = 'Tap song above. Answer below'
    BACK = 'Ok, heading back'
    SHARE = 'Share'
    SETTINGS = 'Settings'
    SCORE = 'Score: \n'
    ERROR = 'Seems like I can\'t fetch that right now, headed back'

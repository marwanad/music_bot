class StateType(object):
    INITIAL = 'initial'
    START_SELECT = "start_select"
    GENRE_SELECT = "genre_select"
    ARTIST_SELECT = "artist_select"
    ANSWER_TIME = "answer_time"
    SETTINGS = "settings"
    DIFFICULTY = "difficulty"


class StateString(object):
    INTRO = 'Welcome to MusIQ! How well do you know your music? I send you music clips, and you guess the song name. ;)'
    START_QUIZ = 'Do you want to be quizzed by genre, artist, or just a random song?'
    GENRE = 'Select or type a genre'
    ARTIST = 'Select or type an artist'
    BACK = 'Ok, heading back to main menu'
    DIFFICULTY = 'Select your difficulty'
    SCORE = 'Score: \n'
    ERROR = 'Seems like I can\'t fetch that right now, going back to main menu'

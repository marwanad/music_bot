from kik.messages import TextResponse

from app.xlib.states import StateType


class SuggestedResponses(object):
    def __init__(self):
        self.srs = dict()
        self.grouped_srs = dict()

    def register_sr(self, name, fn):
        if isinstance(name, str):
            self.srs[name] = fn
        else:
            for key in name:
                self.srs[key] = fn

    def register_group_sr(self, name, sr_names):
        self.grouped_srs[name] = [TextResponse(sr) for sr in sr_names]

    def match_group_sr(self, group_sr, message):
        return message in map(lambda x: x.body.lower(), self.grouped_srs[group_sr])

srs = SuggestedResponses()

srs.register_sr('scores', 'handle_score')
srs.register_sr('set difficulty', 'handle_settings')
srs.register_sr('genre', 'handle_genre')
srs.register_sr('artist', 'handle_artist')
srs.register_sr('random', 'handle_song')
srs.register_sr('back', 'handle_back')
srs.register_sr('hint', 'handle_hint')
srs.register_sr(['easy', 'medium', 'hard'], 'handle_difficulty')

srs.register_group_sr(StateType.INITIAL, ['Random', 'Genre', 'Artist', 'Scores', 'Set Difficulty'])
srs.register_group_sr(StateType.GENRE_SELECT, ['Pop', 'Hip-Hop', 'Electro', 'Jazz', 'Rock', 'Disney', 'Country', 'R-n-B', 'Back'])
srs.register_group_sr(StateType.ARTIST_SELECT, ['Drake', 'Taylor Swift', 'Zayn', 'Kanye West', 'Beyonce', 'Adele', 'Coldplay', 'Back'])
srs.register_group_sr(StateType.ANSWER_TIME, ['Hint', 'Back'])
srs.register_group_sr(StateType.SETTINGS, ['Easy', 'Medium', 'Hard'])

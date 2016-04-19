from kik.messages import TextResponse

class SuggestedResponses(object):
    def __init__(self):
        self.srs = dict()
        self.grouped_srs = dict()

    def register_sr(self, name, fn):
        self.srs[name] = fn

    def register_group_sr(self, name, sr_names):
        self.grouped_srs[name] = [TextResponse(sr) for sr in sr_names]


srs = SuggestedResponses()

srs.register_sr('start a quiz', 'handle_start_quiz')
srs.register_sr('custom track', 'handle_custom_track')
srs.register_sr('share', 'handle_share')
srs.register_sr('settings', 'handle_settings')
srs.register_sr('genre', 'handle_genre')
srs.register_sr('artist', 'handle_artist')
srs.register_sr('random', 'handle_song')
srs.register_sr('skip', 'handle_skip')


srs.register_group_sr('menu', ['Start a quiz', 'Custom track', 'Share', 'Settings'])
srs.register_group_sr('song_options', ['Genre', 'Artist', 'Random'])
srs.register_group_sr('genre', ['Pop', 'Hip-Hop', 'Electro', 'Jazz', 'Rock', 'Disney', 'Country', 'R-n-B'])
srs.register_group_sr('artist', ['Drake', 'Kanye', 'Kendrick', 'Perry', 'Nas', 'Tupac'])
srs.register_group_sr('skip', ['Skip'])


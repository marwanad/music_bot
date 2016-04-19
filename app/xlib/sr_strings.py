from kik.messages import SuggestedResponseKeyboard, TextResponse

class SuggestedResponses(object):
    def __init__(self):
        self.srs = dict()
        self.grouped_srs = dict()

    def register_sr(self, name, fn):
        self.srs[name] = fn

    def register_group_sr(self, name, sr_names):
        self.grouped_srs[name] = SuggestedResponseKeyboard(responses=[TextResponse(body=sr) for sr in sr_names])


srs = SuggestedResponses()

srs.register_sr('Start a quiz', 'handle_start_quiz')
srs.register_sr('Custom track', 'handle_custom_track')
srs.register_sr('Share', 'handle_share')
srs.register_sr('Settings', 'handle_settings')

srs.register_group_sr('main_srs', ['Start a quiz', 'Custom track', 'Share', 'Settings'])

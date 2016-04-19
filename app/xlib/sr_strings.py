class SuggestedResponses(object):
    def __init__(self):
        self.srs = dict()
        self.grouped_srs = dict()
        self.inv_srs = dict()

    def register_sr(self, name, sr):
        self.srs[name] = sr

    def register_group_sr(self, name, sr_names):
        self.grouped_srs[name] = [self.srs[sr_name] for sr_name in sr_names]

    def generate_inverse_srs(self):
        self.inv_srs = {v: k for k, v in self.srs.items()}


suggested_responses = SuggestedResponses()

suggested_responses.register_sr('start_quiz', 'Start a quiz')
suggested_responses.register_sr('custom_track', 'Custom track')
suggested_responses.register_sr('share', 'Share')
suggested_responses.register_sr('settings', 'Settings')

suggested_responses.register_group_sr('main_srs', ['start_quiz', 'custom_track', 'share', 'settings'])

suggested_responses.generate_inverse_srs()
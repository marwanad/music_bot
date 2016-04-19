from sr_strings import suggested_responses

class SR_Matcher(object):
    def match_sr(self, body):
        name = suggested_responses.inv_srs.get('name')
        if name:
            return '.{}'.format(name)
        else:
            return '.fallback'

sr_matcher = SR_Matcher()

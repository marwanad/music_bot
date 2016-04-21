import string
import re
from fuzzywuzzy import fuzz

def guess_matches_answer(guess, answer):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    guess_no_punc = regex.sub('', guess).strip().lower()
    guess_no_dash = guess_no_punc.split('-')[0]
    answer_no_punc = regex.sub('', answer).strip().lower()
    return fuzz.ratio(guess_no_dash, answer_no_punc) >= 95


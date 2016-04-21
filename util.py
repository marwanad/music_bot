import string
import re


def guess_matches_answer(guess, answer):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    guess_no_punc = regex.sub('', guess).strip().lower()
    answer_no_punc = regex.sub('', answer).strip().lower()
    return guess_no_punc == answer_no_punc


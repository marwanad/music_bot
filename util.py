import string

def guess_matches_answer(guess, answer):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    guess_no_punc = guess.translate(string.maketrans("", ""), remove_punctuation_map).strip().lower()
    answer_no_punc = answer.translate(string.maketrans("", ""), remove_punctuation_map).strip().lower()
    return guess_no_punc == answer_no_punc
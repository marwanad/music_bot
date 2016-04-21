import string

def guess_matches_answer(guess, answer):
    guess_no_punc = guess.translate(string.maketrans("", ""), string.punctuation).strip().lower()
    answer_no_punc = answer.translate(string.maketrans("", ""), string.punctuation).strip().lower()
    return guess == answer_no_punc

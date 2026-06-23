import numpy as np

"""
Shared Class between playWordle and solveWordle that contains the scoring of a guess against a word.
Score codes per letter: 0 = grey (not in word), 1 = yellow (wrong position), 2 = green (correct position).
"""


def evaluateGuess(guess, answer):
    """
    Score guess against answer.
    Returns a per-letter list [[letter, code], ...].
    """
    score = [[letter, 0] for letter in guess]
    answerRemaining = answer
    guessRemaining = guess

    # Green: correct letter in the correct position.
    for index in range(len(guess)):
        if guessRemaining[index] == answerRemaining[index]:
            score[index][1] = 2
            answerRemaining = answerRemaining[:index] + "_" + answerRemaining[index + 1:]
            guessRemaining = guessRemaining[:index] + "_" + guessRemaining[index + 1:]

    # Yellow: correct letter, wrong position — consume one unmatched copy.
    for index in range(len(guess)):
        if guessRemaining[index] != "_" and guessRemaining[index] in answerRemaining:
            score[index][1] = 1
            answerRemaining = answerRemaining.replace(guessRemaining[index], "_", 1)
            guessRemaining = guessRemaining[:index] + "_" + guessRemaining[index + 1:]

    # Remaining letters stay grey (0).
    return score


def encode(score):
    """
    Collapse a score list into the compact code string, e.g. "10221".
    """
    return "".join(str(code) for _, code in score)


def load_words(path):
    """
    Load a one-word-per-line word list as a numpy string array.
    """
    return np.loadtxt(path, dtype=str)

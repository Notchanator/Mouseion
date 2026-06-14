"""Shared, stateless Wordle scoring kernel.

Both roles import from here so the scoring rule lives in exactly one place:
the game host (``wordle.py``) scores the player's guess against its secret word,
and the solver (``solveWordle.py``) scores hypothetical answers to reason about
candidates. No game or solver state, no tkinter — pure functions only.

Score codes per letter: 0 = grey (not in word), 1 = yellow (wrong position),
2 = green (correct position).
"""

import numpy as np


def evaluateGuess(guess, answer):
    """Score ``guess`` against ``answer``.

    Returns a per-letter list ``[[letter, code], ...]``. Duplicate letters are
    handled by consuming one matching letter from the answer per green/yellow,
    so a guessed letter is only marked yellow while unmatched copies remain.
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
    """Collapse a score list into the compact code string, e.g. ``"10221"``."""
    return "".join(str(code) for _, code in score)


def load_words(path):
    """Load a one-word-per-line word list as a numpy string array."""
    return np.loadtxt(path, dtype=str)

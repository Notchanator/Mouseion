"""Wordle solver — suggests guesses and narrows the answer from reported scores.

Companion to the playable game. The player is the oracle: the solver proposes a
word, the player reports the real game's evaluation as a 5-char code string
(0 = grey, 1 = yellow, 2 = green, e.g. "10221"), and the solver discards every
candidate answer that could not have produced that report.

The expensive first turn is skipped by hard-coding the opener (conf.SOLVER), so
entropy is only ever computed over the surviving candidate set — never the full
dictionary.

    1. Suggest a word (opener on turn 1, else the highest-entropy survivor).
    2. Read the reported score.
    3. Subset candidates to those consistent with that score.
    4. Repeat until one candidate remains (or the player reports a win).
"""

import numpy as np

import scoring
from conf import DATA, SOLVER


class WordleSolver:
    def __init__(self):
        self.candidates = scoring.load_words(DATA["answers"])
        self.turn = 0

    @property
    def solved(self):
        return len(self.candidates) == 1

    def suggest(self):
        """Next word to guess: the fixed opener on turn 0, else the survivor that
        most evenly splits the remaining candidates (highest entropy)."""
        if self.turn == 0:
            return SOLVER["opener"]
        return max(self.candidates, key=self._entropy)

    def record(self, guess, code):
        """Keep only candidates whose score against ``guess`` matches the reported
        ``code``, then advance the turn."""
        self.candidates = np.array([
            answer for answer in self.candidates
            if scoring.encode(scoring.evaluateGuess(guess, answer)) == code
        ])
        self.turn += 1

    def _entropy(self, guess):
        """Expected information (bits) from guessing ``guess`` against the current
        candidates: partition them by the score they'd yield, then H = -Σ pᵢ·log₂ pᵢ."""
        partitions = {}
        for answer in self.candidates:
            code = scoring.encode(scoring.evaluateGuess(guess, answer))
            partitions[code] = partitions.get(code, 0) + 1
        probs = np.array(list(partitions.values())) / len(self.candidates)
        return float(-(probs * np.log2(probs)).sum())


def main():
    solver = WordleSolver()
    print("Wordle solver — report each guess's score as a 5-char code:")
    print("  0 = grey, 1 = yellow, 2 = green   (e.g. 10221)")
    print("  Type 'done' if the suggested word was the answer.\n")

    while True:
        guess = solver.suggest()
        print(f"Turn {solver.turn + 1}: guess  ->  {guess}")
        code = input("Score (or 'done'): ").strip().lower()

        if code == "done":
            print(f"\nSolved: {guess}")
            return
        if len(code) != 5 or any(c not in "012" for c in code):
            print("  Invalid score — use 5 characters, each 0/1/2.\n")
            continue

        solver.record(guess, code)

        if solver.solved:
            print(f"\nThe word is: {solver.candidates[0]}")
            return
        if len(solver.candidates) == 0:
            print("\nNo candidates remain — double-check the reported scores.")
            return
        print(f"  {len(solver.candidates)} candidates remain.\n")


if __name__ == "__main__":
    main()

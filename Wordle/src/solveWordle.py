from conf import DATA, SOLVER
import scoring

import numpy as np

"""
CLI that interacts with you to solve the Wordle.

Report the score of each word using code like:
    0 = grey, 1 = yellow, 2 = green; e.g. "10221"
This will then return the next most optimal word to guess.
"""


class WordleSolver:
    def __init__(self):
        self.candidates = scoring.load_words(DATA["answers"])
        self.turn = 0

    @property
    def solved(self):
        return len(self.candidates) == 1

    def suggest(self):
        """
        Next word to guess: the fixed opener on turn 0, else the survivor that has the highest entropy.
        """
        if self.turn == 0:
            return SOLVER["opener"]
        return max(self.candidates, key=self._entropy)

    def record(self, guess, code):
        """
        Keep only candidates whose score against guess matches the reported code, then advance the turn.
        """
        self.candidates = np.array([
            answer for answer in self.candidates
            if scoring.encode(scoring.evaluateGuess(guess, answer)) == code
        ])
        self.turn += 1

    def _entropy(self, guess):
        """
        Expected information from guessing each guess against the current candidates. 
        Partition them by the score they'd yield, then H = -Σ pᵢ·log₂ pᵢ."""
        partitions = {}
        for answer in self.candidates:
            code = scoring.encode(scoring.evaluateGuess(guess, answer))
            partitions[code] = partitions.get(code, 0) + 1
        probs = np.array(list(partitions.values())) / len(self.candidates)
        return float(-(probs * np.log2(probs)).sum())


def main():
    solver = WordleSolver()
    print("Wordle Solver: Report each guess's score as a 5-char code:")
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
            print("  Invalid score: Use 5 characters, each 0/1/2.\n")
            continue

        solver.record(guess, code)

        if solver.solved:
            print(f"\nThe word is: {solver.candidates[0]}")
            return
        if len(solver.candidates) == 0:
            print("\nNo candidates remain: Double-check the reported scores.")
            return
        print(f"  {len(solver.candidates)} candidates remain.\n")


if __name__ == "__main__":
    main()

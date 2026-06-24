class Statistics:
    """
    Tracks game outcomes across multiple Wordle rounds.
    """
    LOSS = 0
    MIN_GUESSES = 1
    MAX_GUESSES = 6

    def __init__(self):
        self.distribution = {self.LOSS: 0}
        for guesses in range(self.MIN_GUESSES, self.MAX_GUESSES + 1):
            self.distribution[guesses] = 0

    def recordWin(self, guesses):
        """
        Record a win achieved in the given number of guesses.
        """
        if not self.MIN_GUESSES <= guesses <= self.MAX_GUESSES:
            raise ValueError(f"guesses must be {self.MIN_GUESSES}-{self.MAX_GUESSES}, got {guesses}")
        self.distribution[guesses] += 1

    def recordLoss(self):
        """
        Record a lost game
        """
        self.distribution[self.LOSS] += 1

    def gamesPlayed(self):
        return sum(self.distribution.values())

    def gamesWon(self):
        return sum(count for guesses, count in self.distribution.items() if guesses != self.LOSS)

    def gamesLost(self):
        return self.distribution[self.LOSS]

    def winPercentage(self):
        if self.gamesPlayed() == 0:
            return 0
        return round(100 * self.gamesWon() / self.gamesPlayed())

    def guessDistribution(self):
        """
        Win counts keyed by guess number (1-6), excluding losses.
        """
        return {guesses: count for guesses, count in self.distribution.items() if guesses != self.LOSS}

    def __str__(self):
        lines = [
            f"Played: {self.gamesPlayed()}",
            f"Won: {self.gamesWon()}  ({self.winPercentage()}%)",
            f"Lost: {self.gamesLost()}",
        ]
        for guesses, count in self.guessDistribution().items():
            lines.append(f"  {guesses}: {count}")
        return "\n".join(lines)

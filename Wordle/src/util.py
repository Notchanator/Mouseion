class Statistics:
    """
    Tracks game outcomes across multiple Wordle rounds.

    A game is either won in 1-6 guesses or lost. The distribution maps a
    guess count (1-6) to the number of wins achieved in that many guesses,
    with key 0 reserved for losses.

    This object is intended to outlive any single Wordle game — it is owned
    by the App and persists for the whole session, accumulating results as
    rounds complete.
    """
    LOSS = 0
    MIN_GUESSES = 1
    MAX_GUESSES = 6

    def __init__(self):
        self.distribution = {self.LOSS: 0}
        for guesses in range(self.MIN_GUESSES, self.MAX_GUESSES + 1):
            self.distribution[guesses] = 0

    def recordWin(self, guesses):
        """Record a win achieved in the given number of guesses (1-6)."""
        if not self.MIN_GUESSES <= guesses <= self.MAX_GUESSES:
            raise ValueError(f"guesses must be {self.MIN_GUESSES}-{self.MAX_GUESSES}, got {guesses}")
        self.distribution[guesses] += 1

    def recordLoss(self):
        """Record a lost game."""
        self.distribution[self.LOSS] += 1

    @property
    def gamesPlayed(self):
        return sum(self.distribution.values())

    @property
    def gamesWon(self):
        return sum(count for guesses, count in self.distribution.items() if guesses != self.LOSS)

    @property
    def gamesLost(self):
        return self.distribution[self.LOSS]

    @property
    def winPercentage(self):
        if self.gamesPlayed == 0:
            return 0
        return round(100 * self.gamesWon / self.gamesPlayed)

    @property
    def guessDistribution(self):
        """Win counts keyed by guess number (1-6), excluding losses."""
        return {guesses: count for guesses, count in self.distribution.items() if guesses != self.LOSS}

    def __str__(self):
        lines = [
            f"Played: {self.gamesPlayed}",
            f"Won: {self.gamesWon}  ({self.winPercentage}%)",
            f"Lost: {self.gamesLost}",
        ]
        for guesses, count in self.guessDistribution.items():
            lines.append(f"  {guesses}: {count}")
        return "\n".join(lines)

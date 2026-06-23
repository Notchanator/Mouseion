import scoring
from conf import DATA


import numpy as np

"""
This file is a script for a CLI interfact to the game.

Houses the Wordle game logic for the GUI game in playWordle.
"""

class Wordle:
    def __init__(self, DATA, wordFileName=None, usedWords=[]):
        if wordFileName is None:
            wordFileName = DATA["guesses"]
        self.allWords = scoring.load_words(wordFileName)
        self.possibleAnswers = scoring.load_words(DATA["answers"])
        self.turn = 0
        self.finished = False
        self.wordBank = {"a":-1, "b":-1, "c":-1, "d":-1, "e":-1, "f":-1, "g":-1, "h":-1, "i":-1, "j":-1, "k":-1, "l":-1, "m":-1, "n":-1, "o":-1, "p":-1, "q":-1, "r":-1, "s":-1, "t":-1, "u":-1, "v":-1, "w":-1, "x":-1, "y":-1, "z":-1}
        self.theWord = self.generateWord(usedWords)

    def playGame(self):
        while not self.finished:   
            self.getUserWord()
            if self.userWord is None:
                return None
            score = self.evaluateGuess()
            print(score)
            self.updateWordBank(score)
            self.turn += 1
            self.finished = self.evaluateEnding()
        return self.theWord


    def generateWord(self, usedWords):
        leftoverWords = np.setdiff1d(self.possibleAnswers, usedWords)
        return(np.random.choice(leftoverWords, 1)[0])

    def getUserWord(self):
        while True:
            userWord = input("Guess:").lower()
            if userWord == "quit" or userWord == "q":
                self.finished = True
                self.userWord = None
                return
            if np.isin(userWord, self.allWords):
                self.userWord = userWord
                return
            print("INVALID WORD")

    def testUserWord(self, userWord):
        return np.isin(userWord, self.allWords)


    def evaluateGuess(self):
        # Shared scoring rule — see scoring.py (same rule the solver reasons with).
        return scoring.evaluateGuess(self.userWord, self.theWord)

    def printCorrectLetters(self):
        correctLetters = self.findCorrectLetters()
        formatLetters = [letter if letter in correctLetters else "_" for letter in self.theWord]
        print(*formatLetters, sep=" ", end="  |  ")

    def printSemiCorrectLetters(self):
        semiCorrectLetters = self.findSemiCorrectLetters()
        print(*semiCorrectLetters, sep=" ", end="\n\n")
        
    def evaluateEnding(self):
        if self.userWord == self.theWord:
            print("\nYOU WIN\n")
            return True
        if self.turn == 6:
            print("\n"+self.theWord)
            print("\nNICE TRY\n")
            return True 

    def updateWordBank(self, score):
        for index in range(len(score)):
            self.wordBank[score[index][0]] = max(self.wordBank[score[index][0]], score[index][1])


def programBody(usedWords):
    wordle = Wordle(DATA, usedWords=usedWords)
    return(wordle.playGame())


if __name__ == "__main__":
    usedWords = []
    while True:
        usedWords.append(programBody(usedWords))
        if len(usedWords) > 0 or usedWords[len(usedWords) - 1] is None:
            exit()

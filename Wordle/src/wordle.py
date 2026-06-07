import numpy as np
from pathlib import Path

class Wordle:
    def __init__(self, wordFileName=None, usedWords=[]):
        if wordFileName is None:
            wordFileName =  "/Users/notchjohnson/Mouseion/Mouseion/Wordle/data/wordle_guesses.csv"
        self.allWords = np.loadtxt(wordFileName, dtype=str)
        self.possibleAnswers = np.loadtxt("/Users/notchjohnson/Mouseion/Mouseion/Wordle/data/wordle_answers.csv", dtype=str)
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


    ## Iterate Through it all once
    ## Pick out the greens and then go through the yellows
    def evaluateGuess(self):
        score = [[letter, 0] for letter in self.userWord]
        tempWord = self.theWord
        tempUserWord = self.userWord
        for index in range(len(self.userWord)):
            if tempUserWord[index] == self.theWord[index]:
                score[index][1] = 2
                tempWord = tempWord.replace(score[index][0], "_", 1)
                tempUserWord = tempUserWord.replace(score[index][0], "_", 1)
        for index in range(len(tempUserWord)):
                if tempUserWord[index] != "_" and tempUserWord[index] in tempWord:
                    score[index][1] = max(1, score[index][1])
                    tempWord = tempWord.replace(score[index][0], "_", 1)
                    tempUserWord = tempUserWord.replace(score[index][0], "_", 1)
        for index in range(len(tempUserWord)):
            if tempUserWord[index] != "_":
                score[index][1] = max(0, score[index][1])
        return score

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
    wordle = Wordle(usedWords=usedWords)
    return(wordle.playGame())


usedWords = []
while True:
    usedWords.append(programBody(usedWords))
    if len(usedWords) > 0 or usedWords[len(usedWords) - 1] is None:
        exit()

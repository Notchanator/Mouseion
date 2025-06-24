import numpy as np
import pandas as pd
import sys

# This script is meant as an aide to the actual Wordle application. Start without any guesses
# and it will recommend a starting word then input the results to find the final word.

# Inputs: "apple" "10021" | "a" and "e" are yellow, "l" is green

"""
Workflow:
1. Prompt for # of current guesses
    a. Prompt for word
    b. Prompt for scoring
    c. Repeat for all guesses
2. Run Wordle w/ Used Words
3. Call functions to score and subset possible answers.
4. Output suggestion with highest entropy
5. Prompt for scoring or success
6. Repeat steps 3, 4, and 5.
"""

## For now let's define a new Wordle Class since we need to utilize it differently.
# TODO: Refactor the wordle classes into one.

class Wordle:
      
    possibleAnswers = np.loadtxt("wordle_answers.csv", dtype=str)
    allWords = np.loadtxt("wordle_guesses.csv", dtype=str)
    turn = 0
    wordBank = {"a":-1, "b":-1, "c":-1, "d":-1, "e":-1, "f":-1, "g":-1, "h":-1, "i":-1, "j":-1, "k":-1, "l":-1, "m":-1, "n":-1, "o":-1, "p":-1, "q":-1, "r":-1, "s":-1, "t":-1, "u":-1, "v":-1, "w":-1, "x":-1, "y":-1, "z":-1}

    def __init__(self, usedWords=[], usedWordsScore=[]):
        self.usedWords = usedWords
        self.usedWordsScore = usedWordsScore
        for word in usedWords:
            turn += 1
            # TODO: Confirm that this logic works for an empty list.

    def createAnswersDF(self, numpyList):
        # TODO: Create this function. It should make each value in the numpy list a new row. Each
        # column will represent a letter of the word. 
        return pd.DataFrame(numpyList)


    # To subset all answers & guesses by current scores.
    def subsetAllWords(self, usedWord, usedWordScore):
        # TODO an excpetion for duplicate letters in the word. 
        for index in range(len(usedWord)):
            # If Grey remove all words that contain any of that letter.
            if usedWordScore[index] == 0:
                pass
            # If Yellow remove all words 
            elif usedWordScore[index] == 1:
                pass
            # If Green.
            elif usedWordScore[index] == 2:
                pass
            else:
                raise Exception(f"Invalid Score for {usedWord}")

            
    def subsetUsedWords(self):
        for index, word in enumerate(self.usedWords):
            self.subsetAllWords(word, self.usedWordsScore[index])

    def subsetNewWord(self, word, wordScore):
        self.subsetAllWords(word, wordScore)
        self.turn += 1

    def suggestWord(self):
        # TODO: Create this function. This can closely model the WordleBot in the notebook.
        return "Apple"

    


# Prompt # of current guesses.
guessCount = input("Number of guesses already done:")
try:
    guessCount = int(guessCount)
except:
    raise TypeError
usedWords = []
usedWordsScore = []
for guess in range(0, guessCount):
    usedWords.append(input("Guess:").lower())
    if guess == 1 :
        print("Input Scores like 01021. Where 1 represents Yellow and 2 represents Green.")
    usedWordsScore.append(input("Score:"))
wordle = Wordle(usedWords=usedWords)
wordle.subsetUsedWords()
solved = False
while not solved:
    suggestedWord = wordle.suggestWord()
    print(f"Suggested Word: {suggestedWord}")
    score = input("How did that word score. If it was the word type 'Done'")
    if score == 'Done':
        solved = True
    else:
        wordle.subsetNewWord(suggestedWord, score)





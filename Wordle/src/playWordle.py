from wordle import Wordle
from util import Statistics
from keyboard import Keyboard
from toolbar import Toolbar
from buttons import HowToButton, StatisticsButton
from conf import (
    WINDOW, 
    CANVAS, 
    TILE, 
    SCORE_COLORS,
    END_BANNER,
    DATA
)

import numpy as np
import tkinter as tk

"""
Runable Script to Play Wordle.

Houses Main Class for the GUI of the Wordle Game
"""


class App(tk.Canvas):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.gridRectangles = [[], [], [], [], [], []]
        self.gridLetters = [[], [], [], [], [], []]
        self.keyboard = Keyboard(self)
        self.row = 0
        self.col = 0
        self.winnerBanner = []
        self.loserBanner = []
        self.usedWords = []
        self.guessWord = None
        self.stats = Statistics()
    
    def startWordle(self, usedWords = []):
        self.wordle = Wordle(DATA=DATA, usedWords=usedWords)
        print(self.wordle.theWord, end='\n')

    def setup(self):
        self.createTiles()
        self.keyboard.draw()

    def createTiles(self):
        """
        Creates the tile spaces where all of the guesses are shown.
        """
        x0, y0, step, size = TILE["x_offset"], TILE["y_offset"], TILE["step"], TILE["size"]
        for row in range(TILE["rows"]):
            for col in range(TILE["cols"]):
                self.gridRectangles[row].append(self.create_rectangle(
                    x0 + step*col,
                    y0 + step*row,
                    x0 + step*col + size,
                    y0 + step*row + size,
                    outline=TILE["outline"],
                ))
                self.gridLetters[row].append(self.create_text(
                    x0 + step*col + size//2,
                    y0 + step*row + size//2,
                    text="",
                    font=TILE["font"],
                ))
    
    def clearTiles(self):
        for row in range(6):
            for col in range(5):
                self.delete(self.gridRectangles[row][col])
                self.delete(self.gridLetters[row][col])

    def letterTyped(self, event):
        """
        When a letter is typed place it the correct tile. If all tiles are full test the word.
        """
        letter = event.char.upper()
        if letter in self.keyboard.letters:
            self.writeLetter(letter)
        if self.col == 5:
            self.guessWord = self.createWord().lower()
            if not self.wordle.testUserWord(self.guessWord):
                self.redrawCurrentRow(fill=TILE["invalid_color"])

    def writeLetter(self, letter):
        if self.col < 5:
            self.itemconfigure(self.gridLetters[self.row][self.col], text=letter)
            self.col += 1
    
    def deleteLetter(self, event):
        if self.col == 5:
            self.redrawCurrentRow()
        if self.col > 0:
            self.col -= 1
            self.itemconfig(self.gridLetters[self.row][self.col], text="")

    def updateRectangles(self, score):
        """
        Update the tile spaces that contain letters to reflect the correct colors post scoring.
        """
        for rect in range(TILE["cols"]):
            fill = SCORE_COLORS.get(score[rect][1], SCORE_COLORS[0])
            self.itemconfigure(self.gridRectangles[self.row][rect], fill=fill)
    
    def clearBoard(self):
        if len(self.winnerBanner) == 2:
            self.delete(self.winnerBanner[0])
            self.delete(self.winnerBanner[1])
            self.winnerBanner = []
        if len(self.loserBanner) == 2:
            self.delete(self.loserBanner[0])
            self.delete(self.loserBanner[1])
            self.loserBanner = []

        self.clearTiles()
        self.keyboard.clear()

        self.gridRectangles = [[], [], [], [], [], []]
        self.gridLetters = [[], [], [], [], [], []]
        self.row = 0
        self.col = 0

        self.setup()


    def guessMade(self):
        score = self.wordle.evaluateGuess()
        self.updateRectangles(score)
        self.wordle.updateWordBank(score)
        self.keyboard.update(self.wordle.wordBank)

    def redrawCurrentRow(self, fill="black"):
        """
        Redraw the current row's letters.
        """
        x0, y0, step, size = TILE["x_offset"], TILE["y_offset"], TILE["step"], TILE["size"]
        for i in range(TILE["cols"]):
            self.delete(self.gridLetters[self.row][i])
            self.gridLetters[self.row][i] = self.create_text(
                x0 + step*i + size//2,
                y0 + step*self.row + size//2,
                text=self.guessWord[i].upper(),
                font=TILE["font"],
                fill=fill,
            )

    def wonGame(self):
        possiblePhrases = np.array(END_BANNER["text"])
        phrase = np.random.choice(possiblePhrases, 1)[0]
        self.winnerBanner.append(self.create_rectangle(
            END_BANNER["x0"], END_BANNER["y0"], END_BANNER["x1"], END_BANNER["y1"], fill=END_BANNER["fill"],
        ))
        self.winnerBanner.append(self.create_text(
            END_BANNER["cx"], END_BANNER["cy"], text=phrase, fill=END_BANNER["text_color"], font=END_BANNER["font"],
        ))
        self.stats.recordWin(self.row + 1)
        self.wordle.finished = True

    def lostGame(self):
        self.loserBanner.append(self.create_rectangle(
            END_BANNER["x0"], END_BANNER["y0"], END_BANNER["x1"], END_BANNER["y1"], fill=END_BANNER["fill"],
        ))
        self.loserBanner.append(self.create_text(
            END_BANNER["cx"], END_BANNER["cy"], text=self.wordle.theWord.upper(), fill=END_BANNER["text_color"], font=END_BANNER["font"],
        ))
        self.stats.recordLoss()
        self.wordle.finished = True

    def createWord(self):
        letters = []
        for i in range(5):
            letters.append(self.itemcget(self.gridLetters[self.row][i], "text"))
        return "".join(letters).lower()


    def enterWord(self, event):
        if self.col == 5:
            word = self.createWord()
            if self.wordle.testUserWord(word):
                self.wordle.userWord = word
                self.guessMade()
                if self.wordle.userWord == self.wordle.theWord:
                    self.wonGame()
                elif self.row == 5:
                    self.lostGame()
                else:
                    self.col = 0
                    self.row += 1

    def restartGame(self, event):
        if self.wordle.finished:
            self.usedWords.append(self.wordle.theWord)
            self.clearBoard()
            self.startWordle(usedWords=self.usedWords)


root = tk.Tk()
root.geometry(WINDOW["geometry"])
root.title(WINDOW["title"])
# Toolbar - fixed height.
root.grid_rowconfigure(0, weight=0)
# Canvas  — fills remaining space.
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

toolbar = Toolbar(root, app=None)
toolbar.register(HowToButton)
toolbar.register(StatisticsButton)

app = App(root, width=CANVAS["width"], height=CANVAS["height"], )
app.grid(row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
# Give toolbar buttons access to the game after app exists.
toolbar.app = app  
app.setup()
app.startWordle()

root.bind("<Key>", app.letterTyped)
root.bind("<BackSpace>", app.deleteLetter)
root.bind("<Return>", lambda e: (app.restartGame(e), app.enterWord(e)))
root.bind("<Button>", app.restartGame)

root.mainloop()
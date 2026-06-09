import tkinter as tk
from wordle import Wordle
from toolbar import Toolbar
from buttons import HowToButton
from conf import (
    WINDOW, 
    CANVAS, 
    TILE, 
    SCORE_COLORS, 
    ALPHABET, 
    END_BANNER, 
    DATA
)
import numpy as np


class App(tk.Canvas):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.gridRectangles = [[], [], [], [], [], []]
        self.gridAlphabet = []
        self.gridAlphabetBackground = []
        self.gridLetters = [[], [], [], [], [], []]
        self.row = 0
        self.col = 0
        self.winnerBanner = []
        self.loserBanner = []
        self.usedWords = []
        self.guessWord = None
        self.stats = {0:0, 1:0 , 2:0, 3:0, 4:0, 5:0, 6:0}
    
    def startWordle(self, usedWords = []):
        self.wordle = Wordle(DATA=DATA, usedWords=usedWords)
        print(self.wordle.theWord)

    def setup(self):
        self.createTiles()
        self.letterBank = ALPHABET["letters"]
        self.createLetters()

    def createTiles(self):
        x0, y0, step, size = TILE["x_offset"], TILE["y_offset"], TILE["step"], TILE["size"]
        for row in range(TILE["rows"]):
            for col in range(TILE["cols"]):
                self.gridRectangles[row].append(self.create_rectangle(
                    x0 + step*col, y0 + step*row,
                    x0 + step*col + size, y0 + step*row + size,
                    outline=TILE["outline"],
                ))
                self.gridLetters[row].append(self.create_text(
                    x0 + step*col + size//2, y0 + step*row + size//2,
                    text="", font=TILE["font"],
                ))
    
    def createLetters(self):
        x0, y0, ts = ALPHABET["x_offset"], ALPHABET["y_offset"], ALPHABET["tile_size"]
        for row in [0, 1]:
            for col in range(13):
                self.gridAlphabetBackground.append(self.create_rectangle(
                    x0 + ts*col, y0 + ts*row,
                    x0 + ts*col + ts, y0 + ts*row + ts,
                    outline=ALPHABET["outline"],
                ))
                self.gridAlphabet.append(self.create_text(
                    x0 + ts*col + ts//2, y0 + ts*row + ts//2,
                    text=self.letterBank[row*13 + col], font=ALPHABET["font"],
                ))

    def clearTiles(self):
        for row in range(6):
            for col in range(5):
                self.delete(self.gridRectangles[row][col])
                self.delete(self.gridLetters[row][col])
    
    def clearLetters(self):
        for row in [0,1]:
            for col in range(13):
                self.delete(self.gridAlphabetBackground[col + 13*row])
                self.delete(self.gridAlphabet[col + 13*row])
    
    def letterTyped(self, event):
        letter = event.char.upper()
        if letter in self.letterBank:
            self.writeLetter(letter)
        if self.col == 5:
            self.guessWord = self.createWord().lower()
            if not self.wordle.testUserWord(self.guessWord):
                self.badWord()

    def writeLetter(self, letter):
        if self.col < 5:
            self.itemconfigure(self.gridLetters[self.row][self.col], text=letter)
            self.col += 1
    
    def deleteLetter(self, event):
        if self.col == 5:
            self.undoBadWord()
        if self.col > 0:
            self.col -= 1
            self.itemconfig(self.gridLetters[self.row][self.col], text="")

    def updateRectangles(self, score):
        for rect in range(TILE["cols"]):
            fill = SCORE_COLORS.get(score[rect][1], SCORE_COLORS[0])
            self.itemconfigure(self.gridRectangles[self.row][rect], fill=fill)
    
    def updateAlphabet(self):
        for i in range(26):
            color = self.wordle.wordBank.get(self.letterBank[i].lower())
            if color in SCORE_COLORS:
                self.itemconfig(self.gridAlphabetBackground[i], fill=SCORE_COLORS[color])
    
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
        self.clearLetters()

        self.gridRectangles = [[], [], [], [], [], []]
        self.gridAlphabet = []
        self.gridAlphabetBackground = []
        self.gridLetters = [[], [], [], [], [], []]
        self.row = 0
        self.col = 0

        self.setup()


    def guessMade(self):
        score = self.wordle.evaluateGuess()
        self.updateRectangles(score)
        self.wordle.updateWordBank(score)
        self.updateAlphabet()

    def badWord(self):
        x0, y0, step, size = TILE["x_offset"], TILE["y_offset"], TILE["step"], TILE["size"]
        for i in range(TILE["cols"]):
            self.delete(self.gridLetters[self.row][i])
            self.gridLetters[self.row][i] = self.create_text(
                x0 + step*i + size//2, y0 + step*self.row + size//2,
                text=self.guessWord[i].upper(), font=TILE["font"], fill=TILE["invalid_color"],
            )

    def undoBadWord(self):
        x0, y0, step, size = TILE["x_offset"], TILE["y_offset"], TILE["step"], TILE["size"]
        for i in range(TILE["cols"]):
            self.delete(self.gridLetters[self.row][i])
            self.gridLetters[self.row][i] = self.create_text(
                x0 + step*i + size//2, y0 + step*self.row + size//2,
                text=self.guessWord[i].upper(), font=TILE["font"],
            )

    def winnerText(self):
        possiblePhrases = np.array(END_BANNER["text"])
        phrase = np.random.choice(possiblePhrases, 1)[0]
        self.winnerBanner.append(self.create_rectangle(
            END_BANNER["x0"], END_BANNER["y0"], END_BANNER["x1"], END_BANNER["y1"], fill=END_BANNER["fill"],
        ))
        self.winnerBanner.append(self.create_text(
            END_BANNER["cx"], END_BANNER["cy"], text=phrase, fill=END_BANNER["text_color"], font=END_BANNER["font"],
        ))

    def lostGame(self):
        self.loserBanner.append(self.create_rectangle(
            END_BANNER["x0"], END_BANNER["y0"], END_BANNER["x1"], END_BANNER["y1"], fill=END_BANNER["fill"],
        ))
        self.loserBanner.append(self.create_text(
            END_BANNER["cx"], END_BANNER["cy"], text=self.wordle.theWord.upper(), fill=END_BANNER["text_color"], font=END_BANNER["font"],
        ))
        self.statistics()
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
                    self.winnerText()
                    self.statistics()
                    self.wordle.finished = True
                elif self.row == 5:
                    self.lostGame()
                else:
                    self.col = 0
                    self.row += 1

    def statistics(self):
        print(self.wordle.userWord)
        print(self.wordle.theWord)
        if self.wordle.userWord == self.wordle.theWord:
            self.stats[self.row + 1] += 1
        else:
            self.stats[0] += 1
        print()
        for count in self.stats.keys():
            print("{} : {}".format(count, self.stats.get(count)))
        print()


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

app = App(root, width=CANVAS["width"], height=CANVAS["height"], )
app.grid(row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
# Give toolbar buttons access to the game after app exists.
toolbar.app = app  
app.setup()
app.startWordle()

root.bind("<Key>", app.letterTyped)
root.bind("<BackSpace>", app.deleteLetter)
root.bind("<Return>", app.enterWord)
root.bind("<Button>", app.restartGame)

root.mainloop()
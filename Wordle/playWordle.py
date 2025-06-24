import tkinter as tk
from wordle import Wordle
import numpy as np

# This script runs a local application of wordle that can be played repeatedly. 

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
        self.wordle = Wordle(usedWords=usedWords)
        print(self.wordle.theWord)

    def setup(self):
        self.createTitle()
        self.createTiles()
        self.letterBank = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.createLetters()

    def createTitle(self):
        self.title = tk.Text(self.root, height=0, width=6)
        self.title.config(font=("Courier", 64))
        self.title.grid(row=0, column=0, sticky=(tk.N))
        self.title.insert(tk.INSERT, "WORDLE")

    def createTiles(self):
        for row in range(6):
            for col in range(5):
                self.gridRectangles[row].append(self.create_rectangle(160 + 100*col,80 + 100*row, 
                                                240 + 100*col,160 + 100*row, outline="black"))
                self.gridLetters[row].append(self.create_text(200 + 100*col,120 + 100*row,  text="", font=("Courier", 64)))
    
    def createLetters(self):
        for row in [0,1]:
            for col in range(13):
                self.gridAlphabetBackground.append(self.create_rectangle(75 + 50*col, 675 + 50*row, 125 + 50*col, 725 + 50*row, outline="white"))
                self.gridAlphabet.append(self.create_text(100 + 50*col, 700 + 50*row, text=self.letterBank[row*13 + col], font=("Courier", 16)))

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
        for rect in range(5):
            if score[rect][1] == 2:
                self.itemconfigure(self.gridRectangles[self.row][rect], fill="green")
            elif score[rect][1] == 1:
                self.itemconfigure(self.gridRectangles[self.row][rect], fill="yellow")
            else:
                self.itemconfigure(self.gridRectangles[self.row][rect], fill="light grey")
    
    def updateAlphabet(self):
        for i in range(26):
            color = self.wordle.wordBank.get(self.letterBank[i].lower())
            if color == 2:
                self.itemconfig(self.gridAlphabetBackground[i], fill="green")
            elif color == 1:
                self.itemconfig(self.gridAlphabetBackground[i], fill="yellow")
            elif color == 0:
                self.itemconfig(self.gridAlphabetBackground[i], fill="light grey")
    
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
        for i in range(5):
            self.delete(self.gridLetters[self.row][i])
            self.gridLetters[self.row][i] = self.create_text(200 + 100*i,120 + 100*self.row,  text=self.guessWord[i].upper(), font=("Courier", 64), fill="red")

    def undoBadWord(self):
        for i in range(5):
            self.delete(self.gridLetters[self.row][i])
            self.gridLetters[self.row][i] = self.create_text(200 + 100*i,120 + 100*self.row,  text=self.guessWord[i].upper(), font=("Courier", 64))

    def winnerText(self):
        possiblePhrases = np.loadtxt("winning_messages.csv", dtype=str)
        phrase = np.random.choice(possiblePhrases, 1)[0]
        self.winnerBanner.append(self.create_rectangle(75, 675, 725, 775, fill="black"))
        self.winnerBanner.append(self.create_text(400, 725, text=phrase, fill="white", font=("Courier", 64)))

    def lostGame(self):
        self.loserBanner.append(self.create_rectangle(75, 675, 725, 775, fill="black"))
        self.loserBanner.append(self.create_text(400, 725, text=self.wordle.theWord.upper(), fill="white", font=("Courier", 64)))
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
root.geometry("800x800")
root.title("Wordle")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

app = App(root, width=800, height=800)
app.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
app.setup()
app.startWordle()

root.bind("<Key>", app.letterTyped)
root.bind("<BackSpace>", app.deleteLetter)
root.bind("<Return>", app.enterWord)
root.bind("<Button>", app.restartGame)

root.mainloop()
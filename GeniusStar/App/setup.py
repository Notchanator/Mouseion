from config import Config
from piece import Piece
from board import Board
from obstacle import Obstacle

import pandas as pd
import numpy as np
import os

class Setup:

    def __init__(self):
        self.config = Config()
        self.buildBoard()
        self.buildPieces()
        self.applyPieceConfig()
    
    def playGame(self):
        self.rollDices()
        return self.board, self.pieces, self.obstacles

    def applyPieceConfig(self):
        self.pieces = self.config.setPieceColors(self.pieces)
        self.pieces = self.config.setPieceLocations(self.pieces)

    def buildBoard(self):
        self.board = Board("Resources/Board.csv")
    
    def buildPieces(self):
        folderPath = "Resources/GamePieces/"
        self.pieces = {}
        for fileName in os.listdir(folderPath):
            filePath = os.path.join(folderPath, fileName)
            if os.path.isfile(filePath):
                self.pieces[fileName] = Piece(filePath)

    def buildObstacle(self, digit):
        # Create the Triangle Objects for each Obstacle based on the board information.
        return Obstacle(self.board.data.loc[digit, :])

    def rollDices(self):
        dice = self.config.createDice()
        self.obstacles = []
        for roll in dice:
            digit = np.random.choice(roll)
            self.board.data.loc[digit, "piece"] = "obstacle"
            self.obstacles.append(self.buildObstacle(digit))
            # TODO: Print On Same Line
            # print(digit)

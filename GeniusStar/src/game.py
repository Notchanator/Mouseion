import pandas as pd
import numpy as np
import src.piece as piece
import os

def rollDice(board):
    rand1 = np.random.choice([12, 13, 23, 24, 32, 33, 41, 42])
    board.loc[rand1, "piece"] = "obstacle"
    rand2 = np.random.choice([2, 4, 7, 8, 9, 11, 16, 17])
    board.loc[rand2, "piece"] = "obstacle"
    rand3 = np.random.choice([25, 26, 36, 37, 38, 40, 45, 47])
    board.loc[rand3, "piece"] = "obstacle"
    rand4 = np.random.choice([10,27,31])
    board.loc[rand4, "piece"] = "obstacle"
    rand5 = np.random.choice([18, 22, 39])
    board.loc[rand5, "piece"] = "obstacle"
    rand6 = np.random.choice([1, 5, 15, 34, 44, 48])
    board.loc[rand6, "piece"] = "obstacle"
    rand7 = np.random.choice([19, 20, 21, 28, 29, 30])
    board.loc[rand7, "piece"] = "obstacle"
    print(f"The Dice Rolls are {rand1}, {rand2}, {rand3}, {rand4}, {rand5}, {rand6}, {rand7}")
    return board

def setupGame():
    # Create Board
    board = pd.read_csv("Resources3/Board.csv")
    board['center_x'] = (board['v1_x'] + board['v2_x'] + board['v3_x']) / 3
    board['center_y'] = (board['v1_y'] + board['v2_y'] + board['v3_y']) / 3
    board["piece"] = None
    board = board.set_index('triangle_id')
    # Place Obstacles
    board = rollDice(board)
    # Create Pieces
    folderPath = "Resources3/GamePieces/"
    pieces = {}
    for fileName in os.listdir(folderPath):
        filePath = os.path.join(folderPath, fileName)
        if os.path.isfile(filePath):
            pieces[fileName] = piece.Piece(filePath)
    return board, pieces
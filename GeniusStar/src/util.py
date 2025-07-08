import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def roundHalf(value):
    return np.round(value * 2) / 2

def isSolved(board):
    return board["piece"].isna().sum() == 0

def createFakePiece(vertex, piece):
    return pd.DataFrame({
        'v1_x': piece.data['v1_x'] + vertex[0],
        'v1_y': piece.data['v1_y'] + vertex[1],
        'v2_x': piece.data['v2_x'] + vertex[0],
        'v2_y': piece.data['v2_y'] + vertex[1],
        'v3_x': piece.data['v3_x'] + vertex[0],
        'v3_y': piece.data['v3_y'] + vertex[1]
    })

def getBoardIndices(board):
    return pd.concat([
        board[['v1_x', 'v1_y']].apply(tuple, axis=1),
        board[['v2_x', 'v2_y']].apply(tuple, axis=1),
        board[['v3_x', 'v3_y']].apply(tuple, axis=1)
    ]).value_counts().index.values


def setPreviousPiece(pieces):
    pieces["DarkGreen5.csv"].previous_piece = None
    pieces["Lavender5.csv"].previous_piece = pieces["DarkGreen5.csv"]
    pieces["LightGreen5.csv"].previous_piece = pieces["Lavender5.csv"]
    pieces["Red5.csv"].previous_piece = pieces["LightGreen5.csv"]
    pieces["Purple4.csv"].previous_piece = pieces["Red5.csv"]
    pieces["Orange4.csv"].previous_piece = pieces["Purple4.csv"]
    pieces["Pink4.csv"].previous_piece = pieces["Orange4.csv"]
    pieces["Blue3_1.csv"].previous_piece = pieces["Pink4.csv"]
    pieces["Blue3_2.csv"].previous_piece = pieces["Blue3_1.csv"]
    pieces["Yellow2.csv"].previous_piece = pieces["Blue3_2.csv"] 
    pieces["DarkBlue1.csv"].previous_piece = pieces["Yellow2.csv"]
    return pieces

def setPieceConfigs(pieces):
    pieces["DarkGreen5.csv"].maxRotation = 6
    pieces["DarkGreen5.csv"].canFlip = False
    pieces["Lavender5.csv"].maxRotation = 6
    pieces["Lavender5.csv"].canFlip =  True
    pieces["LightGreen5.csv"].maxRotation = 6
    pieces["LightGreen5.csv"].canFlip = True
    pieces["Red5.csv"].maxRotation = 6
    pieces["Red5.csv"].canFlip = False
    pieces["Purple4.csv"].maxRotation = 2
    pieces["Purple4.csv"].canFlip =  False
    pieces["Orange4.csv"].maxRotation = 6
    pieces["Orange4.csv"].canFlip = False
    pieces["Pink4.csv"].maxRotation = 6
    pieces["Pink4.csv"].canFlip =  False
    pieces["Blue3_1.csv"].maxRotation = 3
    pieces["Blue3_1.csv"].canFlip = True
    pieces["Blue3_2.csv"].maxRotation = 3
    pieces["Blue3_2.csv"].canFlip = True
    pieces["Yellow2.csv"].maxRotation = 4
    pieces["Yellow2.csv"].canFlip =  False
    pieces["DarkBlue1.csv"].maxRotation = 2
    pieces["DarkBlue1.csv"].canFlip = False
    return pieces

def reorderPieces(pieces):
    return [
        pieces["DarkGreen5.csv"], pieces["Lavender5.csv"], pieces["LightGreen5.csv"], 
        pieces["Red5.csv"], pieces["Purple4.csv"], pieces["Orange4.csv"], pieces["Pink4.csv"],
        pieces["Blue3_1.csv"], pieces["Blue3_2.csv"], pieces["Yellow2.csv"], pieces["DarkBlue1.csv"]
    ]

def plotBoard(board):
    fig, ax = plt.subplots()
    for triangle in board.index:
        ax.plot(
            [board.loc[triangle, "v1_x"], board.loc[triangle, "v2_x"]],
            [ board.loc[triangle, "v1_y"],  board.loc[triangle, "v2_y"]]
        )
        ax.plot(
            [board.loc[triangle, "v2_x"], board.loc[triangle, "v3_x"]],
            [board.loc[triangle, "v2_y"], board.loc[triangle, "v3_y"]]
        )
        ax.plot(
            [board.loc[triangle, "v1_x"], board.loc[triangle, "v3_x"]],
            [board.loc[triangle, "v1_y"], board.loc[triangle, "v3_y"]]
        )
        ax.annotate(board.loc[triangle, "piece"], (board.loc[triangle, "center_x"], board.loc[triangle, "center_y"]), size=6,  ha='center')
    plt.show()
import numpy as np
import pandas as pd
import os

from src.util import roundHalf

class Piece:

    previous_piece = None
    last_indx = None
    rotation = 1
    flipped = False
    placed = False
    pattern = None # This will be a string to help define the patterns of connections

    def __init__(self, fileLocation=None):
        self.fileLocation = fileLocation
        self.name = os.path.splitext(os.path.basename(fileLocation))[0]    
        self.createPiece(fileLocation)
    
    def calculateCenter(self):
        self.data['center_x'] = (self.data['v1_x'] + self.data['v2_x'] + self.data['v3_x']) / 3
        self.data['center_y'] = (self.data['v1_y'] + self.data['v2_y'] + self.data['v3_y']) / 3

    def createPiece(self, fileLocation):
        df = pd.read_csv(fileLocation)
        df = df.set_index("triangle_id")
        self.data = df
        self.calculateCenter()

    def rotateForwards(self):
        # Rotate All Three Vertices.
        for vertex in range(1,4):
            # We have to update the axis individually and the calculations are based on the original.
            x = self.data['v'+str(vertex)+'_x']
            y = self.data['v'+str(vertex)+'_y']
            self.data['v'+str(vertex)+'_x'] = roundHalf(x*np.cos(np.pi/3) - y*np.sin(np.pi/3))
            self.data['v'+str(vertex)+'_y'] = roundHalf(y*np.cos(np.pi/3) + x*np.sin(np.pi/3))
        self.calculateCenter()

    def rotateBackwords(self):
        # Rotate All Three Vertices.
        for vertex in range(1,4):
            # We have to update the axis individually and the calculations are based on the original.
            x = self.data['v'+str(vertex)+'_x']
            y = self.data['v'+str(vertex)+'_y']
            self.data['v'+str(vertex)+'_x'] = roundHalf(x*np.cos((-1*np.pi)/3) - y*np.sin((-1*np.pi)/3))
            self.data['v'+str(vertex)+'_y'] = roundHalf(y*np.cos((-1*np.pi)/3) + x*np.sin((-1*np.pi)/3))
        self.calculateCenter()

    def flipPiece(self):
        for vertex in range(1,4):
            self.data['v'+str(vertex)+'_x'] = -1 * self.data['v'+str(vertex)+'_x']
        self.flipped = not self.flipped
        self.calculateCenter()


def placeIfValid(board, vertex, piece):
    # Calculate the Loactions of each Piece within the Board.
    fakePiece = createFakePiece(vertex, piece)
    # Calculate the Centers.
    fakePiece['center_x'] = (fakePiece['v1_x'] + fakePiece['v2_x'] + fakePiece['v3_x']) / 3
    fakePiece['center_y'] = (fakePiece['v1_y'] + fakePiece['v2_y'] + fakePiece['v3_y']) / 3
    # Are the Centers Open?
    triangles = board[board[['center_x', 'center_y']].apply(tuple, axis=1).isin(fakePiece[['center_x', 'center_y']].apply(tuple, axis=1))]
    if triangles[triangles['piece'].isnull()].shape[0] == fakePiece.shape[0]:
        # If all spaces are open, place the piece.
        board.loc[triangles.index, 'piece'] = piece.name
        return board, True
    return board, False

def removePiece(board, piece):
    board.loc[board['piece'] == piece.name, 'piece'] = None
    return board

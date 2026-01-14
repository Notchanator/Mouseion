import pygame
import os
import pandas as pd
import numpy as np

from board import Board
from triangle import Triangle
from piece import Piece

# To Speed Up Blitting: we could blit the board for the space it was just moved from, and then the moving piece. 

def scaleBoard(board, scale = 100, center = (427, 360)):
    board['v1_x'] = (board['v1_x'] * scale) + center[0]
    board['v2_x'] = (board['v2_x'] * scale) + center[0]
    board['v3_x'] = (board['v3_x'] * scale) + center[0]
    board['v1_y'] = (board['v1_y'] * scale) + center[1]
    board['v2_y'] = (board['v2_y'] * scale) + center[1]
    board['v3_y'] = (board['v3_y'] * scale) + center[1]
    return board


def buildBoard():
    board_import = pd.read_csv("Resources3/Board.csv")
    board_import = scaleBoard(board_import)
    board_import['center_x'] = (board_import['v1_x'] + board_import['v2_x'] + board_import['v3_x']) / 3
    board_import['center_y'] = (board_import['v1_y'] + board_import['v2_y'] + board_import['v3_y']) / 3
    board_import["piece"] = None
    board_import = board_import.set_index('triangle_id')
    board = Board(board_import)
    return board

def buildObstacles(board, obstacles):
    # Create the Triangle Objects for each Obstacle based on the board information.
    triangle_list = []
    for obstacle in obstacles:
        triangle_list.append(
            Triangle(
                "obstacle",
                (board.table.loc[obstacle, "v1_x"], board.table.loc[obstacle, "v1_y"]),
                (board.table.loc[obstacle, "v2_x"], board.table.loc[obstacle, "v2_y"]),
                (board.table.loc[obstacle, "v3_x"], board.table.loc[obstacle, "v3_y"])
            )
        )
    return triangle_list

def displayObstacles(screen, obstacles):
    for obstacle in obstacles:
        # print(obstacle.getVertices())
        pygame.draw.polygon(screen, (255,255,255), obstacle.getVertices(), 0)


def rollDices(board):
    rand1 = np.random.choice([12, 13, 23, 24, 32, 33, 41, 42])
    board.table.loc[rand1, "piece"] = "obstacle"
    rand2 = np.random.choice([2, 4, 7, 8, 9, 11, 16, 17])
    board.table.loc[rand2, "piece"] = "obstacle"
    rand3 = np.random.choice([25, 26, 36, 37, 38, 40, 45, 47])
    board.table.loc[rand3, "piece"] = "obstacle"
    rand4 = np.random.choice([10,27,31])
    board.table.loc[rand4, "piece"] = "obstacle"
    rand5 = np.random.choice([18, 22, 39])
    board.table.loc[rand5, "piece"] = "obstacle"
    rand6 = np.random.choice([1, 5, 15, 34, 44, 48])
    board.table.loc[rand6, "piece"] = "obstacle"
    rand7 = np.random.choice([19, 20, 21, 28, 29, 30])
    board.table.loc[rand7, "piece"] = "obstacle"
    obstacles = [rand1, rand2, rand3, rand4, rand5, rand6, rand7]
    print(f"The Dice Rolls are {rand1}, {rand2}, {rand3}, {rand4}, {rand5}, {rand6}, {rand7}")
    return board, buildObstacles(board, obstacles)

def setPieceColors(pieces):
    pieces["DarkGreen5.csv"].color = (0,153,0)
    pieces["Lavender5.csv"].color = (153,0,153)
    pieces["LightGreen5.csv"].color = (0,255,0)
    pieces["Red5.csv"].color = (255,0,0)
    pieces["Purple4.csv"].color = (102,0,204)
    pieces["Orange4.csv"].color = (255,128,0)
    pieces["Pink4.csv"].color = (255,0,255)
    pieces["Blue3_1.csv"].color = (0,128,255)
    pieces["Blue3_2.csv"].color = (0,128,255)
    pieces["Yellow2.csv"].color = (255,255,0)
    pieces["DarkBlue1.csv"].color = (0,0,204)

def setPieceLocations(pieces):
    pieces["DarkGreen5.csv"].placePiece((875, 40))
    pieces["Lavender5.csv"].placePiece((1124, 48))
    pieces["LightGreen5.csv"].placePiece((893, 182))
    pieces["Red5.csv"].placePiece((1161 ,178))
    pieces["Purple4.csv"].placePiece((881, 313))
    pieces["Orange4.csv"].placePiece((1143, 315))
    pieces["Pink4.csv"].placePiece((874,462))
    pieces["Blue3_1.csv"].placePiece((1139, 473))
    pieces["Blue3_2.csv"].placePiece((858, 579))
    pieces["Yellow2.csv"].placePiece((1107, 566))
    pieces["DarkBlue1.csv"].placePiece(((100, 560)))


def buildPieces():
    folderPath = "Resources3/GamePieces/"
    pieces = {}
    for fileName in os.listdir(folderPath):
        filePath = os.path.join(folderPath, fileName)
        if os.path.isfile(filePath):
            pieces[fileName] = Piece(filePath)
    return pieces

def displayPieces(screen, pieces):
    for piece in pieces:
        pieces[piece].displayTriangles(screen)

def startGame():
    board = buildBoard()
    pieces = buildPieces()
    setPieceColors(pieces)
    setPieceLocations(pieces)
    return board, pieces

def isClickOnPiece(pieces, pos):
    # The best way to determine if a point is in a triangle is though Baycentric Coordinates. EXPAND
    # TODO: This can be sped up via pandas.
    for piece in pieces:
        if pieces[piece].posInPiece(pos):
            return piece
    return None

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)
running = True
dt = 0
clickedPiece = None
previousMousePos = None

pygame.display.set_caption('Genius Star')

board, pieces = startGame()
board, obstacles = rollDices(board)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickedPiece = isClickOnPiece(pieces, pygame.mouse.get_pos())
            if clickedPiece: 
                previousMousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION and clickedPiece is not None:
            newMousePos = pygame.mouse.get_pos()
            mousePosDiff = (newMousePos[0] - previousMousePos[0], newMousePos[1] - previousMousePos[1])
            pieces[clickedPiece].placePiece(mousePosDiff)
            previousMousePos = newMousePos
        if event.type == pygame.MOUSEBUTTONUP:
            clickedPiece = None
    screen.fill([104, 104, 104]) 
    displayPieces(screen, pieces)
    displayObstacles(screen, obstacles)
    board.displayTriangles(screen, font)
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
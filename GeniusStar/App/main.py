import pygame
from shapely.geometry import Polygon
from setup import Setup
from board import createShapelyTriangle

# To Speed Up Blitting (if necessary): we could blit the board for the space it was just moved from, and then the moving piece. 



def calculateCenter(triangle):
    x = (triangle["v1_x"] + triangle["v2_x"] + triangle["v3_x"]) / 3
    y = (triangle["v1_y"] + triangle["v2_y"] + triangle["v3_y"]) / 3
    return (x, y)

def displayPieces(screen, piece):
    for piece in pieces:
        pieces[piece].displayTriangles(screen)

def displayObstacles(screen, obstacles):
    for obstacle in obstacles:
        obstacle.displayTriangles(screen)

def distanceBetweenTriangles(triangle1, triangle2):
    center1 = calculateCenter(triangle1)
    center2 = calculateCenter(triangle2)
    return (center1[0] - center2[0], center1[1] - center2[1])


def isClickOnPiece(pieces, pos):
    # The best way to determine if a point is in a triangle is though Baycentric Coordinates. EXPAND
    # TODO: This can be sped up via pandas.
    for piece in pieces:
        inPiece, triangle = pieces[piece].posInPiece(pos)
        if inPiece:
            return piece, triangle
    return None, None

def isClickOnBoard(board, pos):
    # The best way to determine if a point is in a triangle is though Baycentric Coordinates. EXPAND
    # TODO: This can be sped up via pandas.
    inBoard, triangle = board.posInPiece(pos)
    if inBoard:
        return True, triangle
    return False, None


def findValidPlacement(board, boardTriangles, piece, pieceTriangleId):
    # Sort the triangles by overlap.
    sortedTriangles = dict(sorted(boardTriangles.items(), key=lambda x: x[1], reverse=True))
    for id, overlap in sortedTriangles.items():
        if board.data.loc[id, "orientation"] != piece.data.loc[pieceTriangleId, "orientation"]:
            continue
        # We will actually place the piece to identify the locations of all it's triangles. This can be improved.
        distanceToPlace = distanceBetweenTriangles(board.data.loc[id, :], piece.data.loc[pieceTriangleId, :])
        piece.updatePiecePos(distanceToPlace)
        boardTriangles = board.getOverlappingTrianglesForPiece(piece)
        if piece.data.shape[0] != len(boardTriangles):
            continue
        if board.allPiecesOpen(boardTriangles):
            return True, id
    return False, None



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

setup = Setup()
board, pieces, obstacles = setup.playGame()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickedPiece, pieceTriangleId = isClickOnPiece(pieces, pygame.mouse.get_pos())
            if clickedPiece: 
                previousMousePos = pygame.mouse.get_pos()
                board.removePiece(pieces[clickedPiece])
        if event.type == pygame.MOUSEMOTION and clickedPiece:
            newMousePos = pygame.mouse.get_pos()
            mousePosDiff = (newMousePos[0] - previousMousePos[0], newMousePos[1] - previousMousePos[1])
            pieces[clickedPiece].updatePiecePos(mousePosDiff)
            previousMousePos = newMousePos
        if event.type == pygame.MOUSEBUTTONUP and clickedPiece:
            # clickedBoard, boardTriangleId = isClickOnBoard(board, pygame.mouse.get_pos())
            clickedBoard, overlappingBoardTriangles = board.getOverlappingTriangles(createShapelyTriangle(pieces[clickedPiece].data.loc[pieceTriangleId,]))
            if clickedBoard:
                isVald, boardTriangleId = findValidPlacement(board, overlappingBoardTriangles, pieces[clickedPiece], pieceTriangleId)
                if isVald:
                    mousePosDiff = distanceBetweenTriangles(board.data.loc[boardTriangleId, :], pieces[clickedPiece].data.loc[pieceTriangleId, :])
                    board.placePiece(pieces[clickedPiece])
                    pieces[clickedPiece].updatePiecePos(mousePosDiff)
                else:
                    originalPiecePos = setup.config.getPieceOirignalPos(clickedPiece)
                    pieceCurentCenterPos = pieces[clickedPiece].centerPoint
                    mousePosDiff = (originalPiecePos[0] - pieceCurentCenterPos[0], originalPiecePos[1] - pieceCurentCenterPos[1])
                    pieces[clickedPiece].updatePiecePos(mousePosDiff)
            else:
                originalPiecePos = setup.config.getPieceOirignalPos(clickedPiece)
                pieceCurentCenterPos = pieces[clickedPiece].centerPoint
                mousePosDiff = (originalPiecePos[0] - pieceCurentCenterPos[0], originalPiecePos[1] - pieceCurentCenterPos[1])
                board.removePiece(pieces[clickedPiece])
                pieces[clickedPiece].updatePiecePos(mousePosDiff)

            clickedPiece = None
        if event.type == pygame.KEYDOWN:
            mousePos = pygame.mouse.get_pos()
            if event.key == pygame.K_a and clickedPiece:
                pieces[clickedPiece].rotateBackwords(mousePos)
            if event.key == pygame.K_d and clickedPiece:
                pieces[clickedPiece].rotateForwards(mousePos)
            if event.key == pygame.K_w and clickedPiece:
                pieces[clickedPiece].flipPiece(mousePos)
            if event.key == pygame.K_s and clickedPiece:
                pieces[clickedPiece].flipPiece(mousePos)
    screen.fill([104, 104, 104]) 
    board.displayTriangles(screen)
    board.displayTriangleNumbers(screen, font)
    displayObstacles(screen, obstacles)
    displayPieces(screen, pieces)
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
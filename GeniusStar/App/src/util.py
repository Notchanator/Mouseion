import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def isSolved(board):
    return board["piece"].isna().sum() == 0

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
        ax.annotate(board.loc[triangle, "id"], (board.loc[triangle, "center_x"], board.loc[triangle, "center_y"]), size=6,  ha='center')
    plt.show()


def isUnSolvable(board):
    # Create df of empty triangles on the board.
    empty_triangles = board[board['piece'].isnull()]
    # Add Search Information.
    empty_triangles.loc[:, 'searched'] = False
    # Loop throgh each triangle.
    triangle_forest = []
    queue = []
    triangle_tree = []
    # Loop until everything is searched. Add an extra loop to plant the final tree in the forest.
    while empty_triangles['searched'].sum() < (empty_triangles['searched'].count() + 1):
    # for _ in range(10):
        if len(queue) > 0:
            # Pop the first item in the queue.
            indx, queue = queue[0], queue[1:]
            # Get the edges for the indx.
            edges = empty_triangles.loc[int(indx)][['edge_0', 'edge_1', 'edge_2']]
            # Simplify to edges that haven't been searched.
            non_searched_edges = empty_triangles[(empty_triangles.index.isin(edges)) & (~empty_triangles['searched'])]
            # Add each non-searched edge to the tree and queue.
            triangle_tree = np.append(triangle_tree, non_searched_edges.index.tolist())
            queue = np.append(queue, non_searched_edges.index.tolist())
            # Mark each edge as searched.
            empty_triangles.loc[empty_triangles.index.isin(non_searched_edges.index), 'searched'] = True
        else:
            if len(triangle_tree) > 0:
                triangle_forest.append(triangle_tree)
            # Get first unsearched vertex.
            indx = empty_triangles[~empty_triangles['searched']].index.min()
            if np.isnan(indx):
                break
            # Add triangle to the tree and queue.
            triangle_tree = np.array([int(empty_triangles.loc[indx].name)])
            queue = np.array([int(empty_triangles.loc[indx].name)])
            # Mark the triangle as searched.
            empty_triangles.loc[indx, 'searched'] = True
    lengths = [len(tri) for tri in triangle_forest]
    if len([tree for tree in lengths if tree == 1]) > 1:
        return True
    if len([tree for tree in lengths if tree == 2]) > 1:
        return True
    if len([tree for tree in lengths if tree == 3]) > 3:
        return True
    if len([tree for tree in lengths if tree == 4]) > 3:
        return True
    return False
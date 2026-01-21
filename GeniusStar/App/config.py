
class Config:

    pieceConfig = {
        "DarkGreen5.csv":
            {"color":(0,153,0), "originalPos":(841, 606)},
        "Lavender5.csv":
            {"color":(153,0,153), "originalPos":(842, 119)},
        "LightGreen5.csv":
            {"color":(0,255,0), "originalPos":(844, 238)},
        "Red5.csv":
            {"color":(255,0,0), "originalPos":(1087, 117)},
        "Purple4.csv":
            {"color":(102,0,204), "originalPos":(790, 439)},
        "Orange4.csv":
            {"color":(255,128,0), "originalPos":(1146, 613)},
        "Pink4.csv":
            {"color":(255,0,255), "originalPos":(1087,380)},
        "Blue3_1.csv":
            {"color":(0,128,255), "originalPos":(1131, 148)},
        "Blue3_2.csv":
            {"color":(0,128,255), "originalPos":(1131, 263)},
        "Yellow2.csv":
            {"color":(255,255,0), "originalPos":(1082, 500)},
        "DarkBlue1.csv":
            {"color":(0,0,204), "originalPos":(916, 483)},
    }

    def __init__(self):
        pass

    def setPieceColors(self, pieces):
        for piece in pieces:
            pieces[piece].color = self.pieceConfig[piece]["color"]
        return pieces

    def setPieceLocations(self, pieces):
        for piece in pieces:
            pieces[piece].updatePiecePos(self.pieceConfig[piece]["originalPos"])
        return pieces
    
    def getPieceOirignalPos(self, piece):
        return self.pieceConfig[piece]["originalPos"]
    
    def createDice(self):
        return [
            [12, 13, 23, 24, 32, 33, 41, 42],
            [2, 4, 7, 8, 9, 11, 16, 17],
            [25, 26, 36, 37, 38, 40, 45, 47],
            [10,27,31],
            [18, 22, 39],
            [1, 5, 15, 34, 44, 48],
            [19, 20, 21, 28, 29, 30]
        ]

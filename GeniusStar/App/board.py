import pygame
import pandas as pd
import os

def signedRatio(pos1, pos2, pos3):
    # The best way to determine if a point is in a triangle is though Baycentric Coordinates. EXPAND
    return (pos1[0] - pos3[0]) * (pos2[1] - pos3[1]) - (pos2[0] - pos3[0]) * (pos1[1] - pos3[1])

def calculateCenter(triangle):
    x = (triangle["v1_x"] + triangle["v2_x"] + triangle["v3_x"]) / 3
    y = (triangle["v1_y"] + triangle["v2_y"] + triangle["v3_y"]) / 3
    return (x, y)

class Board:

    centerPoint = (0,0)

    def __init__(self, fileLocation=None):
        self.fileLocation = fileLocation
        self.name = os.path.splitext(os.path.basename(fileLocation))[0]    
        self.createPiece()

    def createPiece(self):
        df = pd.read_csv(self.fileLocation)
        df = df.set_index("triangle_id")
        df["piece"] = None
        self.data = df
        self.scalePiece()
        self.updatePiecePos()
    
    def scalePiece(self, scale = 100):
        self.data['v1_x'] = (self.data['v1_x'] * scale)
        self.data['v2_x'] = (self.data['v2_x'] * scale)
        self.data['v3_x'] = (self.data['v3_x'] * scale)
        self.data['v1_y'] = (self.data['v1_y'] * scale)
        self.data['v2_y'] = (self.data['v2_y'] * scale)
        self.data['v3_y'] = (self.data['v3_y'] * scale)
    
    def updatePiecePos(self, location = (427, 360)):
        self.data['v1_x'] = (self.data['v1_x'] + location[0])
        self.data['v2_x'] = (self.data['v2_x'] + location[0])
        self.data['v3_x'] = (self.data['v3_x'] + location[0])
        self.data['v1_y'] = (self.data['v1_y'] + location[1])
        self.data['v2_y'] = (self.data['v2_y'] + location[1])
        self.data['v3_y'] = (self.data['v3_y'] + location[1])
        self.centerPoint = (self.centerPoint[0] + location[0], self.centerPoint[1] + location[1])

    def posInPiece(self, pos):
        # TODO: Better Documentation of this Baycentric Math.
        for id in self.data.index:
            determinate1 = signedRatio(pos, 
                                       (self.data.loc[id, 'v1_x'], self.data.loc[id, 'v1_y']),
                                       (self.data.loc[id, 'v2_x'], self.data.loc[id, 'v2_y'])
            )
            determinate2 = signedRatio(pos,
                                       (self.data.loc[id, 'v2_x'], self.data.loc[id, 'v2_y']),
                                       (self.data.loc[id, 'v3_x'], self.data.loc[id, 'v3_y'])
            )
            determinate3 = signedRatio(pos,
                                       (self.data.loc[id, 'v3_x'], self.data.loc[id, 'v3_y']),
                                       (self.data.loc[id, 'v1_x'], self.data.loc[id, 'v1_y'])
            )
            has_neg = (determinate1 < 0) or (determinate2 < 0) or (determinate3 < 0)
            has_pos = (determinate1 > 0) or (determinate2 > 0) or (determinate3 > 0)

            if not (has_neg and has_pos):
                return True, id
        return False, None

    def displayTriangles(self, screen, font):
        for id in self.data.index:
            vertices = (
                (self.data.loc[id, "v1_x"], self.data.loc[id, "v1_y"]),
                (self.data.loc[id, "v2_x"], self.data.loc[id, "v2_y"]),
                (self.data.loc[id, "v3_x"], self.data.loc[id, "v3_y"])
            )
            pygame.draw.polygon(screen, (0,0,0), vertices, 5)
            display = font.render(str(id), 1, (0,0,0))
            display_pos = display.get_rect(center = calculateCenter(self.data.loc[id, :]))
            screen.blit(display, display_pos)
        
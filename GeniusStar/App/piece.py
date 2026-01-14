import numpy as np
import pandas as pd
import os

from triangle import Triangle

def signedRatio(pos1, pos2, pos3):
    # The best way to determine if a point is in a triangle is though Baycentric Coordinates. EXPAND
    return (pos1[0] - pos3[0]) * (pos2[1] - pos3[1]) - (pos2[0] - pos3[0]) * (pos1[1] - pos3[1])

class Piece:

    def __init__(self, fileLocation=None):
        self.fileLocation = fileLocation
        self.name = os.path.splitext(os.path.basename(fileLocation))[0]    
        self.createPiece(fileLocation)

    def calculateCenter(self):
        self.data['center_x'] = (self.data['v1_x'] + self.data['v2_x'] + self.data['v3_x']) / 3
        self.data['center_y'] = (self.data['v1_y'] + self.data['v2_y'] + self.data['v3_y']) / 3

    def scalePiece(self, scale = 100):
        self.data['v1_x'] = (self.data['v1_x'] * scale)
        self.data['v2_x'] = (self.data['v2_x'] * scale)
        self.data['v3_x'] = (self.data['v3_x'] * scale)
        self.data['v1_y'] = (self.data['v1_y'] * scale)
        self.data['v2_y'] = (self.data['v2_y'] * scale)
        self.data['v3_y'] = (self.data['v3_y'] * scale)

    def updateTrianglePos(self, location):
        for triangle in self.triangle_list:
            triangle.moveVertices(location[0], location[1])
    
    def placePiece(self, location):
        self. updateTrianglePos(location)
        self.data['v1_x'] = (self.data['v1_x'] + location[0])
        self.data['v2_x'] = (self.data['v2_x'] + location[0])
        self.data['v3_x'] = (self.data['v3_x'] + location[0])
        self.data['v1_y'] = (self.data['v1_y'] + location[1])
        self.data['v2_y'] = (self.data['v2_y'] + location[1])
        self.data['v3_y'] = (self.data['v3_y'] + location[1])
        self.calculateCenter()

    def createPiece(self, fileLocation):
        df = pd.read_csv(fileLocation)
        df = df.set_index("triangle_id")
        self.data = df
        self.scalePiece()
        self.calculateCenter()
        self.buildTriangles()

    def posInPiece(self, pos):
        # TODO: Better Documentation of this Baycentric Math.
        for triangle in self.triangle_list:
            determinate1 = signedRatio(pos, triangle.v1, triangle.v2)
            determinate2 = signedRatio(pos, triangle.v2, triangle.v3)
            determinate3 = signedRatio(pos, triangle.v3, triangle.v1) 

            has_neg = (determinate1 < 0) or (determinate2 < 0) or (determinate3 < 0)
            has_pos = (determinate1 > 0) or (determinate2 > 0) or (determinate3 > 0)

            if not (has_neg and has_pos):
                return True
        return False

    
    def buildTriangles(self):
        self.triangle_list = []
        for row in self.data.index:
            self.triangle_list.append(
                Triangle(
                    id = row,
                    v1 = (self.data.loc[row, "v1_x"], self.data.loc[row, "v1_y"]),
                    v2 = (self.data.loc[row, "v2_x"], self.data.loc[row, "v2_y"]),
                    v3 = (self.data.loc[row, "v3_x"], self.data.loc[row, "v3_y"])
                )
            )

    def displayTriangles(self, screen):
        for triangle in self.triangle_list:
            # print(triangle.getVertices())
            triangle.displayTriangle(screen, self.color, 0)
            triangle.displayTriangle(screen, (0,0,0), 2)
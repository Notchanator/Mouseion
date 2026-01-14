import numpy as np
import pygame 

class Triangle:

    placed_center = (427, 360)
    scale = 10

    def __init__(self, id, v1, v2, v3):
        self.id = id
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def calculateCenterPoint(self):
        x = (self.v1[0] + self.v2[0] + self.v3[0]) / 3
        y = (self.v1[1] + self.v2[1] + self.v3[1]) / 3
        self.center_x = x
        self.center_y = y

    def getCenter(self):
        self.calculateCenterPoint()
        return (self.center_x, self.center_y)

    def getVertices(self):
        return (self.v1, self.v2, self.v3)
    
    def scaleVertices(self, scale):
        self.v1 = (self.v1[0] * scale, self.v1[1] * scale)
        self.v2 = (self.v2[0] * scale, self.v2[1] * scale)
        self.v3 = (self.v3[0] * scale, self.v3[1] * scale)

    def moveVertices(self, dx, dy):
        self.v1 = (self.v1[0] + dx, self.v1[1] + dy)
        self.v2 = (self.v2[0] + dx, self.v2[1] + dy)
        self.v3 = (self.v3[0] + dx, self.v3[1] + dy)

    def displayTriangle(self, screen, color, line_width):
        pygame.draw.polygon(screen, color, self.getVertices(), line_width)
import pygame
from triangle import Triangle

class Board:

    def __init__(self, board):
        self.table = board
        self.buildTriangles()

    def buildTriangles(self):
        self.triangle_list = []
        for row in self.table.index:
            self.triangle_list.append(
                Triangle(
                    id = row,
                    v1 = (self.table.loc[row, "v1_x"], self.table.loc[row, "v1_y"]),
                    v2 = (self.table.loc[row, "v2_x"], self.table.loc[row, "v2_y"]),
                    v3 = (self.table.loc[row, "v3_x"], self.table.loc[row, "v3_y"])
                )
            )
    

    def displayTriangles(self, screen, font):
        for triangle in self.triangle_list:
            triangle.displayTriangle(screen, (0,0,0), 5)
            # pygame.draw.polygon(screen, (0,0,0), triangle.getVertices(), 5)
            display = font.render(str(triangle.id), 1, (0,0,0))
            display_pos = display.get_rect(center = triangle.getCenter())
            screen.blit(display, display_pos)
    

    
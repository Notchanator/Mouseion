import pygame


class Obstacle:

    color = (255,255,255)

    def __init__(self, data):
        self.name = "obstacle"
        self.data = data

    def displayTriangles(self, screen):
        vertices = (
            (self.data["v1_x"], self.data["v1_y"]),
            (self.data["v2_x"], self.data["v2_y"]),
            (self.data["v3_x"], self.data["v3_y"])
        )
        pygame.draw.polygon(screen, self.color, vertices, 0)
        pygame.draw.polygon(screen, (0,0,0), vertices, 2)
import os
import pygame as pg

class PacmanMap():
    def __init__(self):
        self.walls = []  # Make a list of the walls
        # Add all the map's walls
        # Outer walls:
        self.walls.append(self.makeWall(0, 0, 17, 1))
        self.walls.append(self.makeWall(0, 1, 1, 7))
        self.walls.append(self.makeWall(0, 9, 1, 7))
        self.walls.append(self.makeWall(0, 16, 17, 1))
        self.walls.append(self.makeWall(16, 1, 1, 7))
        self.walls.append(self.makeWall(16, 9, 1, 7))
        # Outer wall connected pieces:
        #   Left:
        self.walls.append(self.makeWall(1, 6, 3, 2))
        self.walls.append(self.makeWall(1, 9, 3, 2))
        self.walls.append(self.makeWall(1, 14, 1, 1))
        self.walls.append(self.makeWall(3, 15, 4, 1))
        self.walls.append(self.makeWall(5, 14, 1, 1))
        #   Middle:
        self.walls.append(self.makeWall(8, 1, 1, 2))
        self.walls.append(self.makeWall(8, 13, 1, 3))
        #   Right:
        self.walls.append(self.makeWall(13, 6, 3, 2))
        self.walls.append(self.makeWall(13, 9, 3, 2))
        self.walls.append(self.makeWall(15, 14, 1, 1))
        self.walls.append(self.makeWall(10, 15, 4, 1))
        self.walls.append(self.makeWall(11, 14, 1, 1))
        # Field pieces
        #   Left:
        self.walls.append(self.makeWall(2, 2, 2, 1))
        self.walls.append(self.makeWall(2, 4, 2, 1))
        self.walls.append(self.makeWall(5, 2, 2, 1))
        self.walls.append(self.makeWall(5, 4, 1, 4))
        self.walls.append(self.makeWall(5, 9, 1, 2))
        self.walls.append(self.makeWall(5, 12, 2, 1))
        self.walls.append(self.makeWall(2, 12, 2, 1))
        self.walls.append(self.makeWall(3, 13, 1, 1))
        #   Middle:
        self.walls.append(self.makeWall(7, 4, 3, 1))
        self.walls.append(self.makeWall(8, 5, 1, 1))
        self.walls.append(self.makeWall(7, 10, 3, 1))
        self.walls.append(self.makeWall(8, 11, 1, 1))
        #   Right:
        self.walls.append(self.makeWall(10, 2, 2, 1))
        self.walls.append(self.makeWall(13, 2, 2, 1))
        self.walls.append(self.makeWall(13, 4, 2, 1))
        self.walls.append(self.makeWall(11, 4, 1, 4))
        self.walls.append(self.makeWall(11, 9, 1, 2))
        self.walls.append(self.makeWall(10, 12, 2, 1))
        self.walls.append(self.makeWall(13, 12, 2, 1))
        self.walls.append(self.makeWall(13, 13, 1, 1))
        # Ghost box:
        self.walls.append(self.makeWall(7, 7, 3, 2))

    def makeWall(self, leftX, topY, width, height):
        gridSize = 51  # Variable for grid size to easily create walls in a grid format
        # Convert grid unit to pixels
        leftX *= gridSize
        topY *= gridSize
        width *= gridSize
        height *= gridSize
        # Create rectangle object representing wall
        wall = pg.Rect(leftX, topY, width, height)
        return wall

    def mapCollide(self, rect):
        for wall in self.walls:
            if wall.colliderect(rect):
                return True
        return False







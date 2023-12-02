import os
import pygame as pg


class PacmanMap:
    def __init__(self):
        self.__walls = []  # Make a list of the walls
        self.__gridSize = 51 # Using a grid to easily plot the walls on the background map
        # Add all the map's walls
        # Outer walls:
        self.__walls.append(pg.Rect(0*self.__gridSize, 0*self.__gridSize, 17*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(0*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize, 7*self.__gridSize))
        self.__walls.append(pg.Rect(0*self.__gridSize, 9*self.__gridSize, 1*self.__gridSize, 7*self.__gridSize))
        self.__walls.append(pg.Rect(0*self.__gridSize, 16*self.__gridSize, 17*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(16*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize, 7*self.__gridSize))
        self.__walls.append(pg.Rect(16*self.__gridSize, 9*self.__gridSize, 1*self.__gridSize, 7*self.__gridSize))
        # Outer wall connected pieces:
        #   Left:
        self.__walls.append(pg.Rect(1*self.__gridSize, 6*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(1*self.__gridSize, 9*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(1*self.__gridSize, 14*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(3*self.__gridSize, 15*self.__gridSize, 4*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(5*self.__gridSize, 14*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        #   Middle:
        self.__walls.append(pg.Rect(8*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(8*self.__gridSize, 13*self.__gridSize, 1*self.__gridSize, 3*self.__gridSize))
        #   Right:
        self.__walls.append(pg.Rect(13*self.__gridSize, 6*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(13*self.__gridSize, 9*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(15*self.__gridSize, 14*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(10*self.__gridSize, 15*self.__gridSize, 4*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(11*self.__gridSize, 14*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        # Field pieces
        #   Left:
        self.__walls.append(pg.Rect(2*self.__gridSize, 2*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(2*self.__gridSize, 4*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(5*self.__gridSize, 2*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(5*self.__gridSize, 4*self.__gridSize, 1*self.__gridSize, 4*self.__gridSize))
        self.__walls.append(pg.Rect(5*self.__gridSize, 9*self.__gridSize, 1*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(5*self.__gridSize, 12*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(2*self.__gridSize, 12*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(3*self.__gridSize, 13*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        #   Middle:
        self.__walls.append(pg.Rect(7*self.__gridSize, 4*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(7*self.__gridSize, 10*self.__gridSize, 3*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(8*self.__gridSize, 11*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        #   Right:
        self.__walls.append(pg.Rect(10*self.__gridSize, 2*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(13*self.__gridSize, 2*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(13*self.__gridSize, 4*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(11*self.__gridSize, 4*self.__gridSize, 1*self.__gridSize, 4*self.__gridSize))
        self.__walls.append(pg.Rect(11*self.__gridSize, 9*self.__gridSize, 1*self.__gridSize, 2*self.__gridSize))
        self.__walls.append(pg.Rect(10*self.__gridSize, 12*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(13*self.__gridSize, 12*self.__gridSize, 2*self.__gridSize, 1*self.__gridSize))
        self.__walls.append(pg.Rect(13*self.__gridSize, 13*self.__gridSize, 1*self.__gridSize, 1*self.__gridSize))
        # Ghost box:
        self.__walls.append(pg.Rect(7*self.__gridSize, 7*self.__gridSize, 3*self.__gridSize, 2*self.__gridSize))

        self.__walls.append(pg.Rect(6*self.__gridSize, 14*self.__gridSize, 5*self.__gridSize, 2*self.__gridSize))


    @property
    def walls(self):
        return self.__walls

    def mapCollide(self, rect):
        for wall in self.__walls:
            if wall.colliderect(rect):
                return True
        return False

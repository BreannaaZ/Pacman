"""Pacman maze map for main game
@Author: Breanna Zinky
@Date: 12/3/2023
@Version: 1.0
"""

import os
import pygame as pg


class PacmanMap:
    """A class to store the walls of the map (list of rectangle objects)."""
    def __init__(self):
        """Class initializer code - Creates all the wall rectangles with their size and positions."""
        self.__walls = []  # Make a list of the walls
        self.__grid_size = 51  # Using a grid to easily plot the walls on the background map
        # Add all the map's walls
        # Outer walls:
        self.__walls.append(pg.Rect(0*self.__grid_size, 0*self.__grid_size, 17*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(0*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size, 7*self.__grid_size))
        self.__walls.append(pg.Rect(0*self.__grid_size, 9*self.__grid_size, 1*self.__grid_size, 7*self.__grid_size))
        self.__walls.append(pg.Rect(0*self.__grid_size, 16*self.__grid_size, 17*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(16*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size, 7*self.__grid_size))
        self.__walls.append(pg.Rect(16*self.__grid_size, 9*self.__grid_size, 1*self.__grid_size, 7*self.__grid_size))
        # Outer wall connected pieces:
        #   Left:
        self.__walls.append(pg.Rect(1*self.__grid_size, 6*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(1*self.__grid_size, 9*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(1*self.__grid_size, 14*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(3*self.__grid_size, 15*self.__grid_size, 4*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(5*self.__grid_size, 14*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        #   Middle:
        self.__walls.append(pg.Rect(8*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(8*self.__grid_size, 13*self.__grid_size, 1*self.__grid_size, 3*self.__grid_size))
        self.__walls.append(pg.Rect(6*self.__grid_size, 14*self.__grid_size, 5*self.__grid_size, 2*self.__grid_size))
        #   Right:
        self.__walls.append(pg.Rect(13*self.__grid_size, 6*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(13*self.__grid_size, 9*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(15*self.__grid_size, 14*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(10*self.__grid_size, 15*self.__grid_size, 4*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(11*self.__grid_size, 14*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        # Field pieces
        #   Left:
        self.__walls.append(pg.Rect(2*self.__grid_size, 2*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(2*self.__grid_size, 4*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(5*self.__grid_size, 2*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(5*self.__grid_size, 4*self.__grid_size, 1*self.__grid_size, 4*self.__grid_size))
        self.__walls.append(pg.Rect(5*self.__grid_size, 9*self.__grid_size, 1*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(5*self.__grid_size, 12*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(2*self.__grid_size, 12*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(3*self.__grid_size, 13*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        #   Middle:
        self.__walls.append(pg.Rect(7*self.__grid_size, 4*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(7*self.__grid_size, 10*self.__grid_size, 3*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(8*self.__grid_size, 11*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        #   Right:
        self.__walls.append(pg.Rect(10*self.__grid_size, 2*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(13*self.__grid_size, 2*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(13*self.__grid_size, 4*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(11*self.__grid_size, 4*self.__grid_size, 1*self.__grid_size, 4*self.__grid_size))
        self.__walls.append(pg.Rect(11*self.__grid_size, 9*self.__grid_size, 1*self.__grid_size, 2*self.__grid_size))
        self.__walls.append(pg.Rect(10*self.__grid_size, 12*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(13*self.__grid_size, 12*self.__grid_size, 2*self.__grid_size, 1*self.__grid_size))
        self.__walls.append(pg.Rect(13*self.__grid_size, 13*self.__grid_size, 1*self.__grid_size, 1*self.__grid_size))
        # Ghost box:
        self.__walls.append(pg.Rect(7*self.__grid_size, 7*self.__grid_size, 3*self.__grid_size, 2*self.__grid_size))

    # Properties for attributes
    @property
    def walls(self):
        return self.__walls

    def mapCollide(self, rect):
        """Checks for a collision between any of the walls and the given rectangle object.

        Args:
            rect: A rectangle game object, with a size and position.
        """
        for wall in self.__walls:
            if wall.colliderect(rect):
                return True
        return False

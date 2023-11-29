import os
import pygame as pg
import pygame.draw

from pacmanmap import *


class Consumable(pg.sprite.Sprite):
    def __init__(self, value, image):
        """Class initializer code."""
        super(Consumable, self).__init__()  # Call sprite initializer
        # Instance variables
        self.__consumed = False
        self.__value = value
        self.__image = image
        self.__rect = self.__image.get_rect()

    # PROPERTIES FOR NON PUBLIC ATTRIBUTES
    @property
    def consumed(self):
        return self.__consumed

    @consumed.setter
    def consumed(self, newConsumed):
        self.__consumed = newConsumed

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):
        self.__value = newValue

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, newImage):
        self.__image = newImage

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, newRect):
        self.__rect = newRect

    def draw(self, screen):
        """Draws the consumable onto the screen only if not consumed"""
        if not self.__consumed:
            screen.blit(self.__image, self.__rect)

    def consume(self, rect):
        """Checks for collision of the consumable and given rect (player). Returns
        the value of the consumable if it has been collided with (consumed)."""
        if self.__rect.colliderect(rect):
            self.__consumed = True
            points = self.__value
            self.__value = 0
            return points
        else:
            return 0

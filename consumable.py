"""Consumable game object
@Author: Breanna Zinky
@Date: 12/3/2023
@Version: 1.0
"""

import os
import pygame as pg
import pygame.draw
from pacmanmap import *


class Consumable(pg.sprite.Sprite):
    """A game object with an image and value that can be consumed by the player
    when collided with.
    """

    def __init__(self, value, image, centerx, centery):
        """Class initializer code.

        Args:
            value: The points value to be gained by consuming this object.
            image: The image to be displayed for this object.
            centerx: The x coordinate for this object.
            centery: The y coordinate for this object.
        """
        super(Consumable, self).__init__()  # Call sprite initializer
        # Instance variables
        self.__consumed = False
        self.__value = value
        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.centerx = centerx
        self.__rect.centery = centery

    # Properties for attributes
    @property
    def consumed(self):
        return self.__consumed

    @consumed.setter
    def consumed(self, newConsumed):
        if not newConsumed:
            raise ValueError("Consumed cannot be blank.")
        if not isinstance(newConsumed, bool):
            raise ValueError("Consumed must be a boolean.")
        self.__consumed = newConsumed

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):
        if not newValue:
            raise ValueError("Value cannot be blank.")
        if not isinstance(newValue, int):
            raise ValueError("Value must be an integer.")
        self.__value = newValue

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, newImage):
        if not newImage:
            raise ValueError("Image cannot be blank.")
        if not isinstance(newImage, pg.Surface):
            raise ValueError("Image must be a pygame surface object.")
        self.__image = newImage

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, newRect):
        if not newRect:
            raise ValueError("Rect cannot be blank.")
        if not isinstance(newRect, pg.Rect):
            raise ValueError("Rect must be a pygame rectangle object.")
        self.__rect = newRect

    def draw(self, screen):
        """Draws the consumable onto the screen only if not consumed.

        Args:
            screen: The pygame screen surface to draw to.
        """
        if not self.__consumed:
            screen.blit(self.__image, self.__rect)

    def consume(self, rect):
        """Checks for collision of the consumable and given rect (player).

        Args:
            rect: A rectangle game object, with a size and position.

        Returns:
            [Boolean, points]: A tuple which includes a boolean of whether the item was consumed or not,
            and the points to be gained from consuming the item.
        """
        points = self.__value
        if self.__rect.colliderect(rect):
            self.__consumed = True
            self.__value = 0
            return [True, points]
        else:
            return [False, points]

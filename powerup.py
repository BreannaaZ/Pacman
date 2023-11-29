import os
import pygame as pg
from pacmanmap import *
from consumable import *


class Powerup(Consumable):
    """A class to store the pellets for the player to collect"""

    def __init__(self, centerx, centery):
        """Class initializer code."""
        # Every powerup will have the same value and image; we can call consumable initializer with these
        # The super Consumable constructor initializes the value, picture, image, and consumed variables
        super().__init__(50, pg.image.load(os.path.join('assets', 'pacmanPowerUp.png')).convert_alpha())
        # NOT SURE if these two need to be made private
        self.rect.centerx = centerx
        self.rect.centery = centery

    def consume(self, rect):
        """Calls the consume method from super (consumable) to detect for a consumable collision and
        return the value of the consumed item. If the consumed object is a powerup, calls the powerUp method."""
        # Calls the powerUp method if the consumed object is the value of a powerup (since consume returns value)
        consumedValue = super().consume(rect)
        if consumedValue == self.value:
            self.powerUp()
        return consumedValue

    def powerUp(self):
        """Gives the player the powerUp ability - can kill ghosts for short interval of time"""
        pass

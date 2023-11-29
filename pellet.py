import os
import pygame as pg
from pacmanmap import *
from consumable import *


class Pellet(Consumable):
    """A class to store the pellets for the player to collect"""
    def __init__(self, centerx, centery):
        """Class initializer code."""
        # Every pellet will have the same value and image; we can call consumable initializer with these
        # The super Consumable constructor initializes the value, picture, image, and consumed variables
        super().__init__(10, pg.image.load(os.path.join('assets', 'PacmanCoin.png')).convert_alpha())
        # NOT SURE if these two need to be made private
        self.rect.centerx = centerx
        self.rect.centery = centery




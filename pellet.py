import os
import pygame as pg
from pacmanmap import *
from consumable import *


class Pellet(Consumable):
    """A class to store the pellets for the player to collect"""
    def __init__(self, centerx, centery):
        """Class initializer code."""
        # Every pellet will have the same value and image; we can call consumable initializer with these
        super().__init__(10, pg.image.load(os.path.join('assets', 'PacmanCoin.png')).convert_alpha(),
                         centerx, centery)





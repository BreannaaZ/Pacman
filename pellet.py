"""Pellet consumable for main game
@Author: Breanna Zinky
@Date: 12/3/2023
@Version: 1.0
"""

import os
import pygame as pg
from pacmanmap import *
from consumable import *


class Pellet(Consumable):
    """A class to store the pellets for the player to collect. Inherits from consumable."""
    def __init__(self, centerx, centery):
        """Class initializer code.

        Args:
            centerx: The x coordinate for this pellet object.
            centery: The y coordinate for this pellet object.
        """
        # Every pellet will have the same value and image; we can call consumable initializer with these
        super().__init__(10, pg.image.load(os.path.join('assets', 'PacmanCoin.png')).convert_alpha(),
                         centerx, centery)





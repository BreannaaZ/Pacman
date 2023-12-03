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
        super().__init__(50, pg.image.load(os.path.join('assets', 'pacmanPowerUp.png')).convert_alpha(),
                         centerx, centery)

    def powerUp(self, player, ghost, current_time, end_time):
        """Changes the ghost into a frightened state, and gives the player the powerUp ability
        for a short time interval."""
        if current_time < end_time:
            ghost.mode = "frightened"
            player.mode = "powered"
        else:
            ghost.mode = "normal"
            player.mode = "normal"
        ghost.changeMode()



"""Pacman ghost for main game
@Author: Breanna Zinky
@Date: 12/3/2023
@Version: 1.0
"""

import os
import pygame as pg
from pacmanmap import *
import random


class Ghost(pg.sprite.Sprite):
    """A class to store Ghost information."""

    def __init__(self, image, centerx, centery):
        """Class initializer code.

        Args:
            image: The starting image for the ghost
            centerx: The starting x coordinate for the ghost
            centery: The starting y coordinate for the ghost
        """
        super(Ghost, self).__init__()  # Call sprite initializer
        self.__original_image = image  # Need a starting image attribute separate from image for the ghost
        # to revert to after changing images
        self.__image = image
        self.__image = pg.transform.scale(self.__image, (46, 46))
        self.__rect = self.__image.get_rect()
        # Set ghost starting point
        self.__startX = centerx  # Again, need starting x and y for ghost to respawn at after being reinitialized
        self.__startY = centery
        self.__rect.centerx = centerx
        self.__rect.centery = centery
        # set directions
        self.__current_direction = random.choice(["right", "left", "up", "down"])  # Choose a random direction to start
        self.__possible_directions = []  # List to hold possible directions for ghost
        # Best direction is the next direction the ghost will go in
        self.__best_direction = self.__current_direction  # Initialize the best direction to starting direction
        self.__mode = "normal"  # Mode will control whether the ghost is in a normal or frightened state

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, newRect):
        self.__rect = newRect

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, newMode):
        self.__mode = newMode

    @property
    def original_image(self):
        return self.__original_image

    @property
    def startX(self):
        return self.__startX

    @property
    def startY(self):
        return self.__startY

    def draw(self, screen):
        """Draws the ghost to the screen"""
        screen.blit(self.__image, self.__rect)

    def move(self, walls, delta):
        """Allows the ghost to move continuously in a direction until a collision or better direction is detected

        Args:
            walls: The list of rectangles representing the map's walls.
            delta: Number scaled with time (time since last frame) to improve movement.
        """
        move_amount = 110 * delta  # Ghost will move slightly slower than the player
        self.getDirections(walls)  # Get possible directions
        self.chooseDirection()  # Choose a direction from possible ones
        self.__current_direction = self.__best_direction  # Move in chosen direction
        if self.__current_direction == "right":
            self.__rect.centerx += move_amount
        if self.__current_direction == "left":
            self.__rect.centerx -= move_amount
        if self.__current_direction == "up":
            self.__rect.centery -= move_amount
        if self.__current_direction == "down":
            self.__rect.centery += move_amount
        # Handle wraparound for "teleport" part of map
        if self.__rect.centerx < 0:  # Left-side
            self.__rect.centerx += 872
        if self.__rect.centerx > 872:  # Right-side
            self.__rect.centerx -= 872

    def getDirections(self, walls):
        """Finds all the possible directions for the ghost (directions with no collisions)
        and adds them to the possible directions list.

        Args:
            walls: The list of rectangles representing the map's walls.
        """
        # First clear the possible directions list
        del self.__possible_directions[:]
        new_rect = self.__rect.copy()  # Create a copy of the ghost's rect for testing
        # Check right direction for collision
        new_rect.x += 5
        if not walls.mapCollide(new_rect):
            # If no collision detected, add the direction to possible directions list
            self.__possible_directions.append("right")
        new_rect.x -= 5
        # Check left direction for collision
        new_rect.x -= 5
        if not walls.mapCollide(new_rect):
            # If no collision detected, add the direction to possible directions list
            self.__possible_directions.append("left")
        new_rect.x += 5
        # Check upwards direction for collision
        new_rect.y -= 5
        if not walls.mapCollide(new_rect):
            # If no collision detected, add the direction to possible directions list
            self.__possible_directions.append("up")
        new_rect.y += 5
        # Check downwards direction for collision
        new_rect.y += 5
        if not walls.mapCollide(new_rect):
            # If no collision detected, add the direction to possible directions list
            self.__possible_directions.append("down")
        new_rect.y -= 5

    def chooseDirection(self):
        """Chooses a random direction from the ghost's possible directions."""
        # Ghost movement algorithm:
        #   -If there is no collision in current_direction, proceed in current_direction
        #   -At a collision, if only one direction is valid (dead end) go in that direction (backwards)
        #   -At a collision, if more than one direction are valid, choose one at valid that isn't the direction
        #   that the ghost came from (this prevents "pacing" back and forth)
        if self.__current_direction in self.__possible_directions:  # Case: No collision on current direction
            # Keep moving in current direction
            self.__best_direction = self.__current_direction
        elif len(
                self.__possible_directions) == 1:  # If only backwards is valid, go backwards -
            # in this case possible directions will only have 1 item
            self.__best_direction = self.__possible_directions[0]
        elif len(self.__possible_directions) > 1:
            # If more than 2 directions are legal, choose the best or random direction that ISN'T the previous one
            # Remove the opposite/previous direction so the ghost won't bounce back and forth
            # Ex. if current direction = up, remove down from possible directions
            if self.__current_direction == "right" and "left" in self.__possible_directions:
                self.__possible_directions.remove("left")
            if self.__current_direction == "left" and "right" in self.__possible_directions:
                self.__possible_directions.remove("right")
            if self.__current_direction == "up" and "down" in self.__possible_directions:
                self.__possible_directions.remove("down")
            if self.__current_direction == "down" and "up" in self.__possible_directions:
                self.__possible_directions.remove("up")
            # Choose a direction at random
            self.__best_direction = random.choice(self.__possible_directions)

    def chooseBestDirection(self, player_centerx, player_centery):
        """Choose the best direction from the list of possible directions

        Args:
            player_centerx: The x coordinate for the center of the player rectangle
            player_centery: The y coordinate for the center of the player rectangle
        """
        # Best direction here is calculated as the direction that results in the least distance from player
        # Manhattan Distance Formula: abs(current_cell.x – goal.x) + abs(current_cell.y – goal.y)
        distanceFromPlayer = abs(self.__rect.centerx - player_centerx) + abs(self.__rect.centery - player_centery)
        leastDistance = distanceFromPlayer  # Initially set the least distance to the first distance calculated
        # Calculate distance from player in each possible direction first
        for direction in self.__possible_directions:
            if direction == "right":
                distanceFromPlayer = abs((self.__rect.centerx + 10) - player_centerx) + abs(
                    self.__rect.centery - player_centery)
            if direction == "left":
                distanceFromPlayer = abs((self.__rect.centerx - 10) - player_centerx) + abs(
                    self.__rect.centery - player_centery)
            if direction == "up":
                distanceFromPlayer = abs(self.__rect.centerx - player_centerx) + abs(
                    (self.__rect.centery - 10) - player_centery)
            if direction == "down":
                distanceFromPlayer = abs(self.__rect.centerx - player_centerx) + abs(
                    (self.__rect.centery + 10) - player_centery)
            if distanceFromPlayer < leastDistance:  # Check if this distance is smaller
                leastDistance = distanceFromPlayer  # Update distance
                self.__best_direction = direction  # Set best direction to this direction w/ the least distance

    def changeMode(self):
        """Changes the ghost's image depending on it's state (frightened or normal)"""
        if self.__mode == "frightened":
            self.__image = pg.image.load(os.path.join('assets', 'deadGhost.png')).convert_alpha()
        else:
            self.__image = self.__original_image
        self.__image = pg.transform.scale(self.__image, (46, 46))  # Scale image if needed

    def respawn(self, original_image, startX, startY):
        """Re-initializes the ghost with its original image and coordinates to respawn it.

        Args:
            original_image: The ghost's original image
            startX: The ghost's starting X coordinate
            startY: The ghost's starting Y coordinate
        """
        self.__init__(original_image, startX, startY)  # Reinitialize ghost with starting values to respawn it

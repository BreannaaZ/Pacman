import os
import pygame as pg
from pacmanmap import *
import math
import random


class Ghost(pg.sprite.Sprite):
    """A class to store Player (pacman) information."""

    def __init__(self, image, centerx, centery, start_direction):
        """Class initializer code."""
        super(Ghost, self).__init__()  # Call sprite initializer

        # Images and rect
        self.__image = image
        self.__image = pg.transform.scale(self.__image, (46, 46))  # Scale image if needed
        self.__rect = self.__image.get_rect()

        # Set ghost starting point
        self.__startX = centerx
        self.__startY = centery
        self.__rect.centerx = centerx
        self.__rect.centery = centery

        # set starting direction
        self.__start_direction = start_direction
        self.__current_direction = start_direction

        self.__possible_directions = []  # List to hold possible directions for ghost
        # Best direction will be the direction that reduces the ghost's distance to the player the most
        # out of the possible directions
        self.__best_direction = start_direction  # Initialize the best direction to starting direction

        # How ghost movement will work: Pseudo algorithm
        #   1. Determine possible directions for ghost
        #   2. Choose a direction that will make reduce the ghost's distance to player the most
        #   3. Move the ghost in that direction
        #   4. Handle collisions - at each collision find the possible directions

        # Other algorithm:
        #   1. If not moving, check possible directions, choose one at random
        #   2. If moving, continuously check possible directions
        #       -If only forwards/backwards is legal, continue forwards (straight line)
        #       -If only backwards is legal, go backwards (dead end)
        #       -If more than 2 directions are legal, choose one at random (junction)

        self.__time_interval = 5
        self.__index = 0
        self.__timer = 0

        self.__mode = "normal"  # Mode will control whether the ghost is in a normal state - to path towards the
        # player - or whether the ghost is frightened and should run from the player

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
    def image(self):
        return self.__image

    @property
    def startX(self):
        return self.__startX

    @property
    def startY(self):
        return self.__startY

    @property
    def start_direction(self):
        return self.__start_direction

    def draw(self, screen):
        """Draws the ghost to the screen"""
        # Draw ghost to screen
        screen.blit(self.__image, self.__rect)

    def move(self, walls, delta, player_centerx, player_centery):
        """Allows the ghost to move continuously in a direction until a collision or better direction is detected"""
        move_amount = 94 * delta  # Ghost will move slightly slower than the player
        self.getDirections(walls)  # Get possible directions
        self.chooseDirection(delta, walls, player_centerx, player_centery)  # Choose a direction from possible ones
        self.__current_direction = self.__best_direction  # Move in chosen direction
        if self.__current_direction == "right":
            self.__rect.centerx += move_amount
        if self.__current_direction == "left":
            self.__rect.centerx -= move_amount
        if self.__current_direction == "up":
            self.__rect.centery -= move_amount
        if self.__current_direction == "down":
            self.__rect.centery += move_amount

    def checkDirection(self, direction, walls):
        """Checks for a map collision in the given direction, returning true if there is no collision"""
        new_rect = self.__rect.copy()  # Create a copy of the player's rect for testing
        if direction == "right":
            new_rect.x += 6  # Move a small distance to check for collisions on the right
        elif direction == "left":
            new_rect.x -= 6  # Move a small distance to check for collisions on the left
        elif direction == "up":
            new_rect.y -= 6  # Move a small distance to check for collisions upward
        elif direction == "down":
            new_rect.y += 6  # Move a small distance to check for collisions downward
        if not walls.mapCollide(new_rect):  # Check for collision with the new direction
            return True  # Update the player's rect only if no collision detected

    def getDirections(self, walls):
        """Finds all the possible directions for the ghost (directions with no collisions)"""
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
        new_rect.y -= 6

    def chooseDirection(self, delta, walls, player_centerx, player_centery):
        """Chooses a random direction from the ghost's possible directions"""
        if self.checkDirection(self.__current_direction,
                               walls):  # Case: No collision on current direction AND no better direction
            # Keep moving in current direction
            self.__best_direction = self.__current_direction
        # Case 2: No collision on current direction BUT better direction found
        # if self.checkDirection(self.__current_direction, walls) and ?
        # Case 3: Collision on current direction
        elif len(
                self.__possible_directions) == 1:  # If only backwards is valid, go backwards - in this case possible directions will only have 1 item
            self.__best_direction = self.__possible_directions[0]
        elif len(self.__possible_directions) > 1:
            # If more than 2 directions are legal, choose the best or random direction that ISN'T the previous one
            # So it won't bounce back and forth
            # Ex. if current direction = up, remove down from possible directions
            if self.__current_direction == "right" and "left" in self.__possible_directions:
                self.__possible_directions.remove("left")
            if self.__current_direction == "left" and "right" in self.__possible_directions:
                self.__possible_directions.remove("right")
            if self.__current_direction == "up" and "down" in self.__possible_directions:
                self.__possible_directions.remove("down")
            if self.__current_direction == "down" and "up" in self.__possible_directions:
                self.__possible_directions.remove("up")
            # Use a timer to swap the ghost between pathing directly towards the player and moving randomly
            self.__timer += delta
            if self.__timer >= self.__time_interval:
                self.__timer = 0
                self.chooseBestDirection(player_centerx, player_centery)
            else:
                self.__best_direction = random.choice(
                    self.__possible_directions)  # Choose a random direction from possible directions

    def chooseBestDirection(self, player_centerx, player_centery):
        """Choose the best direction from the list of possible directions"""
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
            self.__best_direction = direction  # Set best direction to this direction w/ the least distance

    def changeMode(self):
            if self.__mode == "frightened":
                self.__image = pg.image.load(os.path.join('assets', 'deadGhost.png')).convert_alpha()
            else:
                self.__image = pg.image.load(os.path.join('assets', 'blueGhost.png')).convert_alpha()
            self.__image = pg.transform.scale(self.__image, (46, 46))  # Scale image if needed


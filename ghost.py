import os
import pygame as pg
from pacmanmap import *
import math


class Ghost(pg.sprite.Sprite):
    """A class to store Player (pacman) information."""

    def __init__(self, image, dead_ghost_image, centerx, centery, start_direction):
        """Class initializer code."""
        super(Ghost, self).__init__()  # Call sprite initializer

        # Images and rect
        self.__image = image
        self.__deadGhostImage = dead_ghost_image
        #self.__deadGhostImage.clamp_ip(self.__rect)  # Ties dead ghost image to ghost's rect
        self.__image = pg.transform.scale(self.__image, (46, 46)) # Scale image if needed
        self.__rect = self.__image.get_rect()

        # Set ghost starting point
        self.__rect.centerx = centerx
        self.__rect.centery = centery

        # set starting direction
        self.__current_direction = start_direction
        # self.__new_direction = startDirection
        # self.__changedDirection = False

        self.__possible_directions = []  # List to hold possible directions for ghost
        # Best direction will be the direction that reduces the ghost's distance to the player the most
        # out of the possible directions
        self.__best_direction = start_direction  # Initialize the best direction to starting direction

        # How ghost movement will work: Pseudo algorithm
        #   1. Determine possible directions for ghost
        #   2. Choose a direction that will make reduce the ghost's distance to player the most
        #   3. Move the ghost in that direction
        #   4. Handle collisions - at each collision find the possible directions

    def draw(self, screen):
        """Draws the ghost to the screen"""
        # Draw ghost to screen
        screen.blit(self.__image, self.__rect)

    def move(self, walls, delta, player_centerx, player_centery):
        """Allows the ghost to move continuously in a direction until a collision or better direction is detected"""
        move_amount = 94 * delta # Ghost will move slightly slower than the player
        self.getDirections(walls)
        self.chooseDirection(player_centerx, player_centery)
        if self.__current_direction == self.__best_direction and self.__current_direction in self.__possible_directions:  # Case: No collision on current direction, no better directions - keep moving in this direction
            if self.__current_direction == "right":
                self.__rect.centerx += move_amount
            if self.__current_direction == "left":
                self.__rect.centerx -= move_amount
            if self.__current_direction == "up":
                self.__rect.centery -= move_amount
            if self.__current_direction == "down":
                self.__rect.centery += move_amount
        elif (self.__best_direction != self.__current_direction
              or self.__current_direction not in self.__possible_directions):  # Case: Collision on current direction or better direction found
            # - move in the best direction out of possible directions
            if self.__best_direction == "right":
                self.__rect.centerx += move_amount
            if self.__best_direction == "left":
                self.__rect.centerx -= move_amount
            if self.__best_direction == "up":
                self.__rect.centery -= move_amount
            if self.__best_direction == "down":
                self.__rect.centery += move_amount

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

    def chooseDirection(self, player_centerx, player_centery):
        """Choose the best direction from the list of possible directions"""
        # Best direction here is calculated as the direction that results in the least distance from player
        # Distance between two points formula: d=√((x2 – x1)² + (y2 – y1)²)
        distanceFromPlayer = (
            math.sqrt((self.__rect.centerx - player_centerx) ** 2 + (self.__rect.centery - player_centery) ** 2))
        # OR TRY MANHATTAN DISTANCE
        # h = abs(current_cell.x – goal.x) + abs(current_cell.y – goal.y)
        distanceFromPlayer = abs(self.__rect.centerx - player_centerx) + abs(self.__rect.centery - player_centery)

        leastDistance = distanceFromPlayer  # Initially set the least distance to the first distance calculated

        # Calculate distance from player in each possible direction first
        for direction in self.__possible_directions:
            if direction == "right":
                distanceFromPlayer = math.sqrt(
                    ((self.__rect.centerx + 10) - player_centerx) ** 2 + (self.__rect.centery - player_centery) ** 2)
            if direction == "left":
                distanceFromPlayer = math.sqrt(
                    ((self.__rect.centerx - 10) - player_centerx) ** 2 + (self.__rect.centery - player_centery) ** 2)
            if direction == "up":
                distanceFromPlayer = math.sqrt(
                    (self.__rect.centerx - player_centerx) ** 2 + ((self.__rect.centery - 10) - player_centery) ** 2)
            if direction == "down":
                distanceFromPlayer = math.sqrt(
                    (self.__rect.centerx - player_centerx) ** 2 + ((self.__rect.centery + 10) - player_centery) ** 2)
            if distanceFromPlayer < leastDistance:
                leastDistance = distanceFromPlayer
                self.__best_direction = direction  # Set best direction to this direction w/ the least distance
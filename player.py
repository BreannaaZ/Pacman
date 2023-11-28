import os
import pygame as pg
from pacmanmap import *


class Player(pg.sprite.Sprite):
    """A class to store Player (pacman) information."""

    def __init__(self):
        """Class initializer code."""
        super(Player, self).__init__()  # Call sprite initializer
        # Create pacman images (multiple for animation)
        self.__images = [pg.image.load(os.path.join('assets', 'Pacman1.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman2.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman3.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman4.png')).convert_alpha()]
        self.__image = self.__images[0]  # Initialize pacman image to first sprite
        # The following is for image animation
        self.__time_interval = 0.1
        self.__index = 0
        self.__timer = 0
        # Resize sprite
        self.__image = pg.transform.scale(self.__image, (46, 46))
        self.__rect = self.__image.get_rect()
        # Set player starting point
        self.__rect.centerx = 435
        self.__rect.centery = 485
        # set starting direction
        self.__current_direction = "right"
        self.__new_direction = "right"
        self.__changedDirection = False
        # Direction arrows
        self.__Arrow = pg.image.load(os.path.join('assets', 'arrow.png')).convert_alpha()
        self.__ArrowRect = self.__Arrow.get_rect()
        self.__lives = 3

    # PROPERTIES FOR NON PUBLIC ATTRIBUTES
    @property
    def rect(self):
        return self.__rect
    @rect.setter
    def rect(self, newRect):
        self.__rect = newRect

    def draw(self, screen):
        """Draws the player (pacman) and direction arrow to the screen,
        using direction variables to ensure the correct orientation of both"""
        # Draw player pacman - rotate depending on current direction
        if self.__current_direction == "right":
            screen.blit(self.__image, self.__rect)
        if self.__current_direction == "left":
            screen.blit(pg.transform.rotate(self.__image, 180), self.__rect)
        if self.__current_direction == "up":
            screen.blit(pg.transform.rotate(self.__image, 90), self.__rect)
        if self.__current_direction == "down":
            screen.blit(pg.transform.rotate(self.__image, 270), self.__rect)
        # Set position of arrow
        self.__ArrowRect.clamp_ip(self.__rect)  # Ties arrow to player image
        # Draw arrow - rotate depending on new direction to get correct orientation
        if self.__new_direction == "up":
            screen.blit(self.__Arrow, self.__ArrowRect)
        if self.__new_direction == "right":
            screen.blit(pg.transform.rotate(self.__Arrow, 270), self.__ArrowRect)
        if self.__new_direction == "down":
            screen.blit(pg.transform.rotate(self.__Arrow, 180), self.__ArrowRect)
        if self.__new_direction == "left":
            screen.blit(pg.transform.rotate(self.__Arrow, 90), self.__ArrowRect)

    def update(self, keys, delta):
        """Updates the player's direction depending on user input/keys pressed"""
        # Update keys and direction
        if keys[pg.K_s]:
            if self.__changedDirection:  # Only update previous direction when the player
                # actually starts moving in new direction
                self.__current_direction = self.__new_direction
            self.__new_direction = "down"
        if keys[pg.K_w]:
            if self.__changedDirection:
                self.__current_direction = self.__new_direction
            self.__new_direction = "up"
        if keys[pg.K_a]:
            if self.__changedDirection:
                self.__current_direction = self.__new_direction
            self.__new_direction = "left"
        if keys[pg.K_d]:
            if self.__changedDirection:
                self.__current_direction = self.__new_direction
            self.__new_direction = "right"

        # Update sprite image for animation
        self.__timer += delta
        if self.__timer >= self.__time_interval:
            self.__image = self.__images[self.__index]
            self.__index = (self.__index + 1) % len(self.__images)
            self.__timer = 0
            self.__image = pg.transform.scale(self.__image, (46, 46))

    def move(self, walls, delta):
        """Allows the player to move continuously in a direction until a collision is detected"""
        move_amount = 95 * delta
        if self.checkDirection(self.__new_direction, walls): # Case: No collision on new direction
            # Move in the new direction
            if self.__new_direction == "right":
                self.__rect.centerx += move_amount
            if self.__new_direction == "left":
                self.__rect.centerx -= move_amount
            if self.__new_direction == "up":
                self.__rect.centery -= move_amount
            if self.__new_direction == "down":
                self.__rect.centery += move_amount
            # Check if the player changed direction
            if self.__new_direction != self.__current_direction:
                self.__changedDirection = True
                self.__current_direction = self.__new_direction
        elif self.checkDirection(self.__current_direction, walls): # Case: Collision on new direction but not
            # the current direction
            self.__changedDirection = False
            # Keep moving in the current direction
            if self.__current_direction == "right":
                self.__rect.centerx += move_amount
            elif self.__current_direction == "left":
                self.__rect.centerx -= move_amount
            elif self.__current_direction == "up":
                self.__rect.centery -= move_amount
            elif self.__current_direction == "down":
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

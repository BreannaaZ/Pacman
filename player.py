"""Pacman player for main game
@Author: Breanna Zinky
@Date: 12/3/2023
@Version: 1.0
"""

import os
import pygame as pg
from pacmanmap import *


class Player(pg.sprite.Sprite):
    """A class to store Player (pacman) information."""
    __lives = 3

    def __init__(self):
        """Class initializer code. Sets the player images and starting position and direction."""
        super(Player, self).__init__()  # Call sprite initializer
        # Create pacman images (multiple for animation)
        self.__images = [pg.image.load(os.path.join('assets', 'Pacman1.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman2.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman3.png')).convert_alpha(),
                         pg.image.load(os.path.join('assets', 'Pacman4.png')).convert_alpha()]
        self.__image = self.__images[0]  # Initialize pacman image to first sprite
        self.__image = pg.transform.scale(self.__image, (46, 46)) # Resize image
        self.__rect = self.__image.get_rect() # Get the rectangle for the sprite
        # The following is for image animation and timing
        self.__time_interval = 0.1
        self.__index = 0
        self.__timer = 0
        # Set player starting point
        self.__rect.centerx = 435
        self.__rect.centery = 485
        # Set starting direction
        self.__current_direction = "right"
        self.__new_direction = "right"
        self.__changed_direction = False
        # Direction arrow
        self.__arrow = pg.image.load(os.path.join('assets', 'arrow.png')).convert_alpha()
        self.__arrow_rect = self.__arrow.get_rect()
        self.__mode = "normal" # Mode for powerup detection

    # Properties for attributes
    @property
    def rect(self):
        return self.__rect

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, newMode):
        self.__mode = newMode

    @property
    def lives(self):
        return self.__lives

    def draw(self, screen):
        """Draws the player (pacman) and direction arrow to the screen.

        Args:
            screen: The pygame screen surface to draw to.
        """
        # Draw player pacman - rotate depending on current direction
        if self.__current_direction == "right":
            screen.blit(self.__image, self.__rect)
        if self.__current_direction == "left":
            screen.blit(pg.transform.rotate(self.__image, 180), self.__rect)
        if self.__current_direction == "up":
            screen.blit(pg.transform.rotate(self.__image, 90), self.__rect)
        if self.__current_direction == "down":
            screen.blit(pg.transform.rotate(self.__image, 270), self.__rect)
        # Draw arrow - rotate depending on new direction to get correct orientation
        self.__arrow_rect.clamp_ip(self.__rect)  # Ties arrow to player image
        if self.__new_direction == "up":
            screen.blit(self.__arrow, self.__arrow_rect)
        if self.__new_direction == "right":
            screen.blit(pg.transform.rotate(self.__arrow, 270), self.__arrow_rect)
        if self.__new_direction == "down":
            screen.blit(pg.transform.rotate(self.__arrow, 180), self.__arrow_rect)
        if self.__new_direction == "left":
            screen.blit(pg.transform.rotate(self.__arrow, 90), self.__arrow_rect)

    def update(self, keys, delta, ghosts):
        """Updates the player's direction depending on user input/keys pressed.

        Args:
            keys: The key pressed by the user.
            delta: Number scaled with time (time since last frame) to improve movement.
            ghosts: The list of ghosts in the game.
        """
        # Update keys and direction
        if keys[pg.K_s]:
            if self.__changed_direction:  # Only update previous direction when the player
                # actually starts moving in new direction
                self.__current_direction = self.__new_direction
            self.__new_direction = "down"
        if keys[pg.K_w]:
            if self.__changed_direction:
                self.__current_direction = self.__new_direction
            self.__new_direction = "up"
        if keys[pg.K_a]:
            if self.__changed_direction:
                self.__current_direction = self.__new_direction
            self.__new_direction = "left"
        if keys[pg.K_d]:
            if self.__changed_direction:
                self.__current_direction = self.__new_direction
            self.__new_direction = "right"

        # Update sprite image for animation
        self.__timer += delta
        if self.__timer >= self.__time_interval:
            self.__image = self.__images[self.__index]
            self.__index = (self.__index + 1) % len(self.__images)
            self.__timer = 0
            self.__image = pg.transform.scale(self.__image, (46, 46))

        # Check for ghost collision
        for ghost in ghosts:
            if self.rect.colliderect(ghost.rect):
                if self.mode == "normal":
                    self.__init__()  # Reinitialize player to respawn/reset to default values
                    self.__lives -= 1  # Decrement lives count
                elif self.mode == "powered":
                    ghost.respawn(ghost.original_image, ghost.startX, ghost.startY)

    def move(self, walls, delta):
        """Allows the player to move continuously in a direction until a collision is detected.

        Args:
            walls: The list of rectangles representing the map's walls.
            delta: Number scaled with time (time since last frame) to improve movement.
        """
        move_amount = 130 * delta
        if self.checkDirection(self.__new_direction, walls):  # Case: No collision on new direction
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
                self.__changed_direction = True
                self.__current_direction = self.__new_direction
        elif self.checkDirection(self.__current_direction, walls):  # Case: Collision on new direction but not
            # the current direction
            self.__changed_direction = False
            # Keep moving in the current direction
            if self.__current_direction == "right":
                self.__rect.centerx += move_amount
            elif self.__current_direction == "left":
                self.__rect.centerx -= move_amount
            elif self.__current_direction == "up":
                self.__rect.centery -= move_amount
            elif self.__current_direction == "down":
                self.__rect.centery += move_amount
        # Handle wraparound for "teleport" part of map
        if self.__rect.centerx < 0:  # Left-side
            self.__rect.centerx += 872
        if self.__rect.centerx > 872:  # Right-side
            self.__rect.centerx -= 872

    def checkDirection(self, direction, walls):
        """Checks for a map collision in the given direction.

        Args:
            direction: A string representing the direction to check (left, right, up, or down).
            walls: The list of rectangles representing the map's walls.

        Returns:
            boolean - True if there is no collision between walls and given rectangle, false if there is.
        """
        new_rect = self.__rect.copy()  # Create a copy of the player's rect for testing
        # Move a small amount in given direction to check for a collision
        if direction == "right":
            new_rect.x += 6
        elif direction == "left":
            new_rect.x -= 6
        elif direction == "up":
            new_rect.y -= 6
        elif direction == "down":
            new_rect.y += 6
        if not walls.mapCollide(new_rect):  # Check for collision with the new direction
            return True  # Return true for no collision in given direction

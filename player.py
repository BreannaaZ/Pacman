import os
import pygame as pg
from pacmanmap import *


class Player(pg.sprite.Sprite):
    """A class to store Player (pacman) information."""
    def __init__(self):
        """Class initializer code."""
        super(Player, self).__init__()  # Call sprite initializer
        # Create pacman images (multiple for animation)
        self.images = [pg.image.load(os.path.join('assets', 'Pacman1.png')).convert_alpha(),
                       pg.image.load(os.path.join('assets', 'Pacman2.png')).convert_alpha(),
                       pg.image.load(os.path.join('assets', 'Pacman3.png')).convert_alpha(),
                       pg.image.load(os.path.join('assets', 'Pacman4.png')).convert_alpha()]
        self.image = self.images[0]  # Initialize pacman image to first sprite
        # The following is for image animation
        self.time_interval = 0.1
        self.index = 0
        self.timer = 0
        # Resize sprite
        self.image = pg.transform.scale(self.image, (46, 46))
        self.rect = self.image.get_rect()
        # Set player starting point
        self.rect.centerx = (435)
        self.rect.centery = (485)
        # set starting direction
        self.current_direction = "right"
        self.new_direction = "right"
        self.changedDirection = False
        # Direction arrows
        self.Arrow = pg.image.load(os.path.join('assets', 'arrow.png')).convert_alpha()
        self.ArrowRect = self.Arrow.get_rect()
        lives = 3

    def draw(self, screen):
        """Draws the player (pacman) and direction arrow to the screen,
        using direction variables to ensure the correct orientation of both"""
        # Draw player pacman - rotate depending on current direction
        if self.current_direction == "right":
            screen.blit(self.image, self.rect)
        if self.current_direction == "left":
            screen.blit(pg.transform.rotate(self.image, 180), self.rect)
        if self.current_direction == "up":
            screen.blit(pg.transform.rotate(self.image, 90), self.rect)
        if self.current_direction == "down":
            screen.blit(pg.transform.rotate(self.image, 270), self.rect)
        # Set position of arrow
        self.ArrowRect.clamp_ip(self.rect) # Ties arrow to player image
        # Draw arrow - rotate depending on new direction to get correct orientation
        if self.new_direction == "up":
            screen.blit(self.Arrow, self.ArrowRect)
        if self.new_direction == "right":
            screen.blit(pg.transform.rotate(self.Arrow, 270), self.ArrowRect)
        if self.new_direction == "down":
            screen.blit(pg.transform.rotate(self.Arrow, 180), self.ArrowRect)
        if self.new_direction == "left":
            screen.blit(pg.transform.rotate(self.Arrow, 90), self.ArrowRect)

    def update(self, keys, delta):
        """Updates the player's direction depending on user input/keys pressed"""
        # Update keys and direction
        if keys[pg.K_s]:
            if self.changedDirection: # Only update previous direction when the player
                                      # actually starts moving in new direction
                self.current_direction = self.new_direction
            self.new_direction = "down"
        if keys[pg.K_w]:
            if self.changedDirection:
                self.current_direction = self.new_direction
            self.new_direction = "up"
        if keys[pg.K_a]:
            if self.changedDirection:
                self.current_direction = self.new_direction
            self.new_direction = "left"
        if keys[pg.K_d]:
            if self.changedDirection:
                self.current_direction = self.new_direction
            self.new_direction = "right"

        # Update sprite image for animation
        self.timer += delta
        if self.timer >= self.time_interval:
            self.image = self.images[self.index]
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0
            self.image = pg.transform.scale(self.image, (46, 46))

    def move(self, walls, delta):
        """Allows the player to move continuously in a direction until a collision is detected"""
        if self.new_direction == "right":
            if self.checkDirection(self.new_direction, walls, delta): # Case: No collision on new direction
                self.rect.centerx += 95 * delta # Move in new direction
                if self.current_direction != "right": # Check if the player changed direction
                    self.changedDirection = True
                    self.current_direction = self.new_direction
            elif self.checkDirection(self.current_direction, walls, delta): # Case: Collision on the new direction
                                                                            # but not the previous direction
                self.changedDirection = False # Do not move in new direction
                # Keep moving in previous direction
                if self.current_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.current_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.current_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.current_direction == "down":
                    self.rect.centery += 95 * delta
        if self.new_direction == "left":
            if self.checkDirection(self.new_direction, walls, delta):
                self.rect.x -= 95 * delta
                if self.current_direction != "left":
                    self.changedDirection = True
                    self.current_direction = self.new_direction
            elif self.checkDirection(self.current_direction, walls, delta):
                self.changedDirection = False
                if self.current_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.current_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.current_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.current_direction == "down":
                    self.rect.centery += 95 * delta
        if self.new_direction == "up":
            if self.checkDirection(self.new_direction, walls, delta):
                self.rect.y -= 95 * delta
                if self.current_direction != "up":
                    self.changedDirection = True
                    self.current_direction = self.new_direction
            elif self.checkDirection(self.current_direction, walls, delta):
                self.changedDirection = False
                if self.current_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.current_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.current_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.current_direction == "down":
                    self.rect.centery += 95 * delta
        if self.new_direction == "down":
            if self.checkDirection(self.new_direction, walls, delta):
                self.rect.y += 95 * delta
                if self.current_direction != "down":
                    self.changedDirection = True
                    self.current_direction = self.new_direction
            elif self.checkDirection(self.current_direction, walls, delta):
                self.changedDirection = False
                if self.current_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.current_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.current_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.current_direction == "down":
                    self.rect.centery += 95 * delta

    def checkDirection(self, direction, walls, delta):
        """Checks for a map collision in the given direction, returning true if there is no collision"""
        new_rect = self.rect.copy()  # Create a copy of the player's rect for testing
        if direction == "right":
            new_rect.x += 6  # Move a small distance to check for collisions on the right
        elif direction == "left":
            new_rect.x -= 6  # Move a small distance to check for collisions on the left
        elif direction == "up":
            new_rect.y -= 6  # Move a small distance to check for collisions upward
        elif direction == "down":
            new_rect.y += 6  # Move a small distance to check for collisions downward
        if not walls.mapCollide(new_rect):  # Check for collision with the new direction
            return True # Update the player's rect only if no collision detected

    #def checkCollision(self, walls):
       # return walls.mapCollide(self)

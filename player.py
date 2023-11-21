import os
import pygame as pg
from pacmanmap import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()  # Call sprite initializer
        # Create pacman image
        self.image = pg.image.load(os.path.join('assets', 'pacman.png')).convert_alpha()
        # Resize sprite
        self.image = pg.transform.scale(self.image, (46, 46))
        self.rect = self.image.get_rect()
        self.rect.centerx = (435)
        self.rect.centery = (485)
        self.direction = "right"
        self.previous_direction = "right"
        self.changedDirection = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, keys):
        if keys[pg.K_s]:
            if self.changedDirection: # Only update previous direction when the player actually starts moving in new direction
                self.previous_direction = self.direction
            self.direction = "down"
        if keys[pg.K_w]:
            if self.changedDirection: # Only update previous direction when the player actually starts moving in new direction
                self.previous_direction = self.direction
            self.direction = "up"
        if keys[pg.K_a]:
            if self.changedDirection: # Only update previous direction when the player actually starts moving in new direction
                self.previous_direction = self.direction
            self.direction = "left"
        if keys[pg.K_d]:
            if self.changedDirection: # Only update previous direction when the player actually starts moving in new direction
                self.previous_direction = self.direction
            self.direction = "right"

# Change move function- make so WHEN no collision is detected in that direction, it will turn to that direction.
    # If a collision is detected in the new direction, but not previous direction, keep moving in previous direction
    def move(self, walls, delta):
        if self.direction == "right":
            if self.checkDirection(self.direction, walls, delta): # Case: No collision on new direction
                self.rect.centerx += 95 * delta
                if self.previous_direction != "right":
                    self.changedDirection = True
                    self.previous_direction = self.direction
            elif self.checkDirection(self.previous_direction, walls, delta): # Case: Collision on new direction but not previous direction
                self.changedDirection = False
                if self.previous_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.previous_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.previous_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.previous_direction == "down":
                    self.rect.centery += 95 * delta
        if self.direction == "left":
            if self.checkDirection(self.direction, walls, delta):
                self.rect.x -= 95 * delta
                if self.previous_direction != "left":
                    self.changedDirection = True
                    self.previous_direction = self.direction
            elif self.checkDirection(self.previous_direction, walls, delta):
                self.changedDirection = False
                if self.previous_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.previous_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.previous_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.previous_direction == "down":
                    self.rect.centery += 95 * delta
        if self.direction == "up":
            if self.checkDirection(self.direction, walls, delta):
                self.rect.y -= 95 * delta
                if self.previous_direction != "up":
                    self.changedDirection = True
                    self.previous_direction = self.direction
            elif self.checkDirection(self.previous_direction, walls, delta):
                self.changedDirection = False
                if self.previous_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.previous_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.previous_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.previous_direction == "down":
                    self.rect.centery += 95 * delta
        if self.direction == "down":
            if self.checkDirection(self.direction, walls, delta):
                self.rect.y += 95 * delta
                if self.previous_direction != "down":
                    self.changedDirection = True
                    self.previous_direction = self.direction
            elif self.checkDirection(self.previous_direction, walls, delta):
                self.changedDirection = False
                if self.previous_direction == "right":
                    self.rect.centerx += 95 * delta
                if self.previous_direction == "left":
                    self.rect.centerx -= 95 * delta
                if self.previous_direction == "up":
                    self.rect.centery -= 95 * delta
                if self.previous_direction == "down":
                    self.rect.centery += 95 * delta

    def checkDirection(self, direction, walls, delta):
        new_rect = self.rect.copy()  # Create a copy of the player's rect for testing
        # new_rect.inflate_ip(1, 1) # Make new rectangle slightly bigger than normal pacman rectangle

        if direction == "right":
            new_rect.x += 6  # Move a small distance to check for collisions on the right
        elif direction == "left":
            new_rect.x -= 6  # Move a small distance to check for collisions on the left
        elif direction == "up":
            new_rect.y -= 6  # Move a small distance to check for collisions upward
        elif direction == "down":
            new_rect.y += 6  # Move a small distance to check for collisions downward

        if not walls.mapCollide(new_rect):  # Check for collision with the new direction
            return True # self.rect = new_rect  # Update the player's rect only if no collision detected

    def checkCollision(self, walls):
        return walls.mapCollide(self)

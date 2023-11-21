import os
import pygame as pg
from player import *
from pacmanmap import *
from pygame.locals import *

# Set up pygame
pg.init()
screen = pg.display.set_mode((872, 872))
clock = pg.time.Clock()
running = True
delta = 0
clock.tick(60)  # Limit FPS to 60

# Create background map
background = pg.image.load(os.path.join('assets', 'pacmanMaze.png')).convert_alpha()
# Scale background image to fit screen window
# background = pg.transform.scale(background, screen.get_size())

# Create map walls
pacmanmap = PacmanMap()

# Create player
player = Player()

# core loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill([0, 0, 0]) # Set white screen
    screen.blit(background, (0,0)) # Set background display

    # Handle Input Events
    keys = pg.key.get_pressed()

    # Update Sprites
    player.update(keys)
    # Check if the target direction will result in a collision and handle movement
    # player.checkDirection(pacmanmap, delta)
    player.move(pacmanmap, delta)

    # Draw the whole scene
    player.draw(screen)
    # pg.draw.rect(screen, (0, 255, 0), player.rect)

    # Only move if collision is not detected
    # if not player.checkCollision(pacmanmap):
       # player.move(delta)

    # color in walls to see them
    for wall in pacmanmap.walls:
        pg.draw.rect(screen, (255, 0, 0), wall)

    # Flip buffer when drawing is done
    pg.display.flip()

    delta = clock.tick(60) / 1000.0 # Scale delta

pg.quit()

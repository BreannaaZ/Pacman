import os
import pygame as pg
from player import *
from pacmanmap import *
from pygame.locals import *
from pellet import *
from pygame.freetype import *
from consumable import *


# Note: Should this be made into a class instead?
def main():
    """Runs the game with a main game setup and core loop"""
    # Set up pygame
    pg.init()
    screen = pg.display.set_mode((872, 872))
    clock = pg.time.Clock()
    running = True
    delta = 0
    clock.tick(60)  # Limit FPS to 60

    # Score for player points
    score = 0

    # Start sound
    pg.mixer.music.load('./assets/MainTheme.wav')
    pg.mixer.music.play(-1)

    # Get font setup
    pg.font.init()
    font = pg.font.SysFont('ocraextended', 30)

    # Create background map
    background = pg.image.load(os.path.join('assets', 'PacmanMaze.png')).convert_alpha()
    # Scale background image to fit screen window
    # background = pg.transform.scale(background, screen.get_size())

    # Create map walls (pacmanmap is essentially an array of rectangles that fit the background map image)
    pacmanmap = PacmanMap()

    # Create all the pellets (using loops to more easily get the coordinates to add the pellets to the map)
    pellets = []
    for x in range(80, 300, 50):
        pellets.append(Pellet(75, x))
    for x in range(590, 700, 50):
        pellets.append(Pellet(75, x))
    for x in range(590, 700, 50):
        pellets.append(Pellet(785, x))
    for x in range(80, 200, 50):
        pellets.append(Pellet(385, x))
    for x in range(80, 200, 50):
        pellets.append(Pellet(485, x))
    for x in range(80, 750, 50):
        pellets.append(Pellet(635, x))
    for x in range(80, 300, 50):
        pellets.append(Pellet(785, x))
    for x in range(80, 750, 50):
        pellets.append(Pellet(230, x))
    for x in range(181, 600, 50):
        pellets.append(Pellet(335, x))
    for x in range(181, 600, 50):
        pellets.append(Pellet(535, x))
    for y in range(125, 200, 50):
        pellets.append(Pellet(y, 80))
    for y in range(280, 350, 50):
        pellets.append(Pellet(y, 80))
    for y in range(535, 635, 50):
        pellets.append(Pellet(y, 80))
    for y in range(635, 835, 50):
        pellets.append(Pellet(y, 80))
    for y in range(125, 200, 50):
        pellets.append(Pellet(y, 180))
    for y in range(280, 300, 50):
        pellets.append(Pellet(y, 180))
    for y in range(535, 635, 50):
        pellets.append(Pellet(y, 180))
    for y in range(635, 835, 50):
        pellets.append(Pellet(y, 180))
    for y in range(125, 200, 50):
        pellets.append(Pellet(y, 280))
    for y in range(635, 835, 50):
        pellets.append(Pellet(y, 280))
    for y in range(30, 300, 50):
        pellets.append(Pellet(y, 430))
    for y in range(585, 850, 50):
        pellets.append(Pellet(y, 430))

    # Calculate winning score by adding up pellets value and powerUps value
    winningScore = 0
    for pellet in pellets:
        winningScore += pellet.value

    # Create player
    player = Player()

    # Start core game loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill([0, 0, 0])  # Set white screen
        screen.blit(background, (0, 0))  # Set background display

        # Handle Input Events
        keys = pg.key.get_pressed()

        # Update Sprites
        player.update(keys, delta)
        # Check if the target direction will result in a collision and handle movement
        # player.checkDirection(pacmanmap, delta)
        player.move(pacmanmap, delta)

        # Draw the whole scene
        player.draw(screen)

        # Draw pellets
        for pellet in pellets:
            pellet.draw(screen)
            score += pellet.consume(player.rect)

        # Display score
        scoreText = "Score: "
        scoreText += str(score)
        scoreSurface = font.render(scoreText, False, [254, 254, 254])
        screen.blit(scoreSurface, (355, 0))

        # color in walls to see them
        # for wall in pacmanmap.walls:
        #    pg.draw.rect(screen, (255, 0, 0), wall)

        # Flip buffer when drawing is done
        pg.display.flip()

        delta = clock.tick(60) / 1000.0  # Scale delta

        # Check for win condition
        if score >= winningScore:
            print("Congrats! You won!")
            running = False


# Startup the main method to get things going.
if __name__ == "__main__":
    main()
    pg.quit()

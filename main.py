import os
import pygame as pg
from player import *
from pacmanmap import *
from pygame.locals import *
from pellet import *
from pygame.freetype import *
from consumable import *
from powerup import *
from ghost import *

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

    # Get lives icons
    livesIcon = pg.image.load(os.path.join('assets', 'Pacman3.png')).convert_alpha()
    livesIcon = pg.transform.scale(livesIcon, (30, 30))

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

    # Create powerups
    powerups = [Powerup(435, 180),
                Powerup(80, 790),
                Powerup(790, 790)]

    # Calculate winning score by adding up pellets value and powerUps value
    winningScore = 0
    for pellet in pellets:
        winningScore += pellet.value
    for powerup in powerups:
        winningScore += powerup.value

    powerup_end_time = 0

    # Create player
    player = Player()

    # Create ghosts
    blueGhost = Ghost(pg.image.load(os.path.join('assets', 'blueGhost.png')).convert_alpha(),
                      75, 590, "right")

    # Start core game loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill([0, 0, 0])  # Set white screen
        screen.blit(background, (0, 0))  # Set background display

        # Handle Input Events
        keys = pg.key.get_pressed()

        current_time = pg.time.get_ticks()

        # Update Sprites
        player.update(keys, delta, blueGhost) # Update player based on key input
        player.move(pacmanmap, delta)
        blueGhost.move(pacmanmap, delta, player.rect.centerx, player.rect.centery)

        # Draw the whole scene
        player.draw(screen)
        blueGhost.draw(screen)

        # Draw pellets
        for pellet in pellets:
            pellet.draw(screen)
            if pellet.consume(player.rect):
                score += pellet.value

        # Draw powerups
        for powerup in powerups:
            powerup.draw(screen)
            if powerup.consume(player.rect):
                score += powerup.value
                powerup_end_time = pg.time.get_ticks() + 9000  # display for 3 seconds

        if current_time < powerup_end_time:
            blueGhost.mode = "frightened"
            player.mode = "powered"
        else:
            blueGhost.mode = "normal"
            player.mode = "normal"
        blueGhost.changeMode()

        # Display score
        scoreText = "Score: "
        scoreText += str(score)
        scoreSurface = font.render(scoreText, False, [254, 254, 254])
        screen.blit(scoreSurface, (355, 0))

        # Display lives
        livesText = "LIVES"
        livesSurface = font.render(livesText, False, [254, 254, 254])
        screen.blit(livesSurface, (395, 780))

        # Icon positioning: (x, 780)
        if player.lives >= 1:
            screen.blit(livesIcon, (385, 815))
        if player.lives >= 2:
            screen.blit(livesIcon, (425, 815))
        if player.lives == 3:
            screen.blit(livesIcon, (465, 815))

        # Flip buffer when drawing is done
        pg.display.flip()

        delta = clock.tick(60) / 1000.0  # Scale delta

        # Check for loss condition
        if player.lives == 0:
            print("Game over")
            running = False

        # Check for win condition
        if score >= winningScore:
            print("Congrats! You won!")
            running = False


# Startup the main method to get things going.
if __name__ == "__main__":
    main()
    pg.quit()

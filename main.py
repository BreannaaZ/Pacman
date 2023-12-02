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

    # Create a grid of pellets covering the entire screen
    pellets = []
    for x in range(30, 872, 50):
        for y in range(30, 872, 50):
            pellets.append(Pellet(x, y))

    # Now remove any pellets that overlap the walls
    # List comprehension to set pellets to only the pellets not colliding with walls
    # newlist = [expression for item in iterable if condition == True]
    pellets = [pellet for pellet in pellets if not any(pellet.rect.colliderect(wall) for wall in pacmanmap.walls)]

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
    ghosts = [Ghost(pg.image.load(os.path.join('assets', 'blueGhost.png')).convert_alpha(),
                      75, 75, "right"),
              Ghost(pg.image.load(os.path.join('assets', 'orangeGhost.png')).convert_alpha(),
                      790, 75, "right"),
              Ghost(pg.image.load(os.path.join('assets', 'redGhost.png')).convert_alpha(),
                      435, 640, "right")]

    #blueGhost = Ghost(pg.image.load(os.path.join('assets', 'blueGhost.png')).convert_alpha(),
    #                  75, 590, "right")
    #OrangeGhost = Ghost(pg.image.load(os.path.join('assets', 'orangeGhost.png')).convert_alpha(),
    #                  75, 590, "right")
    #redGhost = Ghost(pg.image.load(os.path.join('assets', 'redGhost.png')).convert_alpha(),
    #                  75, 590, "right")

    # Start core game loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill([0, 0, 0])  # Set white screen
        screen.blit(background, (0, 0))  # Set background display

        # color in walls to see them
        # for wall in pacmanmap.walls:
        #    pg.draw.rect(screen, (255, 0, 0), wall)

        # Handle Input Events
        keys = pg.key.get_pressed()

        current_time = pg.time.get_ticks()

        # Update Sprites
        player.update(keys, delta, ghosts) # Update player based on key input
        player.move(pacmanmap, delta)
        for ghost in ghosts:
            ghost.move(pacmanmap, delta, player.rect.centerx, player.rect.centery)

        # Draw the whole scene
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        # Draw pellets
        for pellet in pellets:
            pellet.draw(screen)
            (consumed, points) = pellet.consume(player.rect)
            if consumed:
                score += points

        # Draw powerups
        for powerup in powerups:
            powerup.draw(screen)
            (consumed, points) = powerup.consume(player.rect)
            if consumed:
                score += points
                powerup_end_time = pg.time.get_ticks() + 9000  # display for 3 seconds
                powerups.remove(powerup)

        for ghost in ghosts:
            if current_time < powerup_end_time:
                ghost.mode = "frightened"
                player.mode = "powered"
            else:
                ghost.mode = "normal"
                player.mode = "normal"
            ghost.changeMode()

        # Display score
        scoreText = "SCORE: "
        scoreText += str(score)
        scoreSurface = font.render(scoreText, False, [254, 254, 254])
        screen.blit(scoreSurface, (355, 5))

        # Display lives
        livesText = "LIVES"
        livesSurface = font.render(livesText, False, [254, 254, 254])
        screen.blit(livesSurface, (390, 735))

        # Icon positioning: (x, 780)
        if player.lives >= 1:
            screen.blit(livesIcon, (380, 775))
        if player.lives >= 2:
            screen.blit(livesIcon, (420, 775))
        if player.lives == 3:
            screen.blit(livesIcon, (460, 775))

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

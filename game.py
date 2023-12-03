import os
import pygame as pg
from pygame.locals import *
from consumable import *
from pacmanmap import *
from player import *
from pellet import *
from powerup import *
from ghost import *


class Game:
    """A class to create the game with a main game setup and core game loop"""
    def __init__(self):
        """Class initializer code - sets up the game"""
        # Set up pygame
        pg.init()
        self.__screen = pg.display.set_mode((872, 872))
        self.__clock = pg.time.Clock()
        self.__running = True
        self.__delta = 0
        self.__clock.tick(60)  # Limit FPS to 60
        self.__score = 0

        # Start sound
        pg.mixer.music.load('./assets/MainTheme.wav')
        pg.mixer.music.play(-1)

        # Get font setup
        pg.font.init()
        self.__font = pg.font.SysFont('ocraextended', 30)

        # Get lives icons
        self.__livesIcon = pg.image.load(os.path.join('assets', 'Pacman3.png')).convert_alpha()
        self.__livesIcon = pg.transform.scale(self.__livesIcon, (30, 30))

        # Create background map
        self.__background = pg.image.load(os.path.join('assets', 'PacmanMaze.png')).convert_alpha()

        # Create map walls (pacmanmap is essentially an array of rectangles that fit the background map image)
        self.__pacmanmap = PacmanMap()

        # Create powerups
        self.__powerups = [Powerup(435, 180),
                           Powerup(80, 790),
                           Powerup(790, 790)]
        self.__powerup_end_time = 0

        # Create a grid of pellets covering the entire screen
        self.__pellets = []
        for x in range(30, 872, 50):
            for y in range(30, 872, 50):
                self.__pellets.append(Pellet(x, y))

        # Now remove any pellets that overlap the walls and powerups
        # List comprehension to set pellets list to only the pellets not colliding with walls/powerups
        self.__pellets = [pellet for pellet in self.__pellets if
                          not any(pellet.rect.colliderect(wall) for wall in self.__pacmanmap.walls)]
        self.__pellets = [pellet for pellet in self.__pellets if
                          not any(pellet.rect.colliderect(powerup) for powerup in self.__powerups)]

        # Calculate the winning score by adding up pellets value and powerups value;
        # A win occurs when all pellets and powerups are consumed.
        self.__winningScore = 0
        for pellet in self.__pellets:
            self.__winningScore += pellet.value
        for powerup in self.__powerups:
            self.__winningScore += powerup.value

        # Create player
        self.__player = Player()

        # Create ghosts
        self.__ghosts = [Ghost(pg.image.load(os.path.join('assets', 'blueGhost.png')).convert_alpha(),
                               75, 75),
                         Ghost(pg.image.load(os.path.join('assets', 'orangeGhost.png')).convert_alpha(),
                               790, 75),
                         Ghost(pg.image.load(os.path.join('assets', 'redGhost.png')).convert_alpha(),
                               75, 790),
                         Ghost(pg.image.load(os.path.join('assets', 'blackGhost.png')).convert_alpha(),
                               790, 790)]

    def play(self):
        # Start core game loop
        while self.__running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
            # Input events - key movement
            keys = pg.key.get_pressed()

            # Move player and ghost
            self.__player.move(self.__pacmanmap, self.__delta)
            for ghost in self.__ghosts:
                ghost.move(self.__pacmanmap, self.__delta, self.__player.rect.centerx, self.__player.rect.centery)

            # Update game state/elements
            current_time = pg.time.get_ticks()  # Get current time
            self.__player.update(keys, self.__delta, self.__ghosts)  # Update player based on key input
            for powerup in self.__powerups: # Update ghosts' and player's powerup state
                for ghost in self.__ghosts:
                    powerup.powerUp(self.__player, ghost, current_time, self.__powerup_end_time)

            # Check for loss condition
            if self.__player.lives == 0:
                print("Game over")
                self.__running = False
            # Check for win condition
            if self.__score >= self.__winningScore:
                print("Congrats! You won!")
                self.__running = False

            # Draw the whole scene
            # Draw background
            self.__screen.blit(self.__background, (0, 0))  # Set background display
            # Draw pellets
            for pellet in self.__pellets:
                pellet.draw(self.__screen)
                (consumed, points) = pellet.consume(self.__player.rect)
                if consumed:
                    self.__score += points
            # Draw powerups
            for powerup in self.__powerups:
                powerup.draw(self.__screen)
                (consumed, points) = powerup.consume(self.__player.rect)
                if consumed:
                    self.__score += points
                    self.__powerup_end_time = pg.time.get_ticks() + 9000  # display for 3 seconds
                    self.__powerups.remove(powerup)
            # Draw player
            self.__player.draw(self.__screen)
            # Draw ghosts
            for ghost in self.__ghosts:
                ghost.draw(self.__screen)
            # Display score
            scoreText = "SCORE: "
            scoreText += str(self.__score)
            scoreSurface = self.__font.render(scoreText, False, [254, 254, 254])
            self.__screen.blit(scoreSurface, (355, 0))
            # Display lives
            livesText = "LIVES"
            livesSurface = self.__font.render(livesText, False, [254, 254, 254])
            self.__screen.blit(livesSurface, (390, 745))
            # Draw lives icons
            if self.__player.lives >= 1:
                self.__screen.blit(self.__livesIcon, (380, 785))
            if self.__player.lives >= 2:
                self.__screen.blit(self.__livesIcon, (420, 785))
            if self.__player.lives == 3:
                self.__screen.blit(self.__livesIcon, (460, 785))

            # Flip buffer when drawing is done
            pg.display.flip()

            self.__delta = self.__clock.tick(60) / 1000.0  # Scale delta


def main():
    """Create and run a game instance"""
    game = Game()
    game.play()


# Startup the main method
if __name__ == "__main__":
    main()
    pg.quit()

import sys

import pygame

from game.game import Game

if __name__ == "__main__":
    game = Game()

    game.run()

    while game.running:
        game.loop()

    pygame.quit()
    sys.exit()

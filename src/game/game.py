import pygame
from pygame.locals import *
from pygame.time import Clock

from src.commons import COLOR_BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from src.gamestates import GameStateName
from src.gamestates.gamestate_manager import GameStateManager


class Game:
    def __init__(self):
        self.__running = False
        self.__clock = Clock()
        self.__delta = 0
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.state_manager = GameStateManager()
        self.state_manager.current_state = GameStateName.TITLE

        pygame.display.set_caption("Hello World")

    @property
    def running(self) -> bool:
        return self.__running

    def run(self):
        self.__running = True

    def __handle_events(self):
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT or keys_pressed[K_ESCAPE]:
                self.__running = False

        self.state_manager.current_state.handle_events()

    def __update(self):
        self.__delta = self.__clock.tick(FPS)
        self.state_manager.current_state.update_dt(self.__delta)

    def __draw(self):
        self.__screen.fill(COLOR_BLACK)
        self.state_manager.current_state.render()
        self.__screen.blit(self.state_manager.current_state.get_surface(), (0, 0))
        pygame.display.flip()

    def loop(self):
        self.__handle_events()
        self.__update()
        self.__draw()

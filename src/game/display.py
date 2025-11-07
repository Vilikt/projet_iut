import pygame
from pygame import Surface

from src.commons import SCREEN_WIDTH, SCREEN_HEIGHT


class Display:
    def __init__(self, game: "Game"):
        self.__game = game
        self.__screen = None
        self.__scale = 3

        self.resize_screen()

    @property
    def screen(self):
        return self.__screen

    @property
    def scale(self):
        return self.__scale

    def resize_screen(self):
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH * self.__scale, SCREEN_HEIGHT * self.__scale))

    def resize_gamestate_surface(self) -> Surface:
        width = self.__game.state_manager.current_state.get_surface().get_width()
        height = self.__game.state_manager.current_state.get_surface().get_height()
        gs_surface_resized = pygame.transform.scale(
            self.__game.state_manager.current_state.get_surface(),
            (width * self.scale, height * self.scale)
        )

        return gs_surface_resized

import pygame
from pygame import Surface

from src.commons import SCREEN_WIDTH, SCREEN_HEIGHT
from src.configuration import conf


class Display:
    def __init__(self, game: "Game"):
        self.__game = game
        self.__screen = None
        self.__scale = 1
        self.__monitor_info = pygame.display.get_desktop_sizes()
        self.__monitor_width, self.__monitor_height = self.__monitor_info[0]

        self.resize_screen()

    @property
    def screen(self):
        return self.__screen

    @property
    def scale(self):
        return self.__scale

    def resize_screen(self):
        """
        Crée une nouvelle instance de la Surface représentant l'écran, en fonction du mode d'affichage (fenêtré ou plein
        écran) et de la taille de la fenêtre.
        """
        if conf.full_screen:
            self.__screen = pygame.display.set_mode(
                (self.__monitor_width, self.__monitor_height),
                pygame.FULLSCREEN
            )
            self.__scale = int(self.__monitor_height / SCREEN_HEIGHT)
        else:
            self.__scale = conf.window_size
            self.__screen = pygame.display.set_mode((SCREEN_WIDTH * self.__scale, SCREEN_HEIGHT * self.__scale))

    def resize_gamestate_surface(self) -> Surface:
        width = self.__game.state_manager.current_state.get_surface().get_width()
        height = self.__game.state_manager.current_state.get_surface().get_height()
        gs_surface_resized = pygame.transform.scale(
            self.__game.state_manager.current_state.get_surface(),
            (width * self.scale, height * self.scale)
        )

        return gs_surface_resized

    def get_gamestate_surface_pos(self) -> tuple[int, int]:
        x, y = 0, 0

        if conf.full_screen:
            x = (self.__monitor_width - SCREEN_WIDTH * self.__scale) / 2
            y = (self.__monitor_height - SCREEN_HEIGHT * self.__scale) / 2

        return x, y
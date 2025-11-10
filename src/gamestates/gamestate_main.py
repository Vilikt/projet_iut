import pygame
from pygame import Surface, K_RETURN
from pygame.event import Event

from src.entities.player import Player
from src.commons import singleton, COLOR_BLACK
from src.gamestates.gamestate import GameState
from src.gamestates import GameStateName


@singleton
class GameStateMain(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.MAIN)

        self.__player = Player(5, 5)

    def handle_events(self, event: Event):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_RETURN]:
            print("pause")

        self.__player.handle_events()

    def update_dt(self, delta: float):
        self.__player.update_dt(delta)

    def render(self):
        self._game_state_surface.fill(COLOR_BLACK)
        self._game_state_surface.blit(self.__player.get_surface(), (self.__player.x, self.__player.y))

    def get_surface(self) -> Surface:
        return self._game_state_surface

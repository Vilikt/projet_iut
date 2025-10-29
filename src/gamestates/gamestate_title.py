import pygame.key
from pygame import K_RETURN, Color, Surface

from src.commons import singleton
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState


@singleton
class GameStateTitle(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.TITLE)

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_RETURN]:
            self.manager.current_state = GameStateName.MAIN

    def update_dt(self, delta: float):
        pass

    def render(self):
        self._game_state_surface.fill(Color(0, 255, 0))

    def get_surface(self) -> Surface:
        return self._game_state_surface

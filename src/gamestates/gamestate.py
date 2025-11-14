from abc import ABC

from pygame import Surface
from pygame.event import Event

from src.commons import SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.gameloop_interface import GameLoopInterface


class GameState(GameLoopInterface, ABC):
    def __init__(self, manager: "GameStateManager", name: "GameStateName"):
        self.manager = manager
        self.name = name

        self._game_state_surface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    @property
    def game(self):
        return self.manager.game

    def handle_events(self, event: Event):
        self.manager.game.hud.handle_events(event)

    def update_dt(self, delta: float):
        self.game.hud.update_dt(delta)

    def render(self):
        self.game.hud.render()
        self._game_state_surface.blit(self.game.hud.get_surface(), (0, 0))

    def get_surface(self) -> Surface:
        return self._game_state_surface

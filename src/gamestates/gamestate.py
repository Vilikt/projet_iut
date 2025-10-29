from abc import ABC, abstractmethod

from pygame import Surface

from src.game.gameloop_interface import GameLoopInterface
from src.commons import SCREEN_WIDTH, SCREEN_HEIGHT


class GameState(GameLoopInterface, ABC):
    def __init__(self, manager: "GameStateManager", name: "GameStateName"):
        self.manager = manager
        self.name = name

        self._game_state_surface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update_dt(self, delta: float):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def get_surface(self) -> Surface:
        pass

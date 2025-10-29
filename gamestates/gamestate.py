from abc import ABC, abstractmethod

from pygame import Surface

from game.gameloop_interface import GameLoopInterface


class GameState(GameLoopInterface, ABC):
    def __init__(self, manager: "GameStateManager"):
        self.manager = manager

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update_dt(self, delta: float):
        pass

    @abstractmethod
    def render(self, screen: Surface):
        pass

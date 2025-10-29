from abc import ABC, abstractmethod

from pygame import Surface


class GameLoopInterface(ABC):
    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update_dt(self, delta: float):
        pass

    @abstractmethod
    def render(self, screen: Surface):
        pass

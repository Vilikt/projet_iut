from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event


class GameLoopInterface(ABC):
    @abstractmethod
    def handle_events(self, event: Event):
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

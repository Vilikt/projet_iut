from pygame import Surface
from pygame.event import Event

from src.entities.entity import Entity


class TileSprite(Entity):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, properties):
        super().__init__(pos_x, pos_y, image)

        self.__properties = properties

    @property
    def properties(self) -> dict:
        return self.__properties

    @properties.setter
    def properties(self, props: dict):
        self.__properties = props

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        pass

    def render(self):
        pass

    def get_surface(self) -> Surface:
        pass

from abc import abstractmethod

from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite

from src.commons.animation import Animation
from src.entities import EntityState
from src.game.gameloop_interface import GameLoopInterface


class Entity(Sprite, GameLoopInterface):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, collision_box: Rect = None, level: "Level" = None):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y

        self._animations: dict[EntityState, Animation | None] = {
            state: None
            for state in list(EntityState)
        }

        self.__current_state = None
        self.__current_animation: Animation | None = None

        self._current_level = level

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = value
        self.rect.x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = value
        self.rect.y = value

    @property
    def current_animation_image(self) -> Surface:
        return self.__current_animation.current_image

    @abstractmethod
    def handle_events(self, event: Event):
        pass

    def update(self, *args, **kwargs):
        self.update_dt(args[0])

    @abstractmethod
    def update_dt(self, delta: float):
        pass

    @abstractmethod
    def render(self):
        pass

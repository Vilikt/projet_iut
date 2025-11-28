import pygame.math
from pygame import Surface, Rect
from pygame.event import Event

from src.commons import FPS
from src.entities import DIRECTION_RIGHT
from src.entities.entity import Entity

GRAVITY = 7 / 32  # 0.21875 pixels/frame


class AliveEntity(Entity):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, collision_rect: Rect, level: "Level" = None):
        super().__init__(pos_x, pos_y, image, collision_rect, level)

        self._current_direction = pygame.math.Vector2(0, 0)
        self._current_side = DIRECTION_RIGHT

    @property
    def is_moving_right(self) -> bool:
        return self._current_direction.x > 0

    @property
    def is_moving_left(self) -> bool:
        return self._current_direction.x < 0

    @property
    def is_moving_up(self) -> bool:
        return self._current_direction.y < 0

    @property
    def is_moving_down(self) -> bool:
        return self._current_direction.y > 0

    @property
    def is_moving_horizontally(self) -> bool:
        return abs(self._current_direction.x) > 0.01

    @property
    def current_side(self) -> str:
        return self._current_side

    @current_side.setter
    def current_side(self, side: str):
        if self._current_side != side:
            self._current_side = side
            for entity_state, animation in self._animations.items():
                if animation is not None:
                    animation.change_direction()

    def _apply_gravity(self, factor: float):
        self._current_direction.y += GRAVITY * factor

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        FACTOR = (delta / 1000) * FPS

        self._apply_gravity(FACTOR)

        self.image = self.current_animation_image

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

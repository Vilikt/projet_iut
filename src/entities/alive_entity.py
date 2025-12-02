import pygame
from pygame import Surface, Rect
from pygame.event import Event

from src.commons import FPS
from src.entities import DIRECTION_RIGHT
from src.entities.entity import Entity
from src.mylogging import logger

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

    @property
    def is_in_air(self) -> bool:
        return abs(self._current_direction.y) > 0

    def _apply_gravity(self, factor: float):
        self._current_direction.y += GRAVITY * factor

    def handle_events(self, event: Event):
        pass

    def __vertical_movement_collision(self, factor: float):
        logger.debug("Début __vertical_movement_collision")

        self.y += self._current_direction.y * factor

        for sprite in self._current_level.collidable_sprites:
            if sprite.rect.colliderect(self.collision_box.inflate(0, 1)):
                if self.is_moving_up:
                    logger.debug("collision vers le haut")
                    self.collision_box_up = sprite.rect.bottom
                    # On applique une mini force vers le bas pour éviter de rester collé si Mario heurte quelque chose.
                    self._current_direction.y = 0.01
                elif self.is_moving_down:
                    logger.debug("collision vers le bas")
                    self.collision_box_down = sprite.rect.top
                    self._current_direction.y = 0

        logger.debug("Fin __vertical_movement_collision")

    def __horizontal_movement_collision(self, factor: float):
        self.x += self._current_direction.x * factor

        for sprite in self._current_level.collidable_sprites:
            if sprite.rect.colliderect(self.collision_box):
                if self.is_moving_left:
                    self.collision_box_left = sprite.rect.right
                elif self.is_moving_right:
                    self.collision_box_right = sprite.rect.left

    def update_dt(self, delta: float):
        logger.debug("Début update AliveEntity")
        super().update_dt(delta)

        FACTOR = (delta / 1000) * FPS

        self.__vertical_movement_collision(FACTOR)
        self.__horizontal_movement_collision(FACTOR)

        self.image = self.current_animation_image
        logger.debug("Fin update AliveEntity")

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

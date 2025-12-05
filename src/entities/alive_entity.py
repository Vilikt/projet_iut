import pygame
from pygame import Surface, Rect
from pygame.event import Event

from src.commons import FPS, RIGHT, get_collision_info, LEFT, UP, DOWN
from src.entities.entity import Entity
from src.entities.states import EntityStateName
from src.mylogging import logger

GRAVITY = 7 / 32  # 0.21875 pixels/frame


class AliveEntity(Entity):
    def __init__(self, name: str, pos_x: int = 0, pos_y: int = 0, image: Surface = None, collision_rect: Rect = None, level: "Level" = None):
        super().__init__(name, pos_x, pos_y, image, collision_rect, level)

        self._current_direction = pygame.math.Vector2(0, 0)
        self._current_side = RIGHT

        self.__can_jump = False

    @property
    def can_jump(self) -> bool:
        return self.__can_jump

    @can_jump.setter
    def can_jump(self, value: bool):
        self.__can_jump = value

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
        return self.current_state.is_in_air()

    def _apply_gravity(self, factor: float):
        self._current_direction.y += GRAVITY * factor

    def handle_events(self, event: Event):
        pass

    def __vertical_movement_collision(self, factor: float):
        logger.debug("Début __vertical_movement_collision")

        self.y += self._current_direction.y * factor

        for sprite in self._current_level.collidable_sprites:
            side, overlap_rect = get_collision_info(self.collision_box.inflate(0, 1), sprite.rect)
            if side is not None:
                collide_event = False

                if side == UP:
                    logger.debug("collision vers le haut")

                    if overlap_rect.width <= 4:
                        if self.x < sprite.x:
                            self.x -= 1
                        elif self.x > sprite.x:
                            self.x += 1
                    else:
                        collide_event = True
                        self.collision_box_up = sprite.rect.bottom
                        # On applique une mini force vers le bas pour éviter de rester collé si Mario heurte quelque chose.
                        self._current_direction.y = 0.01
                elif side == DOWN:
                    logger.debug("collision vers le bas")
                    if not self.is_current_state(EntityStateName.ASCENDING):
                        self.collision_box_down = sprite.rect.top
                        self._current_direction.y = 0

                if collide_event:
                    sprite.on_collide(self, side, overlap_rect)

        logger.debug("Fin __vertical_movement_collision")

    def __horizontal_movement_collision(self, factor: float):
        logger.debug("Début __horizontal_movement_collision")

        self.x += self._current_direction.x * factor

        for sprite in self._current_level.collidable_sprites:
            side, overlap_rect = get_collision_info(self.collision_box.inflate(1, 0), sprite.rect)
            if side is not None:
                if side == LEFT:
                    logger.debug(f"Collision du côté gauche")
                    self.collision_box_left = sprite.rect.right
                elif side == RIGHT:
                    logger.debug(f"Collision du côté droit")
                    self.collision_box_right = sprite.rect.left

                self._current_direction.x = 0
                if side in [LEFT, RIGHT]:
                    sprite.on_collide(self, side, overlap_rect)

        logger.debug("Fin __horizontal_movement_collision")

    def update_dt(self, delta: float):
        logger.debug("Début update AliveEntity")
        super().update_dt(delta)

        FACTOR = (delta / 1000) * FPS

        self._apply_gravity(FACTOR)

        self.__vertical_movement_collision(FACTOR)
        self.__horizontal_movement_collision(FACTOR)

        logger.debug("Fin update AliveEntity")

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

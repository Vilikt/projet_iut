from pygame import Rect, Surface

from src.commons.animation import Animation
from src.entities.entity import Entity
from src.entities.states import EntityStateName
from src.entities.states.stand import EntityStateStand
from src.entities.tiles.solid_sprite import SolidSprite


class AnimatedSolidSprite(SolidSprite):
    def __init__(self, name: str, pos_x: int, pos_y: int, animation: Animation, properties: dict = None, level: "Level" = None):
        super().__init__(name, pos_x, pos_y, animation.current_image, properties, level)

        self.add_state(EntityStateStand(self))
        self.add_animation(EntityStateName.STAND, animation)

        self.try_change_current_state(EntityStateName.STAND)

    def on_collide(self, entity: Entity, side: str, collision_rect: Rect):
        pass

    def update_dt(self, delta: float):
        self.current_animation.update(delta)
        self.image = self.current_animation_image

    def get_surface(self) -> Surface:
        return self.image

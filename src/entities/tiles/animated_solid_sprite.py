from pygame import Surface

from src.commons.animation import Animation
from src.entities.states import EntityStateName
from src.entities.states.stand import EntityStateStand
from src.entities.tiles.solid_sprite import SolidSprite


class AnimatedSolidSprite(SolidSprite):
    def __init__(self, name: str, pos_x: int, pos_y: int, animation: Animation, properties):
        super().__init__(name, pos_x, pos_y, animation.current_image, properties)

        self.add_state(EntityStateStand(self))
        self.add_animation(EntityStateName.STAND, animation)

        self.try_change_current_state(EntityStateName.STAND)

    def update_dt(self, delta: float):
        super().update_dt(delta)

    def get_surface(self) -> Surface:
        return super().get_surface()

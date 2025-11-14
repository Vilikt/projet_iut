from pygame import Surface

from src.commons.animation import Animation
from src.entities.tiles.solid_sprite import SolidSprite
from src.entities import EntityState


class AnimatedSolidSprite(SolidSprite):
    def __init__(self, pos_x: int, pos_y: int, animation: Animation, properties):
        super().__init__(pos_x, pos_y, animation.current_image, properties)

        self._animation = {
            EntityState.STAND: animation
        }

        self.current_state = EntityState.STAND

    def update_dt(self, delta: float):
        self._animation[self.current_state].update(delta)
        self.image = self._animation[self.current_state].current_image

    def get_surface(self) -> Surface:
        return self.image

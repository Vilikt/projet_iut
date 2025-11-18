from pygame import Surface

from src.entities.tiles.solid_sprite import SolidSprite


class BrickBlockSprite(SolidSprite):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, properties):
        super().__init__(pos_x, pos_y, image, properties)

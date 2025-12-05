from pygame import Surface, Rect

from src.entities.entity import Entity
from src.entities.tiles.tile_sprite import TileSprite


class SolidSprite(TileSprite):
    def __init__(self, name: str, pos_x: int, pos_y: int, image: Surface, properties):
        super().__init__(name, pos_x, pos_y, image, properties)

    def on_collide(self, entity: Entity, side: str, collision_rect: Rect):
        pass

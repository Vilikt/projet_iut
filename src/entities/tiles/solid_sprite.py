from pygame import Surface

from src.entities.tiles.tile_sprite import TileSprite


class SolidSprite(TileSprite):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, properties):
        super().__init__(pos_x, pos_y, image, properties)

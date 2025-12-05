from pygame import Surface, Rect

from src.commons import UP
from src.entities.entity import Entity
from src.entities.tiles.solid_sprite import SolidSprite
from src.entities.tiles import sm


class BrickBlockSprite(SolidSprite):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, properties: dict = None, level: "Level" = None):
        super().__init__("brick_block", pos_x, pos_y, image, properties, level)

        self.__hit = False
        self.__animation_frame = 0

    def on_collide(self, entity: Entity, side: str, collision_rect: Rect):
        if entity.name == "player" and side == UP and not self.__hit:
            self.__hit = True
            sm.get("bump").play()

    def update_dt(self, delta: float):
        if not self.__hit:
            return

        self.__animation_frame += 1

        if self.__animation_frame > 5:
            self.__animation_frame = 0
            self.__hit = False
            return

        if self.__animation_frame == 1:
            self.y -= 1
        if self.__animation_frame == 2:
            self.y -= 4
        if self.__animation_frame == 3:
            self.y += 1
        if self.__animation_frame == 4:
            self.y += 6
        if self.__animation_frame == 5:
            self.y -= 2

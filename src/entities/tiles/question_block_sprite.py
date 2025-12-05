from pygame import Rect
from pygame.event import Event

from src.commons import UP
from src.commons.animation import Animation
from src.commons.my_events import QUESTION_BLOCK_HIT
from src.entities.entity import Entity
from src.entities.tiles.animated_solid_sprite import AnimatedSolidSprite
from src.resources_manager.images_manager import ImagesManager


class QuestionBlockSprite(AnimatedSolidSprite):
    def __init__(self, pos_x: int, pos_y: int, animation: Animation, properties):
        if animation is None:
            msg = "Impossible de récupérer l'animation pour un QuestionBlock"
            raise ValueError(msg)

        super().__init__("question_block", pos_x, pos_y, animation, properties)

        self.__hit = False
        self.__empty_image = ImagesManager().get("block_empty")

        self.__animation_frame = 0

        self.__contain_object: Entity | None = None

    def on_collide(self, entity: Entity, side: str, collision_rect: Rect):
        if entity.name == "player" and side == UP and not self.__hit:
            self.__hit = True

            contain = self.properties.get("contain", None)
            if contain == "coin":
                pass

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        if not self.__hit:
            super().update_dt(delta)
            return

        self.__animation_frame += 1

        if self.__animation_frame > 19:
            return

        if self.__animation_frame == 1:
            self.y -= 1
            self.image = self.__empty_image
            if self.__contain_object is not None:
                self.__contain_object.y -= 4
        if self.__animation_frame == 2:
            self.y -= 4
        if self.__animation_frame == 3:
            self.y += 1
            if self.__contain_object is not None:
                self.__contain_object.y -= 12
        if self.__animation_frame == 4:
            self.y += 6
        if self.__animation_frame == 5:
            self.y -= 2
            if self.__contain_object is not None:
                self.__contain_object.y -= 8
        if self.__animation_frame == 6:
            pass
        if self.__animation_frame == 7:
            if self.__contain_object is not None:
                self.__contain_object.y -= 8
        if self.__animation_frame == 8:
            pass
        if self.__animation_frame == 9:
            if self.__contain_object is not None:
                self.__contain_object.y -= 2
        if self.__animation_frame == 11:
            if self.__contain_object is not None:
                self.__contain_object.y += 2
        if self.__animation_frame == 13:
            if self.__contain_object is not None:
                self.__contain_object.y += 8
        if self.__animation_frame == 15:
            if self.__contain_object is not None:
                self.__contain_object.y += 8
        if self.__animation_frame == 17:
            if self.__contain_object is not None:
                self.__contain_object.y += 16
        if self.__animation_frame == 19:
            if self.__contain_object is not None:
                self.__contain_object.kill()

    def render(self):
        pass

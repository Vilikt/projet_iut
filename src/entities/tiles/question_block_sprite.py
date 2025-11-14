from pygame.event import Event

from src.commons.animation import Animation
from src.commons.my_events import QUESTION_BLOCK_HIT
from src.entities.tiles.animated_solid_sprite import AnimatedSolidSprite
# from src.mylogging import logger
from src.resources_manager.images_manager import ImagesManager


class QuestionBlockSprite(AnimatedSolidSprite):
    def __init__(self, pos_x: int, pos_y: int, animation: Animation, properties):
        if animation is None:
            msg = "Impossible de récupérer l'animation pour un QuestionBlock"
            logger.error(msg)
            raise ValueError(msg)

        super().__init__(pos_x, pos_y, animation, properties)

        self.__hit = False
        self.__empty_image = ImagesManager().get("block_empty")

    def handle_events(self, event: Event):
        if event.type == QUESTION_BLOCK_HIT:
            if self is event.dict["sprite"]:
                self.__hit = True
                self.image = self.__empty_image

    def update_dt(self, delta: float):
        if not self.__hit:
            super().update_dt(delta)
            return

    def render(self):
        pass

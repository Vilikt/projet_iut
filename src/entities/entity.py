from abc import abstractmethod

from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite

from src.commons.animation import Animation
from src.entities.states import EntityStateName
from src.entities.states.state import EntityState
from src.game.gameloop_interface import GameLoopInterface
from src.mylogging import logger


class Entity(Sprite, GameLoopInterface):
    def __init__(self, pos_x: int, pos_y: int, image: Surface, collision_box: Rect = None, level: "Level" = None):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.__collision_box = collision_box

        self.x = pos_x
        self.y = pos_y

        self._states: list[EntityState] = []
        self._animations: dict[str, Animation | None] = {}

        self.__current_state = None
        self.__current_animation: Animation | None = None

        self._current_level = level

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value: int):
        self.rect.x = value
        self.__center_collision_box_on_image()

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value: int):
        self.rect.y = value
        self.__center_collision_box_on_image()

    @property
    def collision_box_up(self) -> int:
        return self.__collision_box.top

    @collision_box_up.setter
    def collision_box_up(self, value: int):
        if self.__collision_box is None:
            return

        self.__collision_box.top = value
        self.__center_image_on_collision_box()

    @property
    def collision_box_down(self) -> int:
        return self.__collision_box.top

    @collision_box_down.setter
    def collision_box_down(self, value: int):
        if self.__collision_box is None:
            return

        self.__collision_box.bottom = value
        self.__center_image_on_collision_box()

    @property
    def collision_box_left(self) -> int:
        return self.__collision_box.left

    @collision_box_left.setter
    def collision_box_left(self, value: int):
        if self.__collision_box is None:
            return

        self.__collision_box.left = value
        self.__center_image_on_collision_box()

    @property
    def collision_box_right(self) -> int:
        return self.__collision_box.right

    @collision_box_right.setter
    def collision_box_right(self, value: int):
        if self.__collision_box is None:
            return

        self.__collision_box.right = value
        self.__center_image_on_collision_box()

    @property
    def collision_box(self) -> Rect:
        return self.__collision_box

    @property
    def current_state(self) -> EntityState:
        return self.__current_state

    @property
    def current_animation(self) -> Animation:
        return self.__current_animation

    @current_animation.setter
    def current_animation(self, state: EntityStateName):
        if state.name not in self._animations.keys():
            raise KeyError(f"L'animation {state.name} n'existe pas pour l'entité {self}")

        if self.__current_animation != self._animations[state.name]:
            self.__current_animation = self._animations[state.name]

    @property
    def current_animation_image(self) -> Surface:
        return self.__current_animation.current_image

    def __center_image_on_collision_box(self):
        if self.__collision_box is None:
            return

        self.rect.left = int(self.__collision_box.left - ((self.rect.width - self.__collision_box.width) / 2))
        self.rect.bottom = self.__collision_box.bottom

    def __center_collision_box_on_image(self):
        if self.__collision_box is None:
            return

        self.__collision_box.left = int(self.rect.left + ((self.rect.width - self.__collision_box.width) / 2))
        self.__collision_box.bottom = self.rect.bottom

    def get_animation(self, state: EntityStateName) -> Animation | None:
        if state.name not in self._animations.keys():
            raise KeyError(f"L'animation {state} n'est pas déclarée pour l'entité {self}")

        if self._animations.get(state.name) is None:
            raise KeyError(f"L'animation {state} existe pour l'entité {self}, mais elle est None")

        return self._animations[state.name]

    def add_animation(self, state: EntityStateName, animation: Animation):
        logger.debug(f"Ajout de l'animation {state.name} pour l'entité {self}")
        self._animations[state.name] = animation

    def add_state(self, state: EntityState):
        if state in self._states:
            raise KeyError(f"L'état {state.name} existe déjà pour l'entité {self}")

        self._states.append(state)

    def try_change_current_state(self, state_name: EntityStateName):
        logger.debug(f"'try_change_current_state' de 'Entity' pour {self} -> vers {state_name.name}")

        if self.__current_state is not None:
            if self.__current_state.name == state_name:
                logger.debug(f"L'entité {self} est déjà à l'état {state_name.name}")
                logger.debug(f"Fin du Setter 'try_change_current_state' de 'Entity' pour {self}")
                return

        available_state_names = [state.name.name for state in self._states]
        if state_name.name not in available_state_names:
            raise KeyError(f"L'état {state_name} n'existe pas pour l'entité {self}")

        logger.debug(f"L'état {state_name.name} est bien défini pour l'entité '{self}'")

        for state in self._states:
            if state.name.name == state_name.name:
                self.__current_state = state
                self.current_animation = state.name
                logger.info(f"Passage vers : {state.name}")

        logger.debug(f"Fin de 'try_change_current_state' de 'Entity' pour {self}")

    def is_current_state(self, state_name: EntityStateName) -> bool:
        return self.__current_state.name.name == state_name.name

    @abstractmethod
    def handle_events(self, event: Event):
        pass

    def update(self, *args, **kwargs):
        self.update_dt(args[0])

    def update_dt(self, delta: float):
        logger.debug("Début update Entity")
        self.current_animation.update(delta)
        self.image = self.current_animation_image
        logger.debug("Fin update Entity")

    @abstractmethod
    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

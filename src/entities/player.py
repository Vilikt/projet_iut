import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from src.commons import SCREEN_HEIGHT, TILE_SIZE, FPS
from src.commons.my_events import post_event, MARIO_DEATH
from src.commons.timer import Timer
from src.entities.alive_entity import AliveEntity
from src.entities.states import EntityStateName
from src.entities.states.ascending import EntityStateAscending
from src.entities.states.descending import EntityStateDescending
from src.entities.states.falling import EntityStateFalling
from src.entities.states.running import EntityStateRunning
from src.entities.states.stand import EntityStateStand
from src.entities.states.turning import EntityStateTurning
from src.entities.states.walking import EntityStateWalking
from src.game.gameloop_interface import GameLoopInterface
from src.mylogging import logger
from src.resources_manager import am

MAX_FALL_SPEED = 3.5            # Vitesse maximale de chute.

TIME_BEFORE_RUNNING = 0.5       # Temps en secondes avant de passer en course.

MAX_JUMPING_FRAMES = 7          # La gravité sera annulée pendant ce nombre de frames.


class Player(AliveEntity, GameLoopInterface):
    def __init__(self, pos_x: int, pos_y: int, level: "Level" = None):
        super().__init__(pos_x, pos_y, Surface((TILE_SIZE, TILE_SIZE)), Rect(pos_x, pos_y, 12, 14), level)

        self.__score = 0
        self.__lives = 0
        self.__coins = 0

        # Créations des états
        self.add_state(EntityStateStand(self, [EntityStateName.WALKING, EntityStateName.ASCENDING]))
        self.add_state(EntityStateWalking(self,
                                          [EntityStateName.STAND, EntityStateName.ASCENDING, EntityStateName.RUNNING,
                                           EntityStateName.FALLING,
                                           EntityStateName.TURNING]))
        self.add_state(EntityStateRunning(self,
                                          [EntityStateName.WALKING, EntityStateName.ASCENDING, EntityStateName.FALLING,
                                           EntityStateName.TURNING, EntityStateName.STAND]))
        self.add_state(EntityStateFalling(self, [EntityStateName.STAND, EntityStateName.ASCENDING]))
        self.add_state(EntityStateDescending(self, [EntityStateName.STAND]))
        self.add_state(EntityStateAscending(self, [EntityStateName.DESCENDING]))
        self.add_state(EntityStateTurning(self, [EntityStateName.WALKING, EntityStateName.RUNNING]))

        # Créations des Animations
        self.add_animation(EntityStateName.STAND, am.get("mario_stand"))
        self.add_animation(EntityStateName.WALKING, am.get("mario_moving"))
        self.get_animation(EntityStateName.WALKING).change_speed(1000 / 60 * 4)
        self.add_animation(EntityStateName.RUNNING, am.get("mario_moving"))
        self.get_animation(EntityStateName.RUNNING).change_speed(1000 / 60 * 3)
        self.get_animation(EntityStateName.RUNNING).change_name("mario_run")
        self.add_animation(EntityStateName.TURNING, am.get("mario_turn"))
        self.get_animation(EntityStateName.TURNING).change_speed(1000 / 60 * 4)
        self.add_animation(EntityStateName.ASCENDING, am.get("mario_jump"))
        self.add_animation(EntityStateName.DESCENDING, am.get("mario_jump"))
        self.add_animation(EntityStateName.FALLING, am.get("mario_moving"))

        self.run_timer = Timer(time_to_wait=TIME_BEFORE_RUNNING * 1000, loop=False, auto_start=False)  # Temps en ms

        self.__keys_pressed = set()  # Pour suivre les touches enfoncées

        self.try_change_current_state(EntityStateName.STAND)

        self.__frame_no_gravity_counter = 0
        self.__coyote_frame_counter = 0
        self.__jump_buffer_counter = 0

        self.__was_jumping = False

    @property
    def lives(self) -> int:
        return self.__lives

    @lives.setter
    def lives(self, value: int):
        self.__lives = value

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value

    @property
    def coins(self) -> int:
        return self.__coins

    @coins.setter
    def coins(self, value: int):
        self.__coins = value

    def __is_key_press(self, key: int) -> bool:
        return key in self.__keys_pressed

    def __what_to_do_on_each_state(self, factor: float):
        if self.is_current_state(EntityStateName.STAND):
            self.__what_to_do_on_state_stand()
        elif self.is_current_state(EntityStateName.ASCENDING):
            self.__what_to_do_on_state_ascending(factor)
        elif self.is_current_state(EntityStateName.DESCENDING):
            self.__what_to_do_on_state_descending(factor)
        elif self.is_current_state(EntityStateName.WALKING):
            self.__what_to_do_on_state_walking(factor)
        elif self.is_current_state(EntityStateName.RUNNING):
            self.__what_to_do_on_state_running(factor)
        elif self.is_current_state(EntityStateName.FALLING):
            self.__what_to_do_on_state_falling(factor)

    def _apply_gravity(self, factor: float):
        logger.debug(f"Application de la gravité pour [{self}].")

        # Annulation de la gravité sur les 7 premières frames du saut.
        logger.debug(f"Compteur de frame sans gravité = {str(self.__frame_no_gravity_counter)}.")
        if self.is_current_state(EntityStateName.ASCENDING) and self.__frame_no_gravity_counter < MAX_JUMPING_FRAMES:
            logger.debug("Annulation de gravité.")
            self.__frame_no_gravity_counter += 1
            return
        else:
            logger.debug("La gravité n'est pas annulée.")

        super()._apply_gravity(factor)

        # Limitation de la vitesse de chute
        if self._current_direction.y > MAX_FALL_SPEED:
            logger.debug(f"La valeur du vecteur en Y est supérieur à MAX_FALL_SPEED ({MAX_FALL_SPEED}).")
            self._current_direction.y = MAX_FALL_SPEED
            logger.debug(f"On limite donc le vecteur en Y à {MAX_FALL_SPEED}.")

        logger.debug(f"Fin de l'application de la gravité pour [{self}].")

    def add_in_level(self, level: "Level"):
        self._current_level = level
        self._current_level.player_sprite.add(self)
        self._current_level.center_at = self

    def try_change_current_state(self, next_state_name: EntityStateName):
        logger.debug(f"'try_change_current_state' de 'Player' pour [{self}] -> vers {next_state_name.name}.")

        if self.current_state is not None:
            next_state_name = self.current_state.get_next_state(next_state_name)

        super().try_change_current_state(next_state_name)

        logger.debug(f"Fin de 'try_change_current_state' de 'Player' pour [{self}].")

    def handle_events(self, event: Event):
        if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
            return

        if event.type == pygame.KEYDOWN:
            self.__keys_pressed.add(event.key)
            logger.debug(f"Le bouton {event.key} vient d'être appuyé.")
        elif event.type == pygame.KEYUP:
            self.__keys_pressed.discard(event.key)
            logger.debug(f"Le bouton {event.key} vient d'être relâché.")

    def update_dt(self, delta: float):
        logger.debug("Début update Player.")
        logger.debug(f"La position de Mario est [{self.x}, {self.y}].")
        FACTOR = (delta / 1000) * FPS

        super().update_dt(delta)

        logger.debug(f"L'état courant est {self.current_state.name.name}.")

        # self.__handle_buttons(delta, friction_value)
        # self.__what_to_do_on_each_state(FACTOR)

        if self.y >= SCREEN_HEIGHT + TILE_SIZE:
            post_event(MARIO_DEATH)

        logger.debug("Fin update Player.")

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

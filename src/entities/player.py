import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from src.commons import SCREEN_HEIGHT, TILE_SIZE, FPS, LEFT, RIGHT
from src.commons.my_events import post_event, MARIO_DEATH
from src.commons.timer import Timer
from src.configuration import conf
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
from src.resources_manager import am, sm

# Constantes (valeurs exactes de SMB1, en pixels/frame)
WALK_ACCELERATION = 0.0625      # Accelération max en mode marche normale.
MAX_WALK_SPEED = 1.5            # Vitesse max en mode marche normale.
RUN_ACCELERATION = 0.1          # Accélération plus rapide en mode course
MAX_RUN_SPEED = 2.5             # Vitesse max en mode course
FRICTION = 0.125                # Valeur de la force de frottement
INITIAL_ACCELERATION = 0.5      # Accélération initiale.
JUMP_FORCE = -4.125             # Force initiale du saut (pixels/frame).
MAX_FALL_SPEED = 3.5            # Vitesse maximale de chute.
MIN_JUMP_SPEED = -1.0           # Vitesse minimale si le bouton est relâché tôt.

TIME_BEFORE_RUNNING = 0.5       # Temps en secondes avant de passer en mode course.

COYOTE_TIME = 4                 # Frames de "coyote time" après avoir quitter une plateforme.
JUMP_BUFFER = 2                 # Frames de "jump buffer" avant d'atterrir.
MAX_JUMPING_FRAMES = 7          # La gravité sera annulée pendant ce nombre de frames.


class Player(AliveEntity, GameLoopInterface):
    def __init__(self, pos_x: int = 0, pos_y: int = 0, level: "Level" = None):
        super().__init__("player", pos_x, pos_y, Surface((TILE_SIZE, TILE_SIZE)), Rect(pos_x, pos_y, 12, 14), level)

        self.__score = 0
        self.__lives = 0
        self.__coins = 0

        # Création des états
        self.add_state(EntityStateStand(self, [EntityStateName.WALKING, EntityStateName.ASCENDING]))
        self.add_state(EntityStateWalking(self,
            [EntityStateName.STAND, EntityStateName.ASCENDING, EntityStateName.RUNNING, EntityStateName.FALLING,
             EntityStateName.TURNING]))
        self.add_state(EntityStateRunning(self,
            [EntityStateName.WALKING, EntityStateName.ASCENDING, EntityStateName.FALLING, EntityStateName.TURNING, EntityStateName.STAND]))
        self.add_state(EntityStateFalling(self, [EntityStateName.STAND, EntityStateName.ASCENDING]))
        self.add_state(EntityStateDescending(self, [EntityStateName.STAND]))
        self.add_state(EntityStateAscending(self, [EntityStateName.DESCENDING]))
        self.add_state(EntityStateTurning(self, [EntityStateName.WALKING, EntityStateName.RUNNING]))

        # Ajout des Animations
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
        self.__can_count_jump_buffer_counter = False
        self.__on_jump_buffer = False
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

    @property
    def __is_direction_pressed(self) -> bool:
        return self.__is_key_press(conf.button_left) or self.__is_key_press(conf.button_right)

    @property
    def __in_coyote_time(self) -> bool:
        return self.__coyote_frame_counter < COYOTE_TIME and self.is_current_state(EntityStateName.FALLING)

    def __is_key_press(self, key: int) -> bool:
        return key in self.__keys_pressed

    def __move(self, factor: float):
        acceleration = 0
        speed_max = 0
        func = min

        if self.__is_direction_pressed:
            if not self.__is_key_press(conf.button_b) or not self.run_timer.finished:
                acceleration = WALK_ACCELERATION
                speed_max = MAX_WALK_SPEED
            else:
                acceleration = RUN_ACCELERATION
                speed_max = MAX_RUN_SPEED

        if self.__is_key_press(conf.button_right) and not self.__is_key_press(conf.button_left):
            func = min
        elif self.__is_key_press(conf.button_left) and not self.__is_key_press(conf.button_right):
            func = max
            acceleration *= -1
            speed_max *= -1

        self._current_direction.x += acceleration * factor
        self._current_direction.x = func(self._current_direction.x, speed_max)

    def __handle_button_a(self):
        if self.__is_key_press(conf.button_a) or self.__on_jump_buffer:
            if self.__is_key_press(conf.button_a):
                logger.debug("Le bouton A est appuyé.")
            if self.__on_jump_buffer:
                logger.debug("On est en jump_buffer")

            if (self.can_jump and not self.__was_jumping) or self.__in_coyote_time:
                logger.debug("Mario est au sol -> il peut sauter.")
                if self.__on_jump_buffer:
                    logger.debug("Et c'est grâce au jump_buffer")
                sm.get("jumpsmall").play()
                self.try_change_current_state(EntityStateName.ASCENDING)
                self.__was_jumping = True
                self.__on_jump_buffer = False
            else:
                logger.debug("Mario est en l'air -> il ne peut pas sauter.")
        if not self.__is_key_press(conf.button_a):
            logger.debug("Le bouton A n'est pas appuyé.")
            if not self.is_in_air:
                self.__was_jumping = False

    def __handle_buttons_directions_and_b(self, delta: float, friction_value: float):
        def apply_friction():
            logger.debug(f"On applique la friction.")
            if self._current_direction.x > 0:
                self._current_direction.x -= friction_value
                if self._current_direction.x <= 0:
                    self._current_direction.x = 0
            elif self._current_direction.x < 0:
                self._current_direction.x += friction_value
                if self._current_direction.x >= 0:
                    self._current_direction.x = 0

        if self.__is_direction_pressed:
            logger.debug("Une direction est appuyée -> on essaye de passer à l'état WALKING.")
            self.try_change_current_state(EntityStateName.WALKING)

            if not self.__is_key_press(conf.button_b):
                logger.debug("Le bouton B n'est pas appuyé -> on reset le timer de course.")
                self.run_timer.reset()
            else:
                logger.debug("Le bouton B est appuyé.")
                if not self.run_timer.running:
                    logger.debug("Le timer de course n'est pas en cours -> on le démarre.")
                    self.run_timer.start()
                self.run_timer.update(delta)
                if self.run_timer.finished:
                    logger.debug("Le timer de course est terminé -> on passe à l'état RUNNING.")
                    self.try_change_current_state(EntityStateName.RUNNING)

            if abs(self._current_direction.x) < 0.1:
                logger.debug("La force de mouvement horizontale est inférieure à 0.1")
                if self.__is_key_press(conf.button_left):
                    self.current_side = LEFT
                    logger.debug(f"On applique une accélération initiale de {-INITIAL_ACCELERATION}")
                    self._current_direction.x = -INITIAL_ACCELERATION
                elif self.__is_key_press(conf.button_right):
                    self.current_side = RIGHT
                    logger.debug(f"On applique une accélération initiale de {INITIAL_ACCELERATION}")
                    self._current_direction.x = INITIAL_ACCELERATION

            # Passage éventuel à FALLING
            if self._current_direction.y > 0:
                logger.debug(
                    "La force de mouvement verticale est supérieure à 0 -> on essaye de passer à l'état FALLING.")
                self.try_change_current_state(EntityStateName.FALLING)

            # Passage éventuel à TURNING
            if (self._current_direction.x > 0 and self.__is_key_press(conf.button_left)) or \
                    (self._current_direction.x < 0 and self.__is_key_press(conf.button_right)):
                logger.debug(f"On change de direction alors que la force de déplacement horizontale n'est pas nulle.")
                logger.debug(f"On essaye de passer à l'état TURNING.")
                self.try_change_current_state(EntityStateName.TURNING)
                logger.debug(f"La valeur de la friction est multipliée par 2.")
                friction_value *= 2
                apply_friction()
        else:
            logger.debug("Aucune direction n'est appuyée.")

            apply_friction()

            logger.debug("  -> on reset le timer de course.")
            self.run_timer.reset()

            if not self.is_in_air:
                logger.debug("  -> Mario n'est pas en l'air -> On essaye de passer à l'état STAND.")
                self.try_change_current_state(EntityStateName.STAND)

    def __handle_buttons(self, delta: float, friction_value: float):
        self.__handle_button_a()
        self.__handle_buttons_directions_and_b(delta, friction_value)

    def __handle_jump_buffer(self):
        if self.__can_count_jump_buffer_counter:
            self.__jump_buffer_counter += 1
            logger.debug(f"On peut augmenter le compteur du jump_buffer: {self.__jump_buffer_counter}")
            if self.__jump_buffer_counter > JUMP_BUFFER:
                logger.debug(f"Le compteur de jump_buffer est supérieur à {JUMP_BUFFER}")
                logger.debug(f"Si Mario passe à l'état STAND durant cette frame, son saut ne sera pas pris en compte")
                self.__on_jump_buffer = False
            else:
                logger.debug(f"Le compteur de jump_buffer est encore inférieur à {JUMP_BUFFER}")
                logger.debug(f"Si Mario passe à l'état STAND à la frame suivante, son saut sera encore pris en compte")
                self.__on_jump_buffer = True

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

    def __what_to_do_on_state_stand(self):
        logger.debug("Mario est à l'état STAND.")
        self.__coyote_frame_counter = 0
        logger.debug(f"On aussi peut réinitialiser le compteur de jump_buffer")
        self.__can_count_jump_buffer_counter = False
        self.__jump_buffer_counter = 0

    def __what_to_do_on_state_ascending(self, factor: float):
        logger.debug("Mario est à l'état ASCENDING.")
        self.__move(factor)
        if self._current_direction.y == 0:
            logger.debug(f"Comme la force en Y est à 0, on ajoute directement la valeur de JUMP_FORCE: {JUMP_FORCE}.")
            self._current_direction.y = JUMP_FORCE
        elif self._current_direction.y > 0:
            logger.debug(f"La force en Y est > 0, on peut passer à l'état DESCENDING.")
            self.try_change_current_state(EntityStateName.DESCENDING)
        elif self._current_direction.y < MIN_JUMP_SPEED and not self.__is_key_press(conf.button_a):
            self._current_direction.y = MIN_JUMP_SPEED

    def __what_to_do_on_state_descending(self, factor: float):
        logger.debug("Mario est à l'état DESCENDING.")

        self.__handle_jump_buffer()

        self.__move(factor)

        if self._current_direction.y == 0:
            logger.debug(f"Comme la force en Y est à 0, on réinitialise le compteur de frame sans gravité à 0.")
            self.__frame_no_gravity_counter = 0
            logger.debug(f"On passe à l'état STAND.")
            self.try_change_current_state(EntityStateName.STAND)

    def __what_to_do_on_state_walking(self, factor: float):
        logger.debug("Mario est à l'état WALKING.")
        self.__move(factor)

    def __what_to_do_on_state_running(self, factor: float):
        logger.debug("Mario est à l'état RUNNING.")
        self.__move(factor)

    def __what_to_do_on_state_falling(self, factor: float):
        logger.debug("Mario est à l'état FALLING.")
        self.__move(factor)
        self.__coyote_frame_counter += 1
        logger.debug(f"On augmente le compteur de frame coyote de 1 : {self.__coyote_frame_counter}")

        self.__handle_jump_buffer()

        if self._current_direction.y == 0:
            self.try_change_current_state(EntityStateName.STAND)

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

        logger.debug(f"Fin de 'set_current_state' de 'Player' pour [{self}].")

    def handle_events(self, event: Event):
        if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
            return

        if event.type == pygame.KEYDOWN:
            self.__keys_pressed.add(event.key)
            logger.debug(f"Le bouton {event.key} vient d'être appuyé.")

            if event.key == conf.button_a and (
                    self.is_current_state(EntityStateName.DESCENDING) or self.is_current_state(
                EntityStateName.FALLING)):
                logger.debug(f"Le bouton A vient d'être appouyé alors que Mario est à l'état DESCENDING ou FALLING")
                logger.debug(f"On peut commencer à compter les frames du jump_buffer")
                self.__can_count_jump_buffer_counter = True
        elif event.type == pygame.KEYUP:
            self.__keys_pressed.discard(event.key)
            logger.debug(f"Le bouton {event.key} vient d'être relâché.")

    def update_dt(self, delta: float):
        logger.debug("Début update Player.")
        logger.debug(f"La position de Mario est [{self.x}, {self.y}].")
        FACTOR = (delta / 1000) * FPS

        friction_value = FRICTION * FACTOR
        if self.is_in_air:
            logger.debug("Mario est en l'air, la valeur de friction est divisée par 2.")
            friction_value /= 2

        super().update_dt(delta)

        self.__handle_buttons(delta, friction_value)
        self.__what_to_do_on_each_state(FACTOR)

        if self.y >= SCREEN_HEIGHT + TILE_SIZE:
            post_event(MARIO_DEATH)

        logger.debug(f"L'état courant est {self.current_state.name.name}.")

        logger.debug("Fin update Player.")

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

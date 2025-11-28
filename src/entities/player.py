import pygame
from pygame import Color, Surface
from pygame.event import Event
from pygame.locals import *

from src.commons import SCREEN_HEIGHT, TILE_SIZE
from src.commons.my_events import post_event, MARIO_DEATH
from src.entities.entity import Entity
from src.game.gameloop_interface import GameLoopInterface


class Player(Entity, GameLoopInterface):
    def __init__(self, pos_x: int, pos_y: int):
        from src.resources_manager import im
        image = im.get("mario_stand_0")
        image.set_colorkey(Color(255, 0, 255))
        super().__init__(pos_x, pos_y, image)

        self.__score = 0
        self.__lives = 0
        self.__coins = 0

        self._current_level = None

        self.__move_speed = 0

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
    def move_speed(self) -> float:
        return self.__move_speed

    @move_speed.setter
    def move_speed(self, value: int):
        self.__move_speed = value

    def add_in_level(self, level: "Level"):
        self._current_level = level
        self._current_level.player_sprite.add(self)
        self._current_level.center_at = self

    def handle_events(self, event: Event):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_UP]:
            self.y -= self.move_speed
        elif keys_pressed[K_DOWN]:
            self.y += self.move_speed
        elif keys_pressed[K_LEFT]:
            self.x -= self.move_speed
        elif keys_pressed[K_RIGHT]:
            self.x += self.move_speed

    def update_dt(self, delta: float):
        self.move_speed = delta * 0.15

        if self.y >= SCREEN_HEIGHT + TILE_SIZE:
            post_event(MARIO_DEATH)

    def render(self):
        pass

    def get_surface(self) -> Surface:
        return self.image

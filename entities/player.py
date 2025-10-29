import pygame
from pygame import Color, Surface
from pygame.locals import *

from entities.entity import Entity
from game.gameloop_interface import GameLoopInterface


class Player(Entity, GameLoopInterface):
    def __init__(self, pos_x: int, pos_y: int):
        image = pygame.image.load("assets/images/mario/stand/0.gif").convert_alpha()
        image.set_colorkey(Color(255, 0, 255))
        super().__init__(pos_x, pos_y, image)

        self.__move_speed = 0

    @property
    def move_speed(self) -> float:
        return self.__move_speed

    @move_speed.setter
    def move_speed(self, value: int):
        self.__move_speed = value

    def handle_events(self):
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

    def render(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))

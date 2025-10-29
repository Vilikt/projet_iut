import pygame
from pygame import Surface, K_RETURN

from commons import singleton
from gamestates.gamestate import GameState


@singleton
class GameStateMain(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager)

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_RETURN]:
            print("pause")

    def update_dt(self, delta: float):
        pass

    def render(self, screen: Surface):
        pass

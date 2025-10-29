import pygame.key
from pygame import Surface, K_RETURN, Color

from commons import singleton
from gamestates import GameStateName
from gamestates.gamestate import GameState


@singleton
class GameStateTitle(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager)

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_RETURN]:
            self.manager.current_state = GameStateName.MAIN

    def update_dt(self, delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(Color(0, 255, 0))

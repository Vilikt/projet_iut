import pygame
from pygame import Surface, K_RETURN
from pygame.event import Event

from src.commons import singleton
from src.entities.player import Player
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import lm


@singleton
class GameStateMain(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.MAIN)

        self.__level = None
        self.__player = Player(5, 5)

    def change_level(self, level_name: str):
        self.__level = lm.get(level_name)
        self.__player.add_in_level(self.__level)
        self.game.hud.world_name = self.__level.name
        self.game.hud.time = self.__level.time
        self.__player.x, self.__player.y = self.__level.player_start_point

    def handle_events(self, event: Event):
        super().handle_events(event)

        self.__level.handle_events(event)
        self.__player.handle_events(event)

    def update_dt(self, delta: float):
        super().update_dt(delta)

        self.__level.update_dt(delta)

    def render(self):
        self.__level.render()
        self._game_state_surface = self.__level.get_surface()

        super().render()

    def get_surface(self) -> Surface:
        return self._game_state_surface

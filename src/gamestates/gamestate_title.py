import pygame.key
from pygame import K_RETURN, Surface, KEYUP, KMOD_SHIFT, K_RSHIFT
from pygame.event import Event

from src.commons import singleton
from src.configuration import conf
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import im, fm


class TextPos:
    COIN_NUMBER = (104, 24)
    WORLD_NUMBER = (153, 24)
    ONE_PLAYER = (88, 144)
    TWO_PLAYER = (88, 160)
    OPTIONS = (88, 176)
    TOP = (97, 192)


CURSOR_POS = [
    (72, 144),
    (72, 160),
    (72, 176)
]

@singleton
class GameStateTitle(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.TITLE)

        self.__bg_image = im.get("title_screen_background")
        self.__cursor = im.get("title_screen_cursor")
        self.__cursor_pos_index = 0

        # Prérendu des textes
        self.__one_player_surface = fm.render_text("1 PLAYER GAME")
        self.__two_player_surface = fm.render_text("2 PLAYER GAME")
        self.__options_surface = fm.render_text("OPTIONS")
        self.__top_surface = fm.render_text("TOP-0000000")

        self.__cursor_rect = self.__cursor.get_rect()
        self.__cursor_positions = [pygame.Rect(x, y, *self.__cursor_rect.size) for x, y in CURSOR_POS]

    def handle_events(self, event: Event):
        if event.type != KEYUP:
            return

        if event.key == conf.button_select:
            self.__cursor_pos_index = (self.__cursor_pos_index + 1) % len(CURSOR_POS)
        elif event.key == conf.button_start:
            states = {
                0: GameStateName.MAIN,
                1: GameStateName.MAIN,  # 2 joueurs (TODO: Implémenter GameStateName.TWO_PLAYERS)
                2: GameStateName.OPTIONS
            }
            self.manager.current_state = states.get(self.__cursor_pos_index, GameStateName.TITLE)

    def update_dt(self, delta: float):
        pass

    def render(self):
        self._game_state_surface.blit(self.__bg_image, (0, 0))
        self._game_state_surface.blit(self.__cursor, self.__cursor_positions[self.__cursor_pos_index])
        self._game_state_surface.blit(self.__one_player_surface, TextPos.ONE_PLAYER)
        self._game_state_surface.blit(self.__two_player_surface, TextPos.TWO_PLAYER)
        self._game_state_surface.blit(self.__options_surface, TextPos.OPTIONS)
        self._game_state_surface.blit(self.__top_surface, TextPos.TOP)


    def get_surface(self) -> Surface:
        return self._game_state_surface

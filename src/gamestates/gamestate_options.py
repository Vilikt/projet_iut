from pygame import Surface, KEYUP
from pygame.event import Event

from src.commons import Button
from src.configuration import conf
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import im

CURSOR_POS_X = 24

# Positions du curseur (identiques aux clés de TEXT_POSITIONS pour les options)
CURSOR_POS = {
    "full_screen": (CURSOR_POS_X, 40),
    "window_size": (CURSOR_POS_X, 56),
    Button.A.value: (CURSOR_POS_X, 80),
    Button.B.value: (CURSOR_POS_X, 88),
    Button.UP.value: (CURSOR_POS_X, 96),
    Button.DOWN.value: (CURSOR_POS_X, 104),
    Button.LEFT.value: (CURSOR_POS_X, 112),
    Button.RIGHT.value: (CURSOR_POS_X, 120),
    Button.SELECT.value: (CURSOR_POS_X, 128),
    Button.START.value: (CURSOR_POS_X, 136),
    "default_controls": (CURSOR_POS_X, 152)
}

# Ordre de navigation dans le menu
NAVIGATION_ORDER = list(CURSOR_POS.keys())


class GameStateOptions(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.OPTIONS)

        self.__bg_image = im.get("options_background")
        self.__cursor = im.get("options_cursor")
        self.__current_cursor_index = 0

    @property
    def current_cursor_pos(self) -> tuple[int, int]:
        return CURSOR_POS[NAVIGATION_ORDER[self.__current_cursor_index]]

    def handle_events(self, event: Event):
        if event.type != KEYUP:
            return

        if event.key in [conf.button_select, conf.button_down]:
            self.__current_cursor_index = (self.__current_cursor_index + 1) % len(NAVIGATION_ORDER)
        elif event.key == conf.button_up:
            self.__current_cursor_index = (self.__current_cursor_index - 1) % len(NAVIGATION_ORDER)

    def update_dt(self, delta: float):
        pass

    def render(self):
        self._game_state_surface.blit(self.__bg_image, (0, 0))
        self._game_state_surface.blit(self.__cursor, self.current_cursor_pos)

    def get_surface(self) -> Surface:
        return self._game_state_surface

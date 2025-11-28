from enum import Enum, auto


class GameStateName(Enum):
    TITLE = auto()
    MAIN = auto()
    OPTIONS = auto()
    INTER_LEVEL = auto()
    GAME_OVER = auto()

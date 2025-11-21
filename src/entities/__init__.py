from enum import Enum, auto

DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
DIRECTION_UP = "up"
DIRECTION_DOWN = "down"


class EntityState(Enum):
    STAND = auto()
    WALK = auto()
    RUN = auto()
    JUMP = auto()
    FALL = auto()
    LANDED = auto()
    TURN = auto()

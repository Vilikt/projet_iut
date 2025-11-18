from enum import Enum, auto


class EntityState(Enum):
    STAND = auto()
    WALK = auto()
    RUN = auto()
    JUMP = auto()
    FALL = auto()
    LANDED = auto()
    TURN = auto()

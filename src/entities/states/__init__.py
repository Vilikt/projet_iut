from enum import Enum, auto


class EntityStateName(Enum):
    STAND = auto()
    WALKING = auto()
    RUNNING = auto()
    ASCENDING = auto()
    DESCENDING = auto()
    FALLING = auto()
    TURNING = auto()

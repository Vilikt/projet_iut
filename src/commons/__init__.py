from enum import Enum
from pathlib import Path

from pygame import Color

ROOT = Path("./src/")

FPS = 60

FONT_SIZE = 8

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240

COLOR_BLACK = Color(0, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_TRANSPARENCY = Color(255, 0, 255)


class Button(Enum):
    A = "a"
    B = "b"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    START = "start"
    SELECT = "select"


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

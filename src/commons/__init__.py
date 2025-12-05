from enum import Enum
from pathlib import Path

from pygame import Color, Rect

ROOT = Path("./src/")

FPS = 60

FONT_SIZE = 8
TILE_SIZE = 16

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240

COLOR_BLACK = Color(0, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_TRANSPARENCY = Color(255, 0, 255)

# Directions
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"


# Boutons
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


def get_collision_info(rect1: Rect, rect2: Rect) -> tuple[str, Rect] | tuple[None, None]:
    # Calcul du rectangle de chevauchement
    left = max(rect1.left, rect2.left)
    right = min(rect1.right, rect2.right)
    top = max(rect1.top, rect2.top)
    bottom = min(rect1.bottom, rect2.bottom)

    # Vérifier s'il y a un chevauchement
    if left >= right or top >= bottom:
        return None, None  # Pas de collision

    overlap_rect = Rect(left, top, right - left, bottom - top)

    # Calcul des chevauchements horizontal et vertical
    dx = right - left
    dy = bottom - top

    # Déterminer le côté de la collision
    if dx < dy:
        side = RIGHT if rect1.centerx < rect2.centerx else LEFT
    else:
        side = DOWN if rect1.centery < rect2.centery else UP

    return side, overlap_rect

from pathlib import Path

import pygame
from pygame import Surface

from commons import singleton, COLOR_TRANSPARENCY
from resources_manager import FOLDER_IMAGES
from resources_manager.resources_manager import ResourcesManager


@singleton
class ImagesManager(ResourcesManager):
    def __init__(self):
        super().__init__(FOLDER_IMAGES)

    def _get_resource_from_file(self, file: Path) -> Surface:
        surface = pygame.image.load(file).convert_alpha()
        surface.set_colorkey(COLOR_TRANSPARENCY)
        return surface

    def get(self, resource_name: str) -> Surface:
        return super().get(resource_name)

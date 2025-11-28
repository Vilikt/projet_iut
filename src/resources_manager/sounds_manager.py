from pathlib import Path

from pygame.mixer import Sound

from src.commons import singleton
from src.resources_manager.locals import FOLDER_SOUNDS
from src.resources_manager.resources_manager import ResourcesManager


@singleton
class SoundsManager(ResourcesManager):
    def __init__(self):
        super().__init__(FOLDER_SOUNDS, "wav")

    def _get_resource_from_file(self, file: Path) -> Sound:
        return Sound(file)

    def get(self, resource_name: str) -> Sound:
        return super().get(resource_name)

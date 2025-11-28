from pathlib import Path

from src.commons import singleton
from src.levels.level import Level
from src.resources_manager.locals import FOLDER_LEVELS
from src.resources_manager.resources_manager import ResourcesManager


@singleton
class LevelsManager(ResourcesManager):
    def __init__(self):
        super().__init__(FOLDER_LEVELS, "tmx")

    def _get_resource_from_file(self, file: Path) -> Level:
        return Level(file)

    def get(self, resource_name) -> Level:
        return super().get(resource_name)

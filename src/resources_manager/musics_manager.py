from pathlib import Path

import pygame.mixer

from src.commons import singleton
from src.resources_manager.locals import FOLDER_MUSICS
from src.resources_manager.resources_manager import ResourcesManager
from src.mylogging import logger


@singleton
class MusicsManager(ResourcesManager):
    def __init__(self):
        super().__init__(FOLDER_MUSICS, "wav")

    def _get_resource_from_file(self, file: Path) -> any:
        pass

    def load_music(self, name: str):
        try:
            pygame.mixer.music.load(self._folder / (name + "." + self._extension))
        except Exception as e:
            logger.error(e)

    @staticmethod
    def play():
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()

    @staticmethod
    def toggle():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

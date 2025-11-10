from copy import deepcopy
from pathlib import Path

from src.commons.animation import Animation
from src.resources_manager.images_manager import ImagesManager
from src.resources_manager.locals import FOLDER_ANIMATIONS
from src.resources_manager.resources_manager import ResourcesManager


class AnimationsManager(ResourcesManager):
    def __init__(self, im: ImagesManager):
        self.__im = im
        super().__init__(FOLDER_ANIMATIONS)

    def _load(self):
        prefix = "animations_"
        frames_names = [name.replace(prefix, "") for name in self.__im._resources.keys() if name.startswith(prefix)]
        animations = dict()
        for frame_name in frames_names:
            animation_name = "_".join(frame_name.split("_")[:-1])
            if animation_name not in animations.keys():
                animations[animation_name] = []
            animations[animation_name].append(self.__im.get(f"{prefix}{frame_name}"))

        for name, frames in animations.items():
            self._resources[name] = Animation(name, frames, 150)

    def _get_resource_from_file(self, file: Path) -> any:
        pass

    def get(self, name: str) -> Animation:
        return deepcopy(super().get(name))

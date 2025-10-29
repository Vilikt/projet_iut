import os.path
from abc import ABC
from os import walk
from pathlib import Path

from resources_manager.resources_manager_interface import ResourcesManagerInterface


class ResourcesManager(ResourcesManagerInterface, ABC):
    def __init__(self, folder: Path):
        self._folder = folder

        self._resources = {}

        self.__load()

    def __load(self):
        for root, _, files in walk(self._folder):
            for file in files:
                # la liste des répertoires depuis .[type_ressource]/
                sub_dirs = root.split("\\")[2:]
                key = "_".join(sub_dirs)
                if sub_dirs:
                    key += "_"
                # nom du fichier sans l'extension
                key += file.split('.')[0]

                self._resources[key] = self._get_resource_from_file(Path(os.path.join(root, file)))

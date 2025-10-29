import sys
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
                # Chemin relatif depuis self._folder
                rel_path = Path(root).relative_to(self._folder)

                # Sous-dossiers (compatibles Windows/Linux/Mac)
                sub_dirs = rel_path.parts

                # Clé : "dossier_sousdossier_nom_fichier"
                key_parts = list(sub_dirs) + [Path(file).stem]
                key = "_".join(key_parts)

                # Charge et stocke la ressource
                self._resources[key] = self._get_resource_from_file(Path(root) / file)

    def get(self, resource_name: str) -> any:
        try:
            res = self._resources[resource_name]
        except KeyError:
            print(f"La ressource \"{resource_name}\" dans \"{self._folder}\" n'existe pas.")
            sys.exit()

        return res

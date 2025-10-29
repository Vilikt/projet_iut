from abc import ABC, abstractmethod
from pathlib import Path


class ResourcesManagerInterface(ABC):
    @abstractmethod
    def _get_resource_from_file(self, file: Path) -> any:
        pass

    @abstractmethod
    def get(self, resource_name: str) -> any:
        pass

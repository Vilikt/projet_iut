from pygame import Surface
from pygame.freetype import Font

from src.commons import singleton, COLOR_WHITE, FONT_SIZE
from src.resources_manager.locals import FOLDER_FONTS
from src.resources_manager.resources_manager import ResourcesManager


DEFAULT_NAME = "smb"
DEFAULT_COLOR = COLOR_WHITE
DEFAULT_SIZE = FONT_SIZE


@singleton
class FontsManager(ResourcesManager):
    def __init__(self):
        super().__init__(FOLDER_FONTS)

        self.__fixed_fonts = {}

    def _get_resource_from_file(self, file: str) -> Font:
        return Font(file)

    def get(self, font_name) -> Font:
        return super().get(font_name)

    def render_text(self, text: str, font_name=DEFAULT_NAME, color=DEFAULT_COLOR, size=DEFAULT_SIZE) -> Surface:
        return self.get(font_name).render(text, fgcolor=color, size=size)[0]

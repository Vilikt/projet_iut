from src.resources_manager.animations_manager import AnimationsManager
from src.resources_manager.images_manager import ImagesManager
from src.resources_manager.fonts_manager import FontsManager
from src.resources_manager.levels_manager import LevelsManager
from src.resources_manager.musics_manager import MusicsManager
from src.resources_manager.sounds_manager import SoundsManager

im = ImagesManager()
am = AnimationsManager(im)
fm = FontsManager()
lm = LevelsManager()
sm = SoundsManager()
mm = MusicsManager()

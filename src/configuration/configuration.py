from configparser import ConfigParser
from pathlib import Path

from pygame.locals import *

from src.commons import Button, singleton

OPTIONS = "options"
CONTROLS = "controls"

OPTION_FULL_SCREEN = "full_screen"
OPTION_WINDOW_SIZE = "window_size"

OPTIONS_DEFAULT = {
    OPTION_FULL_SCREEN: 0,
    OPTION_WINDOW_SIZE: 1
}

CONTROLS_DEFAULT = {
    Button.A: K_c,
    Button.B: K_x,
    Button.UP: K_UP,
    Button.DOWN: K_DOWN,
    Button.LEFT: K_LEFT,
    Button.RIGHT: K_RIGHT,
    Button.START: K_RETURN,
    Button.SELECT: K_RSHIFT
}


@singleton
class Configuration:
    def __init__(self):
        self.__parser = ConfigParser()
        self.__file_path = Path("./config.ini")
        self.__read_config_file()

    @property
    def full_screen(self) -> bool:
        return self.__parser.getboolean(OPTIONS, OPTION_FULL_SCREEN, fallback=False)

    @full_screen.setter
    def full_screen(self, value: bool):
        self.__parser.set(OPTIONS, OPTION_FULL_SCREEN, str(value))
        self.__write_config_file()

    @property
    def window_size(self) -> int:
        return self.__parser.getint(OPTIONS, OPTION_WINDOW_SIZE, fallback=OPTIONS_DEFAULT[OPTION_WINDOW_SIZE])

    @window_size.setter
    def window_size(self, value: int):
        self.__parser.set(OPTIONS, OPTION_WINDOW_SIZE, str(value))
        self.__write_config_file()

    def __getattr__(self, name: str):
        if name.startswith("button_"):
            button_name = name[7:]
            try:
                button = Button[button_name.upper()]
                return self.__parser.getint(CONTROLS, str(button), fallback=CONTROLS_DEFAULT[button])
            except (KeyError, ValueError):
                raise AttributeError(f"No such button: {name}")
        raise AttributeError(f"'Configuration' has no attribute '{name}'")

    def __setattr__(self, name: str, value: int):
        if name.startswith("button_"):
            button_name = name[7:]
            try:
                button = Button[button_name.upper()]
                self.__parser.set(CONTROLS, str(button), str(value))
                self.__write_config_file()
            except (KeyError, ValueError):
                raise AttributeError(f"No such button: {name}")
        else:
            super().__setattr__(name, value)

    def restore_default_controls(self):
        self.__parser[CONTROLS] = {
            str(button): str(code)  # Convertir clé et valeur en chaînes
            for button, code in CONTROLS_DEFAULT.items()
        }

        self.__write_config_file()

    def __read_config_file(self):
        if not self.__file_path.exists():
            self.__parser[OPTIONS] = OPTIONS_DEFAULT
            self.__parser[CONTROLS] = {
                str(button): str(code)  # Convertir clé et valeur en chaînes
                for button, code in CONTROLS_DEFAULT.items()
            }

            self.__write_config_file()

        self.__parser.read(self.__file_path)

    def __write_config_file(self):
        with open(self.__file_path, 'w') as config_file:
            self.__parser.write(config_file)

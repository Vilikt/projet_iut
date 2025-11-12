import pygame
from pygame import Surface, Rect, KEYUP, K_ESCAPE, K_F10, K_KP_MINUS, K_KP_PLUS, Color
from pygame.event import Event

from src.commons import Button, FONT_SIZE
from src.commons.timer import Timer
from src.configuration import conf
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import im, fm

BUTTON_NAME_X_POS = 48
BUTTON_VALUE_X_POS = FONT_SIZE * 14
CURSOR_POS_X = 24
ERROR_MESSAGE_POS = (56, 176)

# Positions des textes
STATIC_TEXT_AND_POSITIONS = {
    "full_screen": ("Full screen:", (40, 40)),
    "window_size": ("Window size:", (40, 56)),
    "controls": ("Controls:", (40, 72)),
    Button.A.value: ("A:", (BUTTON_NAME_X_POS, 80)),
    Button.B.value: ("B:", (BUTTON_NAME_X_POS, 88)),
    Button.UP.value: ("Up:", (BUTTON_NAME_X_POS, 96)),
    Button.DOWN.value: ("Down:", (BUTTON_NAME_X_POS, 104)),
    Button.LEFT.value: ("Left:", (BUTTON_NAME_X_POS, 112)),
    Button.RIGHT.value: ("Right:", (BUTTON_NAME_X_POS, 120)),
    Button.SELECT.value: ("Select:", (BUTTON_NAME_X_POS, 128)),
    Button.START.value: ("Start", (BUTTON_NAME_X_POS, 136)),
    "default_controls": ("Restore default", (BUTTON_NAME_X_POS, 152))
}

WAIT_FOR_KEY = fm.render_text("Wait for key...", "smb", Color(0, 255, 0))

# Positions du curseur (identiques aux clés de TEXT_POSITIONS pour les options)
CURSOR_POS = {
    "full_screen": (CURSOR_POS_X, 40),
    "window_size": (CURSOR_POS_X, 56),
    Button.A.value: (CURSOR_POS_X, 80),
    Button.B.value: (CURSOR_POS_X, 88),
    Button.UP.value: (CURSOR_POS_X, 96),
    Button.DOWN.value: (CURSOR_POS_X, 104),
    Button.LEFT.value: (CURSOR_POS_X, 112),
    Button.RIGHT.value: (CURSOR_POS_X, 120),
    Button.SELECT.value: (CURSOR_POS_X, 128),
    Button.START.value: (CURSOR_POS_X, 136),
    "default_controls": (CURSOR_POS_X, 152)
}

# Ordre de navigation dans le menu
NAVIGATION_ORDER = list(CURSOR_POS.keys())


class GameStateOptions(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.OPTIONS)

        self.__bg_image = im.get("options_background")
        self.__cursor = im.get("options_cursor")
        self.__current_cursor_index = 0
        self.__waiting_for_key = False
        self.__button_to_reassign = None

        self.__error_message = None
        self.__error_timer = Timer(2000, False, False)

        # Optimisations
        self.__button_names = [btn.name.lower() for btn in Button]
        self.__static_texts: dict[str, tuple[Surface, Rect]] = {}
        self.__dynamic_texts: dict[str, tuple[Surface, Rect]] = {}

        # Calcul des Rect pour les textes fixes.
        for name, datas in STATIC_TEXT_AND_POSITIONS.items():
            text, position = datas
            surface = fm.render_text(text)
            self.__static_texts[name] = (surface, surface.get_rect(topleft=position))

        self.calc_dynamic_texts()

    @property
    def current_cursor_pos(self) -> tuple[int, int]:
        return CURSOR_POS[NAVIGATION_ORDER[self.__current_cursor_index]]

    @property
    def current_cursor_pos_name(self) -> str:
        return NAVIGATION_ORDER[self.__current_cursor_index]

    def handle_events(self, event: Event):
        if event.type != KEYUP:
            return

        if self.__waiting_for_key:
            self.__handle_key_assignment(event.key)
            self.calc_dynamic_texts()
        elif event.key in [conf.button_select, conf.button_down]:
            self.__current_cursor_index = (self.__current_cursor_index + 1) % len(NAVIGATION_ORDER)
        elif event.key == conf.button_up:
            self.__current_cursor_index = (self.__current_cursor_index - 1) % len(NAVIGATION_ORDER)
        elif event.key in [conf.button_a, conf.button_start]:
            self.__handle_selection()
            self.calc_dynamic_texts()
        elif event.key in [conf.button_left, conf.button_right]:
            self.__handle_window_size(event.key)
            self.calc_dynamic_texts()
        elif event.key == conf.button_b:
            self.manager.current_state = GameStateName.TITLE

    def calc_dynamic_texts(self):
        dynamics_texts = {
            "full_screen": [fm.render_text("yes" if conf.full_screen else "no"), (FONT_SIZE * 18, 40)],
            "window_size": [fm.render_text(str(conf.window_size)), (FONT_SIZE * 18, 56)],
            Button.A.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_a"))),
                             (BUTTON_VALUE_X_POS, 80)],
            Button.B.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_b"))),
                             (BUTTON_VALUE_X_POS, 88)],
            Button.UP.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_up"))),
                              (BUTTON_VALUE_X_POS, 96)],
            Button.DOWN.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_down"))),
                                (BUTTON_VALUE_X_POS, 104)],
            Button.LEFT.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_left"))),
                                (BUTTON_VALUE_X_POS, 112)],
            Button.RIGHT.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_right"))),
                                 (BUTTON_VALUE_X_POS, 120)],
            Button.SELECT.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_select"))),
                                  (BUTTON_VALUE_X_POS, 128)],
            Button.START.value: [fm.render_text(pygame.key.name(getattr(conf, f"button_start"))),
                                 (BUTTON_VALUE_X_POS, 136)],
        }

        # Calcul des Rect pour les textes dynamiques.
        for name, datas in dynamics_texts.items():
            surface, position = datas
            self.__dynamic_texts[name] = (
                surface,
                surface.get_rect(topleft=position)
            )

    def __handle_key_assignment(self, key):
        """Gère l'assignation des touches avec vérification des conflits"""
        # Interdiction d'assigner des touches système
        if key in [K_ESCAPE, K_F10, K_KP_MINUS, K_KP_PLUS]:
            self.__handle_error_message(f"Can't be reassigned !")
            return

        # Vérifie les conflits
        for btn in self.__button_names:
            if getattr(conf, f"button_{btn}") == key and btn != self.current_cursor_pos_name:
                self.__handle_error_message(f"Already assigned !")
                return

        setattr(conf, f"button_{self.__button_to_reassign}", key)
        self.__waiting_for_key = False
        self.__error_message = None
        self.__error_timer.reset()

    def __handle_error_message(self, message: str):
        self.__error_message = fm.render_text(message, color=Color(255, 0, 0))
        self.__error_timer.start()

    def __handle_selection(self):
        """Gère la sélection des options"""
        name = self.current_cursor_pos_name
        if name == "full_screen":
            conf.full_screen = not conf.full_screen
            self.game.resize()
        elif name in self.__button_names:
            self.__assign_control()
        elif name == "default_controls":
            conf.restore_default_controls()

    def __assign_control(self):
        self.__waiting_for_key = True
        self.__button_to_reassign = self.current_cursor_pos_name

    def __handle_window_size(self, key: int):
        """Gère l'ajustement de la taille de fenêtre"""
        if self.current_cursor_pos_name == "window_size" and not conf.full_screen:
            if key == conf.button_left and conf.window_size > 1:
                conf.window_size -= 1
            elif key == conf.button_right:
                conf.window_size += 1
            self.game.resize()

    def update_dt(self, delta: float):
        if not self.__error_timer.finished:
            self.__error_timer.update(delta)
        else:
            self.__error_timer.reset()

    def render(self):
        self._game_state_surface.blit(self.__bg_image, (0, 0))

        self._game_state_surface.blit(self.__cursor, self.current_cursor_pos)

        # Textes statiques
        for surface, rect in self.__static_texts.values():
            self._game_state_surface.blit(surface, rect)

        # Textes dynamiques
        for name, datas in self.__dynamic_texts.items():
            if self.__waiting_for_key and self.current_cursor_pos_name == name:
                datas = (WAIT_FOR_KEY, datas[1])
            self._game_state_surface.blit(*datas)

        # Message d'erreur
        if self.__error_timer.running and (pygame.time.get_ticks() // 250) % 2 == 0:
            self._game_state_surface.blit(self.__error_message, ERROR_MESSAGE_POS)

    def get_surface(self) -> Surface:
        return super().get_surface()

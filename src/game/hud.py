from pygame import Surface
from pygame.event import Event

from src.commons import singleton
from src.commons.timer import Timer
from src.game.gameloop_interface import GameLoopInterface
from src.resources_manager import im, fm, am

COIN_ANIM_POS = (88, 24)


class TextPos:
    PLAYER_NAME = (24, 16)
    COIN_NUMBER = (104, 24)
    WORLD_NUMBER = (153, 24)
    SCORE = (16, 24)
    TIME = (208, 24)


@singleton
class Hud(GameLoopInterface):
    def __init__(self):
        self.__world_name = "1-1"
        self.__player_name = "MARIO"
        self.__score = 0
        self.__coins = 0
        self.__time = 400
        self.__remaining_time = self.__time

        self.__background = im.get("hud_background")
        self.__coins_animation = am.get("hud_coins")

        # Prérendu des textes
        self.__player_name_surface = fm.render_text("MARIO")
        self.__score_surface = fm.render_text(str(self.__score).zfill(7))
        self.__coin_number_surface = fm.render_text(str(self.__coins).zfill(2))
        self.__world_surface = fm.render_text(self.__world_name)
        self.__time_surface = fm.render_text(str(self.__time).zfill(3))

        # Rects pour optimiser le blit
        self.__coins_rect = self.__coins_animation.current_image.get_rect(topleft=COIN_ANIM_POS)

        self.__timer = Timer(self.__time * 1000, loop=False, auto_start=False)
        self.__show_timer = True

        self.__surface = None

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value
        self.__score_surface = fm.render_text(str(self.__score).zfill(7))

    @property
    def coins(self) -> int:
        return self.__coins

    @coins.setter
    def coins(self, value: int):
        self.__coins = value
        self.__coin_number_surface = fm.render_text(str(self.__coins).zfill(2))

    @property
    def world_name(self) -> str:
        return self.__world_name

    @world_name.setter
    def world_name(self, value: str):
        self.__world_name = value
        self.__world_surface = fm.render_text(self.__world_name)

    @property
    def time(self) -> int:
        return self.__time

    @time.setter
    def time(self, value: int):
        self.__time = value
        self.remaining_time = self.__time
        self.__timer.time_to_wait = self.__time * 1000
        self.__timer.reset()

    @property
    def remaining_time(self) -> int:
        return self.__remaining_time

    @remaining_time.setter
    def remaining_time(self, value: int):
        self.__remaining_time = value
        self.__time_surface = fm.render_text(str(self.__remaining_time).zfill(3))

    @property
    def show_timer(self) -> bool:
        return self.__show_timer

    @show_timer.setter
    def show_timer(self, value: bool):
        self.__show_timer = value

    def stop_timer(self):
        if self.__timer.running:
            self.__timer.stop()

    def start_timer(self):
        if not self.__timer.running:
            self.__timer.start()

    def reset_timer(self):
        self.__timer.reset()

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        self.__coins_animation.update(delta)
        self.__timer.update(delta)
        self.remaining_time = int(self.__timer.remaining / 1000)

    def render(self):
        self.__surface = self.__background.copy()
        self.__surface.blit(self.__player_name_surface, TextPos.PLAYER_NAME)
        self.__surface.blit(self.__score_surface, TextPos.SCORE)
        self.__surface.blit(self.__coins_animation.current_image, self.__coins_rect)
        self.__surface.blit(self.__coin_number_surface, TextPos.COIN_NUMBER)
        self.__surface.blit(self.__world_surface, TextPos.WORLD_NUMBER)
        if self.__show_timer:
            self.__surface.blit(self.__time_surface, TextPos.TIME)

    def get_surface(self) -> Surface:
        return self.__surface

from pygame import Surface
from pygame.event import Event

from src.commons import singleton, COLOR_BLACK
from src.commons.timer import Timer
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import im, fm


@singleton
class GameStateInterLevel(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.INTER_LEVEL)

        self.__player_lives = 0

        self.__mario_surf = im.get("animations_mario_stand_0")
        world_name = self.game.hud.world_name
        self.__world_text = fm.render_text(f"WORLD {world_name}")
        self.__x_text = fm.render_text("x", size=8)
        self.__player_lives_text = fm.render_text(str(self.__player_lives))

        self.__show_timer = Timer(2500, loop=False)

    @property
    def player_lives(self) -> int:
        return self.__player_lives

    @player_lives.setter
    def player_lives(self, value: int):
        self.__player_lives = value
        self.__player_lives_text = fm.render_text(str(self.__player_lives))

    def on_enter(self):
        player = self.manager.get_state(GameStateName.MAIN).player
        self.player_lives = player.lives
        self.__show_timer.restart()

    def on_quit(self):
        pass

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        super().update_dt(delta)
        self.__show_timer.update(delta)

        if self.__show_timer.finished:
            self.manager.current_state = GameStateName.MAIN

    def render(self):
        self._game_state_surface.fill(COLOR_BLACK)
        super().render()
        self._game_state_surface.blit(self.__x_text, (120, 112))
        self._game_state_surface.blit(self.__player_lives_text, (144, 112))
        self._game_state_surface.blit(self.__mario_surf, (96, 105))
        self._game_state_surface.blit(self.__world_text, (88, 80))

    def get_surface(self) -> Surface:
        return super().get_surface()

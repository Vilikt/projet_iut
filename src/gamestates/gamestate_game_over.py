from pygame.event import Event

from src.commons import singleton, COLOR_BLACK
from src.commons.timer import Timer
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import fm, sm


@singleton
class GameStateGameOver(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.GAME_OVER)

        self.__game_over_text_surface = fm.render_text("GAME OVER")
        self.__player_name_surface = fm.render_text("MARIO")

        self.__show_timer = Timer(5000, False, False)

    def on_enter(self):
        sm.get("gameover").play()
        self.__show_timer.start()

    def on_quit(self):
        self.__show_timer.reset()

    def handle_events(self, event: Event):
        pass

    def update_dt(self, delta: float):
        super().update_dt(delta)
        self.__show_timer.update(delta)
        if self.__show_timer.finished:
            self.manager.current_state = GameStateName.TITLE

    def render(self):
        self._game_state_surface.fill(COLOR_BLACK)
        self._game_state_surface.blit(self.__player_name_surface, (104, 112))
        self._game_state_surface.blit(self.__game_over_text_surface, (88, 128))
        super().render()

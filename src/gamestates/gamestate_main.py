from pygame import Surface, KEYUP
from pygame.event import Event

from src.commons import singleton
from src.commons.my_events import MARIO_DEATH
from src.commons.timer import Timer
from src.configuration import conf
from src.entities.player import Player
from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.resources_manager import lm, sm, mm


@singleton
class GameStateMain(GameState):
    def __init__(self, manager: "GameStateManager"):
        super().__init__(manager, GameStateName.MAIN)

        self.__level = None
        self.__player = Player(5, 5)

        self.__paused = False

        self.__change_state_timer = Timer(4000, loop=False, auto_start=False)

    @property
    def player(self):
        return self.__player

    @property
    def paused(self) -> bool:
        return self.__paused

    @paused.setter
    def paused(self, value: bool):
        sm.get("pause").play()
        self.__paused = value
        mm.toggle()

    def change_level(self, level_name: str):
        self.__level = lm.get(level_name)
        self.__player.add_in_level(self.__level)
        self.game.hud.world_name = self.__level.name
        self.game.hud.time = self.__level.time

        if self.__level.type == "overworld":
            mm.load_music("overworld")

    def on_enter(self):
        self.game.hud.show_timer = True
        self.game.hud.start_timer()
        self.__player.x, self.__player.y = self.__level.player_start_point
        # mm.play()

    def on_quit(self):
        self.game.hud.show_timer = False
        self.game.hud.reset_timer()
        self.__change_state_timer.stop()
        mm.stop()

    def handle_events(self, event: Event):
        super().handle_events(event)

        self.__level.handle_events(event)
        self.__player.handle_events(event)

        if event.type == MARIO_DEATH:
            self.__change_state_timer.start()
            sm.get("death").play()
            mm.stop()
            self.__player.lives -= 1
        elif event.type == KEYUP and event.key == conf.button_start:
            self.paused = not self.paused

    def update_dt(self, delta: float):
        if self.__paused:
            return

        super().update_dt(delta)

        self.__change_state_timer.update(delta)
        if self.__change_state_timer.finished:
            if self.__player.lives > 0:
                self.game.state_manager.current_state = GameStateName.INTER_LEVEL
            else:
                self.game.state_manager.current_state = GameStateName.GAME_OVER
        elif not self.__change_state_timer.running:
            self.__level.update_dt(delta)

    def render(self):
        self.__level.render()
        self._game_state_surface = self.__level.get_surface()

        super().render()

    def get_surface(self) -> Surface:
        return self._game_state_surface

from src.gamestates import GameStateName
from src.gamestates.gamestate import GameState
from src.gamestates.gamestate_main import GameStateMain
from src.gamestates.gamestate_options import GameStateOptions
from src.gamestates.gamestate_title import GameStateTitle


class GameStateManager:
    def __init__(self):
        self._title = GameStateTitle(self)
        self._main = GameStateMain(self)
        self._options = GameStateOptions(self)
        self.__current_state = None

    @property
    def current_state(self) -> "GameState":
        return self.__current_state

    @current_state.setter
    def current_state(self, state_name: GameStateName):
        if not isinstance(state_name, GameStateName):
            raise ValueError("Le paramètre doit être une instane de GameStateName")

        self.__current_state = getattr(self, f"_{str(state_name.name).lower()}", None)

    def get_state(self, state_name: GameStateName) -> GameState:
        if not isinstance(state_name, GameStateName):
            raise ValueError("Le paramètre doit être une instane de GameStateName")

        return getattr(self, f"_{str(state_name.name).lower()}", None)

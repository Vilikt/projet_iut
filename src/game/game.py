import pygame
from pygame import Surface
from pygame.locals import *
from pygame.time import Clock

from src.commons import COLOR_BLACK, FPS, singleton
from src.configuration import conf
from src.game.display import Display
from src.game.gameloop_interface import GameLoopInterface
from src.gamestates import GameStateName


@singleton
class Game(GameLoopInterface):
    def __init__(self):
        self.__running = False
        self.__display = Display(self)
        self.__clock = Clock()
        from src.game.hud import Hud
        self.__hud = Hud()

        from src.gamestates.gamestate_manager import GameStateManager
        self.state_manager = GameStateManager(self)
        self.state_manager.current_state = GameStateName.TITLE

        pygame.display.set_caption("Hello World")

    @property
    def running(self) -> bool:
        return self.__running

    @property
    def hud(self) -> "Hud":
        return self.__hud

    def run(self):
        self.__running = True

    def handle_events(self, _):
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT or keys_pressed[K_ESCAPE]:
                self.__running = False
            elif event.type == KEYUP:
                if event.key in [K_KP_MINUS, K_KP_PLUS, K_F10]:
                    if event.key == K_KP_PLUS:
                        conf.window_size += 1
                    elif event.key == K_KP_MINUS and conf.window_size > 1:
                        conf.window_size -= 1
                    elif event.key == K_F10:
                        conf.full_screen = not conf.full_screen

                    self.state_manager.get_game_state_options.calc_dynamic_texts()
                    self.resize()

            self.state_manager.current_state.handle_events(event)

    def update_dt(self, delta):
        self.state_manager.current_state.update_dt(delta)

    def render(self):
        self.__display.screen.fill(COLOR_BLACK)
        self.state_manager.current_state.render()
        pos_x, pos_y = self.__display.get_gamestate_surface_pos()
        self.__display.screen.blit(self.__display.resize_gamestate_surface(), (pos_x, pos_y))
        pygame.display.flip()

    def loop(self):
        self.handle_events(None)
        self.update_dt(self.__clock.tick(FPS))
        self.render()

    def get_surface(self) -> Surface:
        return self.__display.screen

    def resize(self):
        self.__display.resize_screen()

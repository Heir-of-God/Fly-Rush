"""Module which contain Control class which controls everything in game (states)"""

import pygame as pg
from constants import FPS, GAME_SCREEN_HEIGHT, GAME_SCREEN_WIDTH
from states.base_state import State
from states.main_game_state import MainGameState
from states.menu_state import MenuState
from states.pause_state import PauseState
from states.game_over_state import GameOverState


class Control:
    def __init__(self) -> None:
        pg.init()

        # Setting up game's screen
        self.screen: pg.Surface = pg.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        icon: pg.Surface = pg.transform.scale(
            pg.image.load("assets/graphics/icons/main_icon.png").convert_alpha(), (64, 64)
        )
        pg.display.set_icon(icon)
        pg.display.set_caption("Fly RUSH!")

        self.state_dict: dict[str, State] = {
            "gameplay": MainGameState(),
            "menu": MenuState(),
            "pause": PauseState(),
            "game_over": GameOverState(),
        }
        self.state_name: str = "menu"
        self.state: State = self.state_dict[self.state_name]
        # load graphics
        for state in self.state_dict.values():
            state.load_graphics()
        self.state_dict["menu"].setup_rects_and_buttons()
        self.state_dict["pause"].setup_rects_and_buttons()
        self.state_dict["game_over"].setup_rects_and_buttons()
        self.state_dict["gameplay"].setup_rects_and_objects()
        self.state.startup()

        self.done = False
        self.clock = pg.time.Clock()

    def flip_state(self) -> None:
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup()

    def update(self) -> None:
        keys: pg.key.ScancodeWrapper = pg.key.get_pressed()
        self.state.get_keys(keys)
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update()

    def event_loop(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.state_dict["gameplay"].update_record()
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self) -> None:
        while not self.done:
            self.event_loop()
            self.update()
            self.state.draw(self.screen)

            self.clock.tick(FPS)
            pg.display.update()

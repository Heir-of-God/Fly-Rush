"""Module which contains state for the pause"""

import sys
import os

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

import pygame as pg
from .base_state import State
from .menu_button import Button


class PauseState(State):
    def __init__(self) -> None:
        super().__init__()

    def update_active_button(self, new_ind: int) -> None:
        self.buttons_list[self.current_active_button_ind].change_active()
        self.current_active_button_ind: int = new_ind
        self.buttons_list[self.current_active_button_ind].change_active()

    def load_graphics(self) -> None:
        self.pause_title: pg.Surface = pg.image.load("assets/graphics/pause/pause_title.png").convert_alpha()
        self.pause_title = pg.transform.rotozoom(self.pause_title, 0, 0.7)

        self.pause_title_bg: pg.Surface = pg.image.load("assets/graphics/pause/title_bg.png").convert_alpha()
        self.pause_title_bg = pg.transform.rotozoom(self.pause_title_bg, 0, 0.8)

    def setup_rects_and_buttons(self) -> None:
        self.pause_title_bg_rect: pg.Rect = self.pause_title_bg.get_rect(center=(721, 150))
        self.pause_tittle_rect: pg.Rect = self.pause_title.get_rect(
            center=(self.pause_title_bg_rect.centerx, self.pause_title_bg_rect.centery - 15)
        )

        self.game_title_rect: pg.Rect = self.pause_title.get_rect(
            center=(self.pause_title_bg_rect.centerx + 10, self.pause_title_bg_rect.centery)
        )

        self.resume_button = Button(
            721,
            395,
            "assets/graphics/pause/resume_button.png",
            "assets/graphics/pause/resume_button_active.png",
        )
        self.to_home_button = Button(
            721,
            530,
            "assets/graphics/pause/to_home_button.png",
            "assets/graphics/pause/to_home_button_active.png",
        )

        self.buttons_list: list[Button] = [self.resume_button, self.to_home_button]
        self.current_active_button_ind = 0
        self.buttons_list[self.current_active_button_ind].change_active()

    def cleanup(self) -> None:
        super().cleanup()
        self.update_active_button(0)

    def get_event(self, event) -> None:
        if event.type == pg.KEYDOWN:
            pressed_key = event.key
            if pressed_key == pg.K_SPACE:
                self.done = True
                if self.current_active_button_ind == 0:
                    self.next = "gameplay"
                elif self.current_active_button_ind == 1:
                    self.next = "menu"

            # change active button in the pause
            elif self.current_active_button_ind == 1 and pressed_key == pg.K_w:
                self.update_active_button(0)
            elif self.current_active_button_ind == 0 and pressed_key == pg.K_s:
                self.update_active_button(1)

    def draw(self, screen) -> None:
        screen.blit(self.pause_title_bg, self.pause_title_bg_rect)
        screen.blit(self.pause_title, self.pause_tittle_rect)
        for button in self.buttons_list:
            button.draw(screen)

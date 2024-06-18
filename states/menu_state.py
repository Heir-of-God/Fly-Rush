"""Module which contain state for main game"""

import sys
import os

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

import pygame as pg
from .base_state import State
from .menu_button import Button


class MenuState(State):
    def __init__(self) -> None:
        super().__init__()

    def update_active_button(self, new_ind: int) -> None:
        self.buttons_list[self.current_active_button_ind].change_active()
        self.current_active_button_ind: int = new_ind
        self.buttons_list[self.current_active_button_ind].change_active()

    def load_graphics(self) -> None:
        self.background: pg.Surface = pg.image.load("assets/graphics/menu/menu_bg.png").convert_alpha()
        self.game_title: pg.Surface = pg.image.load("assets/graphics/menu/game_title.png").convert_alpha()
        self.game_title = pg.transform.rotozoom(self.game_title, 0, 0.8)

        self.game_title_bg: pg.Surface = pg.image.load("assets/graphics/menu/title_bg.png").convert_alpha()
        self.game_title_bg = pg.transform.rotozoom(self.game_title_bg, 0, 0.8)

        self.buttons_bg: pg.Surface = pg.image.load("assets/graphics/menu/buttons_bg.png")

    def setup_rects_and_buttons(self) -> None:
        self.game_title_bg_rect: pg.Rect = self.game_title_bg.get_rect(center=(721, 150))
        self.buttons_bg_rect: pg.Rect = self.buttons_bg.get_rect(center=(721, 510))

        self.game_title_rect: pg.Rect = self.game_title.get_rect(
            center=(self.game_title_bg_rect.centerx + 10, self.game_title_bg_rect.centery)
        )

        self.play_button = Button(
            self.buttons_bg_rect.centerx,
            self.buttons_bg_rect.centery - 115,
            "assets/graphics/menu/play_button.png",
            "assets/graphics/menu/play_button_active.png",
        )
        self.leave_button = Button(
            self.buttons_bg_rect.centerx,
            self.buttons_bg_rect.centery + 20,
            "assets/graphics/menu/leave_button.png",
            "assets/graphics/menu/leave_button_active.png",
        )

        self.volume_button_on = Button(
            self.buttons_bg_rect.centerx - 130,
            self.buttons_bg_rect.centery + 140,
            "assets/graphics/menu/volume_button_on.png",
            "assets/graphics/menu/volume_button_on_active.png",
        )
        self.volume_button_off = Button(
            self.buttons_bg_rect.centerx - 130,
            self.buttons_bg_rect.centery + 140,
            "assets/graphics/menu/volume_button_off.png",
            "assets/graphics/menu/volume_button_off_active.png",
        )

        self.music_button_on = Button(
            self.buttons_bg_rect.centerx + 130,
            self.buttons_bg_rect.centery + 140,
            "assets/graphics/menu/music_button_on.png",
            "assets/graphics/menu/music_button_on_active.png",
        )
        self.music_button_off = Button(
            self.buttons_bg_rect.centerx + 130,
            self.buttons_bg_rect.centery + 140,
            "assets/graphics/menu/music_button_off.png",
            "assets/graphics/menu/music_button_off_active.png",
        )

        self.buttons_list: list[Button] = [
            self.play_button,
            self.leave_button,
            self.volume_button_on,
            self.music_button_on,
        ]
        self.music_button_off.change_active()
        self.volume_button_off.change_active()
        self.volume_buttons: list[Button] = [self.volume_button_on, self.volume_button_off]
        self.music_buttons: list[Button] = [self.music_button_on, self.music_button_off]
        self.current_active_button_ind = 0
        self.buttons_list[self.current_active_button_ind].change_active()
        self.current_volume_button_ind = 0
        self.current_music_button_ind = 0

    def cleanup(self) -> None:
        super().cleanup()
        self.update_active_button(0)

    def get_event(self, event) -> None:
        if event.type == pg.KEYDOWN:
            pressed_key = event.key
            if pressed_key == pg.K_SPACE:
                if self.current_active_button_ind == 0:
                    self.done = True
                    self.next = "gameplay"
                elif self.current_active_button_ind == 1:
                    self.done = True
                    self.quit = True
                elif self.current_active_button_ind == 2:
                    self.current_volume_button_ind = int(not self.current_volume_button_ind)
                    self.buttons_list[self.current_active_button_ind] = self.volume_buttons[
                        self.current_volume_button_ind
                    ]

                elif self.current_active_button_ind == 3:
                    self.current_music_button_ind = int(not self.current_music_button_ind)
                    self.buttons_list[self.current_active_button_ind] = self.music_buttons[
                        self.current_music_button_ind
                    ]

            # change active button in the menu
            elif pressed_key in [pg.K_w, pg.K_a, pg.K_s, pg.K_d]:
                if self.current_active_button_ind == 0 and pressed_key == pg.K_s:
                    self.update_active_button(1)

                elif self.current_active_button_ind == 1:
                    possible_keys: dict[int, int] = {pg.K_w: -1, pg.K_s: 1}
                    if pressed_key in possible_keys:
                        self.update_active_button(self.current_active_button_ind + possible_keys[pressed_key])

                elif self.current_active_button_ind in (2, 3):
                    if pressed_key == pg.K_w:
                        self.update_active_button(1)
                    elif self.current_active_button_ind == 2 and pressed_key == pg.K_d:
                        self.update_active_button(3)
                    elif self.current_active_button_ind == 3 and pressed_key == pg.K_a:
                        self.update_active_button(2)

    def draw(self, screen) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(self.game_title_bg, self.game_title_bg_rect)
        screen.blit(self.game_title, self.game_title_rect)
        for button in self.buttons_list:
            button.draw(screen)

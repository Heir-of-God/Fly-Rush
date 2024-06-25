"""Module which contains state for main game"""

import sys
import os


# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

import pygame as pg
from .base_state import State
from .menu_button import Button
from save_load_system import GameSaveLoadSystem
from constants import BEST_SCORE_FILE_NAME


class MenuState(State):
    def __init__(self) -> None:
        self.save_load_system = GameSaveLoadSystem()
        self.font_bauhaus93: pg.font.Fon = pg.font.Font("assets/fonts/bauhaus93.ttf", 34)
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

    def startup(self) -> None:
        self.audio_controller.change_music("menu")
        record: int = self.save_load_system.load_game_data({BEST_SCORE_FILE_NAME: 0})[BEST_SCORE_FILE_NAME]
        self.player_record_surf: pg.Surface = self.font_bauhaus93.render(
            "Your record: " + str(record).zfill(6), True, "#FFD723"
        )
        self.player_record_rect: pg.Rect = self.player_record_surf.get_rect()
        self.player_record_rect.topleft = (10, 5)

    def get_event(self, event) -> None:
        if event.type == pg.KEYDOWN:
            pressed_key = event.key
            if pressed_key == pg.K_SPACE:
                self.audio_controller.play_sound("button_confirm")
                if self.current_active_button_ind == 0:
                    self.done = True
                    self.next = "gameplay"
                elif self.current_active_button_ind == 1:
                    self.done = True
                    self.quit = True
                elif self.current_active_button_ind == 2:
                    self.audio_controller.flip_volume_status()
                    self.current_volume_button_ind = int(not self.current_volume_button_ind)
                    self.buttons_list[self.current_active_button_ind] = self.volume_buttons[
                        self.current_volume_button_ind
                    ]

                elif self.current_active_button_ind == 3:
                    self.audio_controller.flip_music_status()
                    self.current_music_button_ind = int(not self.current_music_button_ind)
                    self.buttons_list[self.current_active_button_ind] = self.music_buttons[
                        self.current_music_button_ind
                    ]

            # change active button in the menu
            elif pressed_key in [pg.K_w, pg.K_a, pg.K_s, pg.K_d]:
                button_change = False
                if self.current_active_button_ind == 0 and pressed_key == pg.K_s:
                    button_change = True
                    self.update_active_button(1)

                elif self.current_active_button_ind == 1:
                    possible_keys: dict[int, int] = {pg.K_w: -1, pg.K_s: 1}
                    if pressed_key in possible_keys:
                        button_change = True
                        self.update_active_button(self.current_active_button_ind + possible_keys[pressed_key])

                elif self.current_active_button_ind in (2, 3):
                    if pressed_key == pg.K_w:
                        button_change = True
                        self.update_active_button(1)
                    elif self.current_active_button_ind == 2 and pressed_key == pg.K_d:
                        button_change = True
                        self.update_active_button(3)
                    elif self.current_active_button_ind == 3 and pressed_key == pg.K_a:
                        button_change = True
                        self.update_active_button(2)
                if button_change:
                    self.audio_controller.play_sound("button_change")

    def draw(self, screen) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(self.game_title_bg, self.game_title_bg_rect)
        screen.blit(self.game_title, self.game_title_rect)
        screen.blit(self.player_record_surf, self.player_record_rect)
        for button in self.buttons_list:
            button.draw(screen)

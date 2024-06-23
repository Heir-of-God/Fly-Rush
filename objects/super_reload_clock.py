"""Module which contains class for clock object which dealing with super ability reload time"""

import os
import sys
import pygame as pg

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

from constants import TORPEDO_TIME_RELOAD


class ReloadTimer:

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.image.load(f"assets/graphics/clock_timer/clock_{str(i)}.png") for i in range(1, 17, 1)
        ]
        for ind in range(len(cls.images)):
            cls.images[ind] = pg.transform.rotozoom(cls.images[ind], 0, 0.08).convert_alpha()

    def __init__(self, centerx: int, centery: int, path_to_font_for_countdown: str) -> None:
        self.reload_time: int = 0
        self.image: pg.Surface = self.images[0]
        self.rect: pg.Rect = self.image.get_rect(center=(centerx, centery))
        self.timer_font = pg.font.Font(path_to_font_for_countdown, 20)

    def set_timer(self) -> None:
        self.reload_time = TORPEDO_TIME_RELOAD

    def reset_timer(self) -> None:
        self.reload_time = 0

    def timer_animation(self) -> None:
        cur_step = int(((TORPEDO_TIME_RELOAD - self.reload_time) / TORPEDO_TIME_RELOAD) * len(self.images))
        if not cur_step >= len(self.images):
            self.image = self.images[cur_step]

    def update(self) -> None:
        if self.reload_time != 0:
            self.reload_time -= 1
            self.timer_animation()

    def draw(self, screen: pg.Surface) -> None:
        if self.reload_time != 0:
            text_color: str = (
                "#FF3333"
                if self.reload_time > TORPEDO_TIME_RELOAD / 2
                else "#FFA30B" if self.reload_time > TORPEDO_TIME_RELOAD / 4 else "#83FF67"
            )
            time_text_surf: pg.Surface = self.timer_font.render(f"{round(self.reload_time / 60, 2)}", True, text_color)
            screen.blit(self.image, self.rect)
            screen.blit(time_text_surf, time_text_surf.get_rect(center=self.rect.center))

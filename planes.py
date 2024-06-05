"""Module which contains classes for player's plane, enemies' planes and base class for them"""

from random import choice
import pygame as pg
from constants import GAME_SCREEN_HEIGHT, GAME_SCREEN_WIDTH, PLAYER_SPEED_X_RIGHT, PLAYER_SPEED_X_LEFT, PLAYER_SPEED_Y


class Plane(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.reload_time = 0

    def create_collide_rect(self):
        self.collide_rect = self.rect.copy()
        self.collide_rect.scale_by_ip(0.71, 0.8)

    def bullet_reload(self) -> None:
        if self.reload_time != 0:
            self.reload_time -= 1

    def check_left_border(self) -> bool:
        return self.rect.left >= 0

    def check_right_border(self) -> bool:
        return self.rect.right <= GAME_SCREEN_WIDTH

    def check_top_border(self) -> bool:
        return self.rect.top >= 0

    def check_bottom_border(self) -> bool:
        return self.rect.bottom <= GAME_SCREEN_HEIGHT

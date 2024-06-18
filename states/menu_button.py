"""Module which contains base class for menu button"""

import pygame as pg


class Button:

    def load_graphics(self, normal_button_path, active_button_path) -> None:
        self.image_normal: pg.Surface = pg.image.load(normal_button_path).convert_alpha()
        self.image_active: pg.Surface = pg.image.load(active_button_path).convert_alpha()

    def __init__(self, x_pos_center, y_pos_center, normal_button_path, active_button_path) -> None:
        self.load_graphics(normal_button_path, active_button_path)
        self.rect: pg.Rect = self.image_normal.get_rect(center=(x_pos_center, y_pos_center))
        self.currently_active: bool = False

    def change_active(self) -> None:
        self.currently_active = not self.currently_active

    def draw(self, screen: pg.Surface) -> None:
        if self.currently_active:
            screen.blit(self.image_active, self.rect)
        else:
            screen.blit(self.image_normal, self.rect)

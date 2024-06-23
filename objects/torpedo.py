"""Module which contains Torpedo class and its full logic"""

from random import choice, randint
import pygame as pg
from constants import (
    GAME_SCREEN_HEIGHT,
    GAME_SCREEN_WIDTH,
    TORPEDO_DELTA_X,
    TORPEDO_DELTA_Y,
    TORPEDO_SPEED_Y,
    TORPEDO_EXPLOSION_RECT_SIDE,
)


class Torpedo(pg.sprite.Sprite):

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.image.load(f"assets/graphics/torpedo/torpedo_{i}.png") for i in range(1, 4, 1)
        ]
        for ind in range(len(cls.images)):
            cls.images[ind] = pg.transform.rotozoom(cls.images[ind], 0, 0.18).convert_alpha()

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__()
        self.image: pg.Surface = self.images[0]
        self.rect: pg.Rect = self.image.get_rect(midleft=(start_x, start_y))
        self.target_center_x: int = int(GAME_SCREEN_WIDTH * 0.85) + randint(-TORPEDO_DELTA_X, TORPEDO_DELTA_X)
        self.start_center_y: int = self.rect.centery
        self.y_step: float = choice([-TORPEDO_SPEED_Y, TORPEDO_SPEED_Y])
        self.current_animation_step = 0

    def animation(self) -> None:
        self.image = self.images[self.current_animation_step // 5]
        self.current_animation_step += 1
        if self.current_animation_step >= 15:
            self.current_animation_step = 0

    def move(self) -> None:
        self.rect.x += 8
        self.rect.y += self.y_step
        if (
            abs(self.start_center_y - self.rect.centery) > TORPEDO_DELTA_Y
            or self.rect.top < 0
            or self.rect.bottom > GAME_SCREEN_HEIGHT
        ):
            self.rect.centery = (
                self.start_center_y + TORPEDO_DELTA_Y if self.y_step > 0 else self.start_center_y - TORPEDO_DELTA_Y
            )
            self.rect.top = max(0, self.rect.top)
            self.rect.bottom = min(GAME_SCREEN_HEIGHT, self.rect.bottom)
            self.y_step = -self.y_step

    def is_ready_to_explode(self) -> bool:
        return self.rect.centerx >= self.target_center_x

    def get_explosion_rect(self) -> pg.Rect:
        explosion_rect = pg.Rect(0, 0, TORPEDO_EXPLOSION_RECT_SIDE, TORPEDO_EXPLOSION_RECT_SIDE)
        explosion_rect.center = self.rect.center
        return explosion_rect

    def update(self):
        self.animation()
        self.move()

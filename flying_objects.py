"""Module which contains classes for some collectable flying objects in game sich as coins, stars etc"""

from random import choice, randint
import pygame as pg
from constants import (
    GAME_SCREEN_HEIGHT,
    GAME_SCREEN_WIDTH,
    BRONZE_COINS_NUMBER,
    SILVER_COINS_NUMBER,
    GOLD_COINS_NUMBER,
    BRONZE_COIN_VALUE,
    SILVER_COIN_VALUE,
    GOLD_COIN_VALUE,
    FPS,
    COINS_SPEED_Y,
    COINS_SPEED_X,
)


class FlyingObject(pg.sprite.Sprite):
    """Base class for all flying objects in game"""

    def __init__(self) -> None:
        super().__init__()

    def check_right_board(self) -> None:
        if self.rect.right <= 0:
            self.kill()


class Coin(FlyingObject):
    types_to_choose: list[str] = (
        ["bronze"] * BRONZE_COINS_NUMBER + ["silver"] * SILVER_COINS_NUMBER + ["gold"] * GOLD_COINS_NUMBER
    )
    values: dict[str, int] = {"bronze": BRONZE_COIN_VALUE, "silver": SILVER_COIN_VALUE, "gold": GOLD_COIN_VALUE}

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: dict[str, list[pg.Surface]] = {}  # coin type name -> list of images for this coin
        for t in ["bronze", "silver", "gold"]:
            cls.images[t] = [
                pg.transform.rotozoom(
                    pg.image.load(f"assets/graphics/flying_objects/coins/{t}/coin_{i}.png"), 0, 0.7
                ).convert_alpha()
                for i in range(0, 15, 1)
            ]

    def __init__(self) -> None:
        super().__init__()
        self.coin_type: str = choice(self.types_to_choose)
        self.images: list[pg.Surface] = self.images[self.coin_type]
        self.current_animation_step: int = 0
        self.image: pg.Surface = self.images[0]
        self.rect: pg.Rect = self.image.get_rect(
            topleft=(
                GAME_SCREEN_WIDTH,
                randint(0, GAME_SCREEN_HEIGHT - self.image.get_height()),
            )
        )
        self.create_collide_rect()

    def animation(self) -> None:
        self.current_animation_step += 15 / (FPS * 0.5)  # Two full animations in 1 second
        if self.current_animation_step > 14:
            self.current_animation_step = 0
        self.image = self.images[int(self.current_animation_step)]

    def create_collide_rect(self) -> None:
        self.collide_rect: pg.Rect = self.rect.copy()
        self.collide_rect.scale_by_ip(0.43, 0.38)  # coefficients are hardcoded through tests

    def move(self) -> None:
        if int(self.current_animation_step) >= 10 or int(self.current_animation_step) <= 2:  # If coin is flying up
            self.rect.top = max(0, self.rect.top - COINS_SPEED_Y)
            self.rect.x -= COINS_SPEED_X
        else:  # If coin if flying down
            self.rect.bottom = min(GAME_SCREEN_HEIGHT, self.rect.bottom + COINS_SPEED_Y)
            self.rect.x -= COINS_SPEED_X
        self.update_collide_rect()

    def update_collide_rect(self) -> None:
        self.collide_rect.center = self.rect.center

    def get_value(self) -> int:
        return self.values[self.coin_type]

    def update(self):
        self.animation()
        self.move()

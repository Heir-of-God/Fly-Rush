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
    SCORE_STAR_ANGLE_SPEED,
    SCORE_STAR_VALUE_RANGE,
    SCORE_STAR_SPEED_X,
    FLYING_HEART_DELTA_Y,
    FLYING_HEART_SPEED_Y,
)


class FlyingObject(pg.sprite.Sprite):
    """Base class for all flying objects in game"""

    def __init__(self) -> None:
        super().__init__()

    def check_right_board(self) -> None:
        if self.rect.right <= 0:
            self.kill()

    def set_up_rects(self) -> None:
        self.rect: pg.Rect = self.image.get_rect(
            topleft=(
                GAME_SCREEN_WIDTH,
                randint(0, GAME_SCREEN_HEIGHT - self.image.get_height()),
            )
        )
        self.create_collide_rect()

    def create_collide_rect(self) -> None:
        self.collide_rect: pg.Rect = self.rect.copy()

    def update_collide_rect(self) -> None:
        self.collide_rect.center = self.rect.center


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
        self.set_up_rects()

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

    def get_value(self) -> int:
        return self.values[self.coin_type]

    def update(self) -> None:
        self.animation()
        self.move()


class ScoreStar(FlyingObject):

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.transform.rotozoom(
                pg.image.load("assets/graphics/flying_objects/score_star/star.png"), 0, 0.25
            ).convert_alpha()
        ]

    def __init__(self) -> None:
        super().__init__()
        self.image: pg.Surface = self.images[0]
        self.start_image: pg.Surface = self.image  # Saving start image to then rotate it
        self.current_angle = 0
        self.angle_speed: int = choice([SCORE_STAR_ANGLE_SPEED, -SCORE_STAR_ANGLE_SPEED])
        self.value: int = randint(SCORE_STAR_VALUE_RANGE[0], SCORE_STAR_VALUE_RANGE[1])
        self.set_up_rects()

    def move(self) -> None:
        self.rect.x -= SCORE_STAR_SPEED_X

    def animation(self) -> None:
        self.image = pg.transform.rotate(self.start_image, self.current_angle)
        self.current_angle += self.angle_speed
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self) -> None:
        self.animation()
        self.move()
        self.update_collide_rect()


class FlyingHeart(FlyingObject):

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.transform.rotozoom(
                pg.image.load(f"assets/graphics/flying_hearts/hearts/heart{i}.png").convert_alpha(), 0, 0.3
            )
            for i in range(1, 6, 1)
        ]

    def __init__(self) -> None:
        super().__init__()
        self.image: pg.Surface = self.images[0]
        self.current_animation_step: int = 0
        self.set_up_rects()
        self.start_coor_y_center = self.rect.centery
        self.pos_y_delta: int = randint(FLYING_HEART_DELTA_Y[0], FLYING_HEART_DELTA_Y[1])
        self.speed_y: int = choice(
            [FLYING_HEART_SPEED_Y, -FLYING_HEART_SPEED_Y]
        )  # randomly go from start to bottom or to the top

    def animation(self) -> None:
        self.current_animation_step += 1
        if self.current_animation_step > 74:  # 75 // 15 = 5 -> last index is 4 because there's 5 heart's images
            self.current_animation_step = 0
        self.image = self.images[self.current_animation_step // 15]

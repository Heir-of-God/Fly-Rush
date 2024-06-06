"""Module which contains classes for player's plane, enemies' planes and base class for them"""

from random import choice, randint
import pygame as pg
from constants import GAME_SCREEN_HEIGHT, GAME_SCREEN_WIDTH, PLAYER_SPEED_X_RIGHT, PLAYER_SPEED_X_LEFT, PLAYER_SPEED_Y


class Plane(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.reload_time = 0
        self.type = 1

    def create_collide_rect(self) -> None:
        """Create collide rect for plane based on its type (there's two types: 1 (smaller) and 2 (bigger). Player's plane always type 1)"""
        self.collide_rect = self.rect.copy()
        y_scale = 0.62 if self.type == 1 else 0.75
        self.collide_rect.scale_by_ip(0.70, y_scale)

    def bullet_reload(self) -> None:
        if self.reload_time != 0:
            self.reload_time -= 1


class PlayerPlane(Plane):
    def __init__(self) -> None:
        super().__init__()
        self.image: pg.Surface = pg.transform.rotozoom(
            pg.image.load(f"assets/graphics/planes/{choice(['red', 'blue', 'green', 'yellow'])}1.png"), 0, 0.15
        ).convert_alpha()
        self.rect: pg.Rect = self.image.get_rect(center=(706.5, 384))
        self.create_collide_rect()

    def handle_player_input(self) -> None:
        keys: pg.key.ScancodeWrapper = pg.key.get_pressed()
        # Player movement considering edges of the screen
        if keys[pg.K_w]:
            self.rect.top = max(self.rect.top - PLAYER_SPEED_Y, 0)
        if keys[pg.K_s]:
            self.rect.bottom = min(self.rect.bottom + PLAYER_SPEED_Y, GAME_SCREEN_HEIGHT)
        if keys[pg.K_d]:
            self.rect.right = min(self.rect.right + PLAYER_SPEED_X_RIGHT, GAME_SCREEN_WIDTH)
        if keys[pg.K_a]:
            self.rect.left = max(self.rect.left - PLAYER_SPEED_X_LEFT, 0)
        self.collide_rect.center = self.rect.centerx, self.rect.centery + (
            self.rect.width * 0.08 if self.type == 1 else self.rect.width * 0.04
        )

    def update(self) -> None:
        self.bullet_reload()
        self.handle_player_input()


class EnemyPlane(Plane):
    def __init__(self) -> None:
        super().__init__()
        self.type: int = randint(1, 2)
        self.image: pg.Surface = pg.transform.rotozoom(
            pg.image.load(f"assets/graphics/planes/{choice(['red', 'blue', 'green', 'yellow'])}{self.type}.png"),
            0,
            0.15,
        ).convert_alpha()
        self.image_width: int = self.image.get_width()
        self.rect: pg.Rect = self.image.get_rect(
            topleft=(
                randint(GAME_SCREEN_WIDTH, GAME_SCREEN_WIDTH + self.image_width * 3),
                randint(0, GAME_SCREEN_HEIGHT - self.image.get_height()),
            )
        )
        self.right_target_x: int = randint(GAME_SCREEN_WIDTH - self.image_width * 3, GAME_SCREEN_WIDTH)
        self.create_collide_rect()

"""Module which contains classes for player's plane, enemies' planes and base class for them"""

from random import choice, randint
import pygame as pg
from constants import (
    GAME_SCREEN_HEIGHT,
    GAME_SCREEN_WIDTH,
    PLAYER_SPEED_X_RIGHT,
    PLAYER_SPEED_X_LEFT,
    PLAYER_SPEED_Y,
    ENEMY_SPEED_X,
    ENEMY_SPEED_Y,
    ENEMY_DELTA_Y,
)


class Plane(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.reload_time = 0
        self.type = 1

    def create_collide_rect(self) -> None:
        """Create collide rect for plane based on its type (there's two types: 1 (smaller) and 2 (bigger). Player's plane always type 1)"""
        self.collide_rect: pg.Rect = self.rect.copy()
        y_scale: float = 0.62 if self.type == 1 else 0.75
        self.collide_rect.scale_by_ip(0.70, y_scale)

    def bullet_reload(self) -> None:
        if self.reload_time != 0:
            self.reload_time -= 1

    def update_collide_rect(self) -> None:
        self.collide_rect.center = self.rect.centerx, self.rect.centery + (
            self.rect.width * 0.08 if self.type == 1 else self.rect.width * 0.04
        )

    def set_reload_time(self, val: int) -> None:
        self.reload_time: int = val

    def can_shoot(self) -> bool:
        return self.reload_time == 0


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
        self.update_collide_rect()

    def get_bullet_position(self) -> tuple[int, int]:
        """Returns position for bullet to appear (left bound for x and center for y)"""
        return (self.collide_rect.right, self.collide_rect.centery)

    def update(self) -> None:
        self.bullet_reload()
        self.handle_player_input()


class EnemyPlane(Plane):
    def __init__(self) -> None:
        super().__init__()
        self.type: int = randint(1, 2)
        self.image: pg.Surface = pg.image.load(
            f"assets/graphics/planes/{choice(['red', 'blue', 'green', 'yellow'])}{self.type}.png"
        )
        self.image = pg.transform.rotozoom(self.image, 0, 0.15).convert_alpha()
        self.image = pg.transform.flip(self.image, True, False)

        self.image_width: int = self.image.get_width()
        self.rect: pg.Rect = self.image.get_rect(
            topleft=(
                randint(GAME_SCREEN_WIDTH, GAME_SCREEN_WIDTH + self.image_width * 3),
                randint(0, GAME_SCREEN_HEIGHT - self.image.get_height()),
            )
        )
        self.right_target_x: int = randint(GAME_SCREEN_WIDTH - self.image_width * 3, GAME_SCREEN_WIDTH)
        self.speed_y: int = choice([ENEMY_SPEED_Y, -ENEMY_SPEED_Y])
        self.pos_y_delta: int = randint(ENEMY_DELTA_Y[0], ENEMY_DELTA_Y[1])
        self.start_coor_y_top: int = self.rect.top
        self.create_collide_rect()

    def move(self) -> None:
        # if enemy hasn't reached its target yet
        if self.rect.right >= self.right_target_x:
            self.rect.x -= ENEMY_SPEED_X
        else:
            self.rect.y += self.speed_y
            if self.speed_y > 0:  # Enemy is going down
                if self.rect.bottom >= GAME_SCREEN_HEIGHT:
                    self.rect.bottom = GAME_SCREEN_HEIGHT
                    self.speed_y *= -1
                elif self.rect.bottom >= self.start_coor_y_top + self.rect.height + self.pos_y_delta:
                    self.speed_y *= -1

            else:  # enemy is going up
                if self.rect.top <= 0:
                    self.rect.top = 0
                    self.speed_y *= -1
                elif self.rect.top <= self.start_coor_y_top - self.pos_y_delta:
                    self.speed_y *= -1
        self.update_collide_rect()

    def update(self) -> None:
        self.bullet_reload()
        self.move()

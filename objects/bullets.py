"""Module which describe Bullet classes"""

import pygame as pg
from constants import PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED, GAME_SCREEN_WIDTH


class Bullet(pg.sprite.Sprite):
    """Base Bullet class for inheritance (PlayerBullet and EnemyBullet)"""

    def __init__(self) -> None:
        super().__init__()

    def create_collide_rect(self) -> None:
        self.collide_rect: pg.Rect = self.rect.copy()
        self.collide_rect.inflate_ip(-10, -5)  # (hardcoded)

    def update_collide_rect(self) -> None:
        self.collide_rect.center = self.rect.center

    def check_boards(self) -> None:
        """Method check that bullet is still in the game window and if it's not delete it from groups"""
        if self.rect.right <= 0 or self.rect.left >= GAME_SCREEN_WIDTH:
            self.kill()

    def move(self) -> None:
        self.rect.x += self.speed
        self.update_collide_rect()

    def update(self) -> None:
        self.move()
        self.check_boards()


class PlayerBullet(Bullet):
    """Class for player's bullet"""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__()
        self.image: pg.Surface = self.images[0]

        self.rect: pg.Rect = self.image.get_rect()
        self.rect.left = start_x
        self.rect.centery = start_y
        self.create_collide_rect()

        self.speed: int = PLAYER_BULLET_SPEED

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [pg.image.load(f"assets/graphics/bullets/bullet2.png")]
        cls.images[0] = pg.transform.rotozoom(cls.images[0], 0, 0.25).convert_alpha()


class EnemyBullet(Bullet):
    """Class for enemy's bullet"""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__()

        self.image: pg.Surface = self.images[0]

        self.rect: pg.Rect = self.image.get_rect()
        self.rect.right = start_x
        self.rect.centery = start_y
        self.create_collide_rect()

        self.speed: int = -ENEMY_BULLET_SPEED

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [pg.image.load(f"assets/graphics/bullets/bullet1.png")]
        cls.images[0] = pg.transform.rotozoom(cls.images[0], 0, 0.25).convert_alpha()
        cls.images[0] = pg.transform.flip(cls.images[0], True, False).convert_alpha()

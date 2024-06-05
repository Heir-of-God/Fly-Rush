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
        self.collide_rect.scale_by_ip(0.75, 0.6)

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
        self.collide_rect.center = self.rect.centerx, self.rect.centery + 10

    def update(self):
        self.bullet_reload()
        self.handle_player_input()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pg.draw.rect(screen, (255, 0, 0), self.collide_rect)
        # TODO remove line above, just to test collide rectangles

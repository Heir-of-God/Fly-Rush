"""Module which contain state for main game"""

import sys
import os

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

from random import randint
import pygame as pg
from background import GameBackground
from .base_state import State
from constants import PLANE_EXPLOSION_SIZE_COEFFICIENT, PLAYER_RELOAD_TIME
from player import Player
from objects.explosion import Explosion
from objects.planes import EnemyPlane
from objects.bullets import PlayerBullet, EnemyBullet
from objects.flying_objects import Coin, ScoreStar, FlyingHeart


class MainGameState(State):
    def __init__(self) -> None:
        super().__init__()
        self.game_background: GameBackground = GameBackground()  # Class to move and draw game background

        self.player = Player()
        self.player_group = pg.sprite.GroupSingle(self.player.player_plane)  # Class to control the player
        self.player_bullets_group = pg.sprite.Group()  # Class to control player's bullets

        self.enemies_group = pg.sprite.Group()  # Class to control enemies
        self.enemies_bullets_group = pg.sprite.Group()  # Control all enemies' bullets

        self.explosion_group = pg.sprite.Group()  # Control all explosions

        self.coins_group = pg.sprite.Group()  # Controll all coins
        self.score_stars_group = pg.sprite.Group()  # Controll all score stars
        self.flying_hearts_group = pg.sprite.Group()  # Controll all flying hearts

        self.enemy_spawn_event: int = pg.USEREVENT + 1
        self.coin_spawn_event: int = pg.USEREVENT + 2
        self.star_spawn_event: int = pg.USEREVENT + 3
        self.flying_heart_spawn_event: int = pg.USEREVENT + 4

        self.set_timers()

    def reset_game(self) -> None:
        self.enemies_bullets_group.empty()
        self.enemies_group.empty()
        self.player_bullets_group.empty()
        self.explosion_group.empty()
        self.coins_group.empty()
        self.score_stars_group.empty()
        self.flying_hearts_group.empty()
        self.player_group.sprite.reset_position()
        self.player.reset_coins()
        self.player.reset_score()

        self.set_timers()

    def set_timers(self) -> None:
        # TOFIX Pygame events running even when paused, rework them with conunters inside game state
        pg.time.set_timer(self.enemy_spawn_event, 1500)
        pg.time.set_timer(self.coin_spawn_event, 6000)
        pg.time.set_timer(self.star_spawn_event, 6000)
        pg.time.set_timer(self.flying_heart_spawn_event, 8000)

    def get_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "pause"
                self.done = True

        elif event.type == self.enemy_spawn_event:
            if randint(0, 3):
                if len(self.enemies_group) < 16:
                    self.enemies_group.add(EnemyPlane())

        elif event.type == self.coin_spawn_event:
            if randint(1, 3):  # Now spawning always. TODO (TOCHANGE)
                self.coins_group.add(Coin())

        elif event.type == self.star_spawn_event:
            if randint(1, 2):
                self.score_stars_group.add(ScoreStar())

        elif event.type == self.flying_heart_spawn_event:
            if randint(1, 2):
                self.flying_hearts_group.add(FlyingHeart())

    def get_keys(self, keys: pg.key.ScancodeWrapper) -> None:
        # handle keys
        if keys[pg.K_SPACE] and self.player_group.sprite.can_shoot():
            self.player_group.sprite.set_reload_time(PLAYER_RELOAD_TIME)
            self.player_bullets_group.add(PlayerBullet(*self.player_group.sprite.get_bullet_position()))

        # Handle enemy shooting
        for enemy in self.enemies_group.sprites():
            if enemy.can_shoot():
                self.enemies_bullets_group.add(EnemyBullet(*enemy.get_bullet_position()))
                enemy.update_reload_time()

    def load_graphics(self) -> None:
        PlayerBullet.load_graphics()
        EnemyBullet.load_graphics()
        Explosion.load_graphics()
        Coin.load_graphics()
        ScoreStar.load_graphics()
        FlyingHeart.load_graphics()

    def check_collisions(self) -> None:
        for player_bullet in self.player_bullets_group.sprites():
            killed_enemies: list[EnemyPlane] = pg.sprite.spritecollide(
                player_bullet,
                self.enemies_group,
                False,
                lambda bull, enem: bull.collide_rect.colliderect(enem.collide_rect),
            )  # get list of enemies which collide with bullet
            if killed_enemies:
                # TOFIX enemies can be killed while they're not even in screen
                killed: EnemyPlane = killed_enemies[0]
                self.explosion_group.add(Explosion(killed.get_rects_center(), PLANE_EXPLOSION_SIZE_COEFFICIENT))
                killed.kill()
                player_bullet.kill()

        if pg.sprite.groupcollide(
            self.player_group,
            self.enemies_bullets_group,
            False,
            False,
            lambda pl, bull: pl.collide_rect.colliderect(bull.collide_rect),
        ):
            self.reset_game()

        collected_coins: list[Coin] = pg.sprite.spritecollide(
            self.player_group.sprite,
            self.coins_group,
            False,
            lambda pl, coin: pl.collide_rect.colliderect(coin.collide_rect),
        )
        for coin in collected_coins:
            coin.kill()
            self.player.add_to_coins(coin.get_value())

        collected_stars: list[ScoreStar] = pg.sprite.spritecollide(
            self.player_group.sprite,
            self.score_stars_group,
            False,
            lambda pl, star: pl.collide_rect.colliderect(star.collide_rect),
        )
        for star in collected_stars:
            star.kill()
            self.player.add_to_score(star.get_value())

    def update(self) -> None:
        """Method which updates all game with its logic"""
        self.game_background.move_background()
        self.player_group.update()
        self.enemies_group.update()
        self.coins_group.update()
        self.score_stars_group.update()
        self.flying_hearts_group.update()
        self.player_bullets_group.update()
        self.enemies_bullets_group.update()
        self.explosion_group.update()
        self.check_collisions()

    def draw(self, screen) -> None:
        self.game_background.draw_background(screen)
        self.player_bullets_group.draw(screen)
        self.enemies_bullets_group.draw(screen)
        self.coins_group.draw(screen)
        self.score_stars_group.draw(screen)
        self.flying_hearts_group.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.explosion_group.draw(screen)

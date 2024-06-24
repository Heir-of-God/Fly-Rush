"""Module which contain state for main game"""

import sys
import os
from typing import Callable

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

from random import randint
import pygame as pg
from background import GameBackground
from .base_state import State
from constants import (
    PLANE_EXPLOSION_SIZE_COEFFICIENT,
    PLAYER_RELOAD_TIME,
    GAME_SCREEN_WIDTH,
    BEST_SCORE_FILE_NAME,
    TORPEDO_EXPLOSION_SIZE_COEFFICIENT,
    TORPEDO_COIN_PRICE,
)
from player import Player
from objects.explosion import Explosion
from objects.planes import EnemyPlane
from objects.bullets import PlayerBullet, EnemyBullet
from objects.flying_objects import Coin, ScoreStar, FlyingHeart
from objects.super_reload_clock import ReloadTimer
from objects.torpedo import Torpedo
from save_load_system import GameSaveLoadSystem


class MainGameState(State):
    def __init__(self) -> None:
        super().__init__()
        self.save_load_system: GameSaveLoadSystem = GameSaveLoadSystem()
        self.game_background: GameBackground = GameBackground()  # Class to move and draw game background

        self.player = Player()
        self.player_group = pg.sprite.GroupSingle(self.player.player_plane)  # Class to control the player
        self.player_bullets_group = pg.sprite.Group()  # Class to control player's bullets

        self.enemies_group = pg.sprite.Group()  # Class to control enemies
        self.enemies_bullets_group = pg.sprite.Group()  # Control all enemies' bullets

        self.torpedo_group = pg.sprite.Group()  # Control all torpedos
        self.explosion_group = pg.sprite.Group()  # Control all explosions

        self.coins_group = pg.sprite.Group()  # Controll all coins
        self.score_stars_group = pg.sprite.Group()  # Controll all score stars
        self.flying_hearts_group = pg.sprite.Group()  # Controll all flying hearts

        self.enemy_spawn_event: int = pg.USEREVENT + 1
        self.coin_spawn_event: int = pg.USEREVENT + 2
        self.star_spawn_event: int = pg.USEREVENT + 3
        self.flying_heart_spawn_event: int = pg.USEREVENT + 4

        self.set_timers()

    def load_graphics(self) -> None:
        PlayerBullet.load_graphics()
        EnemyBullet.load_graphics()
        Torpedo.load_graphics()
        ReloadTimer.load_graphics()
        Explosion.load_graphics()
        Coin.load_graphics()
        ScoreStar.load_graphics()
        FlyingHeart.load_graphics()
        self.extra_life_surfs: list[pg.Surface] = [
            pg.transform.rotozoom(
                pg.image.load(f"assets/graphics/flying_objects/hearts/heart{i}.png"), 0, 0.21
            ).convert_alpha()
            for i in range(2)
        ]

    def setup_rects_and_objects(self) -> None:
        """Method to load all needed objects and rects after graphic has been loaded"""
        self.bauhaus_font: pg.font.Font = pg.font.Font("assets/fonts/bauhaus93.ttf", 34)

        self.get_updated_coin_surf: Callable[..., pg.Surface] = lambda: self.bauhaus_font.render(
            str(self.player.coins).zfill(5), True, "#fee201"
        )

        self.player_coins_surf: pg.Surface = self.get_updated_coin_surf()
        self.player_coins_background: pg.Surface = pg.image.load(
            "assets/graphics/backgrounds/coin_background.png"
        ).convert_alpha()
        self.player_coins_background = pg.transform.rotozoom(self.player_coins_background, 0, 0.4)
        self.player_coins_background_rect: pg.Rect = self.player_coins_background.get_rect(topleft=(0, 0))
        self.player_coins_rect: pg.Rect = self.player_coins_surf.get_rect(
            center=(self.player_coins_background_rect.centerx + 76, self.player_coins_background_rect.centery - 4)
        )

        self.get_updated_score_surf: Callable[..., pg.Surface] = lambda: self.bauhaus_font.render(
            "Scores: " + str(self.player.score).zfill(6), True, "#ffd723"
        )
        self.player_score_surf: pg.Surface = self.get_updated_score_surf()
        self.player_score_rect: pg.Rect = self.player_score_surf.get_rect()
        self.player_score_rect.topright = (GAME_SCREEN_WIDTH - 10, 5)

        self.extra_life_rect: pg.Rect = self.extra_life_surfs[0].get_rect(
            midleft=(self.player_coins_background_rect.right + 5, self.player_coins_background_rect.centery - 4)
        )
        self.torpedo_reload_timer = ReloadTimer(
            self.extra_life_rect.right + 15,
            self.extra_life_rect.centery,
            "assets/fonts/bauhaus93.ttf",
        )

    def reset_game(self) -> None:
        self.enemies_bullets_group.empty()
        self.enemies_group.empty()
        self.player_bullets_group.empty()
        self.torpedo_group.empty()
        self.explosion_group.empty()
        self.coins_group.empty()
        self.score_stars_group.empty()
        self.flying_hearts_group.empty()
        self.player_group.sprite.reset_position()
        self.player.reset_coins()
        self.player.reset_score()
        self.player.recover_extra_life()
        self.player_coins_surf = self.get_updated_coin_surf()
        self.player_score_surf = self.get_updated_score_surf()
        self.torpedo_reload_timer.reset_timer()

        self.set_timers()

    def update_record(self) -> None:
        current_player_score: int = self.player.score
        last_player_record: int = self.save_load_system.load_game_data({BEST_SCORE_FILE_NAME: 0})[BEST_SCORE_FILE_NAME]
        if current_player_score > last_player_record:
            self.save_load_system.save_game_data({BEST_SCORE_FILE_NAME: current_player_score})

    def startup(self) -> None:
        if self.previous != "pause":
            self.reset_game()

    def cleanup(self) -> None:
        self.update_record()

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
            if (
                self.torpedo_reload_timer.reload_time == 0
                and self.player.coins >= TORPEDO_COIN_PRICE
                and event.key == pg.K_k
            ):
                self.torpedo_group.add(Torpedo(*self.player_group.sprite.get_bullet_position()))
                self.torpedo_reload_timer.set_timer()
                self.player.add_to_coins(-TORPEDO_COIN_PRICE)

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

    def check_collisions(self) -> None:
        killed = None
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

        for torpedo in self.torpedo_group:
            if torpedo.is_ready_to_explode():
                explosion_collide_rect: pg.Rect = torpedo.get_explosion_rect()
                pg.sprite.spritecollide(
                    torpedo,
                    self.enemies_group,
                    True,
                    lambda _, enem: enem.collide_rect.colliderect(explosion_collide_rect),
                )
                torpedo.kill()
                self.explosion_group.add(Explosion(explosion_collide_rect.center, TORPEDO_EXPLOSION_SIZE_COEFFICIENT))

        if pg.sprite.groupcollide(
            self.player_group,
            self.enemies_bullets_group,
            False,
            False,
            lambda pl, bull: pl.collide_rect.colliderect(bull.collide_rect),
        ):
            self.done = True
            self.next = "game_over"

        collected_coins: list[Coin] = pg.sprite.spritecollide(
            self.player_group.sprite,
            self.coins_group,
            False,
            lambda pl, coin: pl.collide_rect.colliderect(coin.collide_rect),
        )
        for coin in collected_coins:
            coin.kill()
            self.player.add_to_coins(coin.get_value())
        if collected_coins:
            self.player_coins_surf = self.get_updated_coin_surf()

        collected_stars: list[ScoreStar] = pg.sprite.spritecollide(
            self.player_group.sprite,
            self.score_stars_group,
            False,
            lambda pl, star: pl.collide_rect.colliderect(star.collide_rect),
        )
        for star in collected_stars:
            star.kill()
            self.player.add_to_score(star.get_value())
        if collected_stars or killed is not None:
            self.player_score_surf = self.get_updated_score_surf()

    def update(self) -> None:
        """Method which updates all game with its logic"""
        self.game_background.move_background()
        self.player_group.update()
        self.enemies_group.update()
        self.torpedo_group.update()
        self.torpedo_reload_timer.update()
        self.coins_group.update()
        self.score_stars_group.update()
        self.flying_hearts_group.update()
        self.player_bullets_group.update()
        self.enemies_bullets_group.update()
        self.explosion_group.update()
        self.check_collisions()

    def draw(self, screen) -> None:
        self.game_background.draw_background(screen)
        screen.blit(self.player_coins_background, self.player_coins_background_rect)
        screen.blit(self.player_coins_surf, self.player_coins_rect)
        screen.blit(self.player_score_surf, self.player_score_rect)
        screen.blit(self.extra_life_surfs[self.player.extra_life], self.extra_life_rect)
        self.torpedo_reload_timer.draw(screen)
        self.player_bullets_group.draw(screen)
        self.enemies_bullets_group.draw(screen)
        self.torpedo_group.draw(screen)
        self.coins_group.draw(screen)
        self.score_stars_group.draw(screen)
        self.flying_hearts_group.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.explosion_group.draw(screen)

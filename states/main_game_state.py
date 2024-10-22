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
    COIN_SPAWN_EVENT_TIMER,
    ENEMY_SPAWN_EVENT_TIMER,
    EXPLOSION_SOUND_VOLUME2,
    FLYING_HEART_SPAWN_EVENT_TIMER,
    MAXIMUM_NUMBER_OF_ENEMIES_ON_THE_SCREEN,
    PLANE_EXPLOSION_SIZE_COEFFICIENT,
    PLAYER_RELOAD_TIME,
    GAME_SCREEN_WIDTH,
    BEST_SCORE_FILE_NAME,
    SCORE_ADD_EVENT_TIMER,
    STAR_SPAWN_EVENT_TIMER,
    TORPEDO_EXPLOSION_SIZE_COEFFICIENT,
    TORPEDO_COIN_PRICE,
    PLAYER_PLANE_EXPLOSION_SIZE_COEFFICIENT,
    ENEMY_SCORE_RANGE,
    COIN_SPAWN_EVENT_CHANCE_DENOMINATOR,
    STAR_SPAWN_EVENT_CHANCE_DENOMINATOR,
    ENEMY_SPAWN_EVENT_CHANCE_DENOMINATOR,
    FLYING_HEART_SPAWN_EVENT_CHANCE_DENOMINATOR,
)
from player import Player
from objects.explosion import Explosion
from objects.planes import EnemyPlane, PlayerPlane
from objects.bullets import PlayerBullet, EnemyBullet
from objects.flying_objects import Coin, ScoreStar, FlyingHeart
from objects.super_reload_clock import ReloadTimer
from objects.torpedo import Torpedo
from objects.particle import Particle
from save_load_system import GameSaveLoadSystem


class MainGameState(State):
    def __init__(self) -> None:
        super().__init__()
        self.save_load_system: GameSaveLoadSystem = GameSaveLoadSystem()

        self.game_background: GameBackground = GameBackground()  # Class to move and draw game background

        self.player = Player()
        self.player_group = (
            pg.sprite.GroupSingle()
        )  # Class to control the player (Player plane added after loading graphics)
        self.player_bullets_group = pg.sprite.Group()  # Class to control player's bullets

        self.enemies_group = pg.sprite.Group()  # Class to control enemies
        self.enemies_bullets_group = pg.sprite.Group()  # Control all enemies' bullets

        self.torpedo_group = pg.sprite.Group()  # Control all torpedos
        self.explosion_group = pg.sprite.Group()  # Control all explosions

        self.coins_group = pg.sprite.Group()  # Controll all coins
        self.score_stars_group = pg.sprite.Group()  # Controll all score stars
        self.flying_hearts_group = pg.sprite.Group()  # Controll all flying hearts
        self.particle_effect_group = pg.sprite.Group()  # Controll all particle effects

        self.set_timers()

    def load_graphics(self) -> None:
        PlayerPlane.load_graphics()
        PlayerBullet.load_graphics()
        EnemyBullet.load_graphics()
        Torpedo.load_graphics()
        ReloadTimer.load_graphics()
        Explosion.load_graphics()
        Coin.load_graphics()
        Particle.load_graphics()
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
        self.player_group.add(PlayerPlane())
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
        self.particle_effect_group.empty()
        self.flying_hearts_group.empty()
        self.player_group.sprite.reset()
        self.player.reset_coins()
        self.player.reset_score()
        self.player.recover_extra_life()
        self.player_coins_surf = self.get_updated_coin_surf()
        self.player_score_surf = self.get_updated_score_surf()
        self.torpedo_reload_timer.reset_timer()
        self.game_over_timer: int = -1
        self.last_score_value: int = self.player.score
        # if =-1 then game is still running, if 0 game's ended and if >0 then game is over but some animations are still running

        self.set_timers()

    def update_record(self) -> None:
        current_player_score: int = self.player.score
        last_player_record: int = self.save_load_system.load_game_data({BEST_SCORE_FILE_NAME: 0})[BEST_SCORE_FILE_NAME]
        if current_player_score > last_player_record:
            self.save_load_system.save_game_data({BEST_SCORE_FILE_NAME: current_player_score})

    def startup(self) -> None:
        self.audio_controller.change_music("gameplay")
        if self.previous != "pause":
            self.reset_game()

    def cleanup(self) -> None:
        self.update_record()

    def set_timers(self) -> None:
        self.enemy_spawn_event_timer: int = ENEMY_SPAWN_EVENT_TIMER
        self.coin_spawn_event_timer: int = COIN_SPAWN_EVENT_TIMER
        self.star_spawn_event_timer: int = STAR_SPAWN_EVENT_TIMER
        self.flying_heart_spawn_event_timer: int = FLYING_HEART_SPAWN_EVENT_TIMER
        self.score_add_event_timer: int = SCORE_ADD_EVENT_TIMER

    def update_timers(self) -> None:
        self.enemy_spawn_event_timer -= 1
        self.coin_spawn_event_timer -= 1
        self.star_spawn_event_timer -= 1
        self.flying_heart_spawn_event_timer -= 1
        self.score_add_event_timer -= 1

    def get_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.audio_controller.play_sound("button_change")
                self.next = "pause"
                self.done = True
            if (
                self.torpedo_reload_timer.reload_time == 0
                and self.player.coins >= TORPEDO_COIN_PRICE
                and event.key == pg.K_k
            ):
                self.audio_controller.play_sound("torpedo")
                self.torpedo_group.add(Torpedo(*self.player_group.sprite.get_bullet_position()))
                self.torpedo_reload_timer.set_timer()
                self.player.add_to_coins(-TORPEDO_COIN_PRICE)
                self.player_coins_surf = self.get_updated_coin_surf()

    def manage_own_events(self) -> None:
        if self.enemy_spawn_event_timer <= 0:
            if not randint(0, ENEMY_SPAWN_EVENT_CHANCE_DENOMINATOR - 1):
                if len(self.enemies_group) < MAXIMUM_NUMBER_OF_ENEMIES_ON_THE_SCREEN:
                    self.enemies_group.add(EnemyPlane())
            self.enemy_spawn_event_timer = ENEMY_SPAWN_EVENT_TIMER

        if self.coin_spawn_event_timer <= 0:
            if not randint(0, COIN_SPAWN_EVENT_CHANCE_DENOMINATOR - 1):
                self.coins_group.add(Coin())
            self.coin_spawn_event_timer = COIN_SPAWN_EVENT_TIMER

        if self.star_spawn_event_timer <= 0:
            if not randint(0, STAR_SPAWN_EVENT_CHANCE_DENOMINATOR - 1):
                self.score_stars_group.add(ScoreStar())
            self.star_spawn_event_timer = STAR_SPAWN_EVENT_TIMER

        if self.flying_heart_spawn_event_timer <= 0:
            if not randint(0, FLYING_HEART_SPAWN_EVENT_CHANCE_DENOMINATOR - 1):
                self.flying_hearts_group.add(FlyingHeart())
            self.flying_heart_spawn_event_timer = FLYING_HEART_SPAWN_EVENT_TIMER

        if self.score_add_event_timer <= 0:
            self.player.add_to_score(randint(2, 5))
            self.score_add_event_timer = SCORE_ADD_EVENT_TIMER

    def get_keys(self, keys: pg.key.ScancodeWrapper) -> None:
        # handle keys
        if keys[pg.K_SPACE] and self.player_group.sprite.can_shoot():
            self.audio_controller.play_sound("shot")
            self.player_group.sprite.set_reload_time(PLAYER_RELOAD_TIME)
            self.player_bullets_group.add(PlayerBullet(*self.player_group.sprite.get_bullet_position()))

        # Handle enemy shooting
        for enemy in self.enemies_group.sprites():
            if enemy.can_shoot():
                self.enemies_bullets_group.add(EnemyBullet(*enemy.get_bullet_position()))
                enemy.update_reload_time()

    def __get_sprites_collided_with_player(self, group: pg.sprite.Group, kill_sprites: bool = True) -> list:
        """Returns a list of sprites of passed group which colliding with player"""
        return pg.sprite.spritecollide(
            self.player_group.sprite,
            group,
            kill_sprites,
            lambda pl, group_object: pl.collide_rect.colliderect(group_object.collide_rect),
        )

    def __spawn_particle(self, rect_center: tuple[int, int]) -> None:
        self.audio_controller.play_sound("particle")
        self.particle_effect_group.add(Particle(rect_center))

    def check_collisions(self) -> None:
        killed_enemies: list[EnemyPlane] = []  # list which collects every killed enemy
        for player_bullet in self.player_bullets_group.sprites():
            killed_by_this_bullet: list[EnemyPlane] = pg.sprite.spritecollide(
                player_bullet,
                self.enemies_group,
                False,
                lambda bull, enem: bull.collide_rect.colliderect(enem.collide_rect),
            )  # get list of enemies which collide with bullet
            if killed_by_this_bullet:
                player_bullet.kill()
                killed_enemies.append(killed_by_this_bullet[0])

        for torpedo in self.torpedo_group:
            if torpedo.is_ready_to_explode():
                explosion_collide_rect: pg.Rect = torpedo.get_explosion_rect()
                killed_enemies.extend(
                    pg.sprite.spritecollide(
                        torpedo,
                        self.enemies_group,
                        False,
                        lambda _, enem: enem.collide_rect.colliderect(explosion_collide_rect),
                    )
                )
                torpedo.kill()
                self.audio_controller.play_sound("explosion", EXPLOSION_SOUND_VOLUME2)
                self.explosion_group.add(Explosion(explosion_collide_rect.center, TORPEDO_EXPLOSION_SIZE_COEFFICIENT))
        if len(self.torpedo_group) == 0:
            self.audio_controller.stop_sound("torpedo")
        killed_enemies = [enemy for enemy in killed_enemies if not enemy.is_immortal]
        if killed_enemies:
            self.audio_controller.play_sound("explosion")
        for killed_enemy in killed_enemies:
            killed_enemy.kill()
            self.player.add_to_score(randint(ENEMY_SCORE_RANGE[0], ENEMY_SCORE_RANGE[1]))
            self.explosion_group.add(Explosion(killed_enemy.get_rects_center(), PLANE_EXPLOSION_SIZE_COEFFICIENT))

        if not self.player_group.sprite.immortal_timer:  # if player can be damaged now
            player_damaged = False
            hit_bullets: list[EnemyBullet] = self.__get_sprites_collided_with_player(self.enemies_bullets_group)
            if hit_bullets:
                player_damaged = True
            else:  # if player still has immortal status
                collided_planes: list[EnemyPlane] = self.__get_sprites_collided_with_player(self.enemies_group)
                if collided_planes:
                    dead_enemy = collided_planes[0]
                    self.explosion_group.add(Explosion(dead_enemy.rect.center, PLANE_EXPLOSION_SIZE_COEFFICIENT))
                    player_damaged = True

            if player_damaged:
                self.audio_controller.play_sound("explosion", EXPLOSION_SOUND_VOLUME2)
                self.explosion_group.add(
                    Explosion(self.player_group.sprite.rect.center, PLAYER_PLANE_EXPLOSION_SIZE_COEFFICIENT)
                )
                if self.player.extra_life:
                    self.player_group.sprite.make_immortal()
                    self.player.extra_life = not self.player.extra_life
                else:
                    self.game_over_timer = 12  # So explosion animation can progress

        collected_coins: list[Coin] = self.__get_sprites_collided_with_player(self.coins_group)
        for coin in collected_coins:
            self.__spawn_particle(coin.rect.center)
            self.player.add_to_coins(coin.get_value())
        if collected_coins:
            self.player_coins_surf = self.get_updated_coin_surf()

        collected_stars: list[ScoreStar] = self.__get_sprites_collided_with_player(self.score_stars_group)
        for star in collected_stars:
            self.__spawn_particle(star.rect.center)
            self.player.add_to_score(star.get_value())

        if not self.player.extra_life:
            collected_hearts: list[FlyingHeart] = self.__get_sprites_collided_with_player(self.flying_hearts_group)
            if collected_hearts:
                self.__spawn_particle(collected_hearts[0].rect.center)
                if not self.player.extra_life:
                    self.player.recover_extra_life()

    def update(self) -> None:
        """Method which updates all game with its logic"""
        self.update_timers()
        self.manage_own_events()
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
        self.particle_effect_group.update()
        self.check_collisions()
        # update score surf if score was changed
        if self.player.score != self.last_score_value:
            self.last_score_value = self.player.score
            self.player_score_surf = self.get_updated_score_surf()
        self.game_over_timer -= 1 if self.game_over_timer != -1 else 0
        if self.game_over_timer == 0:
            self.done = True
            self.next = "game_over"

    def draw(self, screen) -> None:
        self.game_background.draw_background(screen)
        screen.blit(self.player_coins_background, self.player_coins_background_rect)
        screen.blit(self.player_coins_surf, self.player_coins_rect)
        screen.blit(self.player_score_surf, self.player_score_rect)
        screen.blit(self.extra_life_surfs[self.player.extra_life], self.extra_life_rect)
        self.particle_effect_group.draw(screen)
        self.torpedo_reload_timer.draw(screen)
        self.player_bullets_group.draw(screen)
        self.enemies_bullets_group.draw(screen)
        self.torpedo_group.draw(screen)
        self.coins_group.draw(screen)
        self.score_stars_group.draw(screen)
        self.flying_hearts_group.draw(screen)
        if self.game_over_timer == -1:
            self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.explosion_group.draw(screen)

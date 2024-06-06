"""Module which contain main class for the game"""

from random import randint
import pygame as pg
from constants import GAME_SCREEN_HEIGHT, GAME_SCREEN_WIDTH, FPS
from background import GameBackground
from planes import PlayerPlane, EnemyPlane


class Game:
    """Main class to start and control the game. Uses other classes to create game and manage it."""

    def __init__(self) -> None:
        pg.init()

        # Setting up games screen
        self.screen: pg.Surface = pg.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        icon: pg.Surface = pg.transform.scale(
            pg.image.load("assets/graphics/icons/main_icon.png").convert_alpha(), (64, 64)
        )
        pg.display.set_icon(icon)
        pg.display.set_caption("Fly RUSH!")

        self.game_background: GameBackground = GameBackground()  # Class to move and draw game background

        self.player_group = pg.sprite.GroupSingle(PlayerPlane())  # Class to control the player
        self.enemies_group = pg.sprite.Group()  # Class to control enemies

        self.enemy_spawn_event: int = pg.USEREVENT + 1

        self.set_timers()
        self.clock = pg.time.Clock()

    def set_timers(self) -> None:
        pg.time.set_timer(self.enemy_spawn_event, 1500)

    def handle_events(self) -> None:
        """Method to handle all events in the game"""
        events: list[pg.event.Event] = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == self.enemy_spawn_event:
                if randint(0, 3):
                    if len(self.enemies_group) < 16:
                        self.enemies_group.add(EnemyPlane())

    def update_screen(self) -> None:
        """Method which draws all objects in game etc"""
        self.game_background.draw_background(self.screen)
        self.player_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        pg.display.update()

    def execute(self) -> None:
        """Method to keep game running and update everything in game"""
        while True:
            self.handle_events()

            self.game_background.move_background()
            self.player_group.update()
            self.enemies_group.update()

            self.update_screen()
            self.clock.tick(FPS)

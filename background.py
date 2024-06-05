"""Contain GameBackground class which manage background in the game"""

import pygame as pg
from constants import GAME_SCREEN_WIDTH, BACKGROUND_SPEED


class BackgroundElement(pg.sprite.Sprite):
    def __init__(self, start_x: int, start_y: int, to_reverse: bool) -> None:
        """Element of the background (to make animation we actually need only 2)

        Args:
            start_x (int): x of left border
            start_y (int): y of top border
            to_reverse (bool): specify if we need to reverse this element by x-axis
        """
        super().__init__()
        self.image: pg.Surface = pg.transform.rotozoom(
            pg.image.load("assets/graphics/backgrounds/background.png").convert_alpha(), 0, 0.5
        )  # Make element 2 times smaller to fit the screen
        self.rect: pg.Rect = self.image.get_rect(topleft=(start_x, start_y))
        if to_reverse:
            self.image = pg.transform.flip(self.image, True, False)

    def move_to_start(self) -> None:
        self.rect.left = GAME_SCREEN_WIDTH

    def slide_to_left(self) -> None:
        self.rect.left -= BACKGROUND_SPEED

    def check_right(self) -> None:
        if self.rect.right < 0:
            self.move_to_start()


class GameBackground:
    def __init__(self) -> None:
        self.background_elements_group = pg.sprite.Group(
            BackgroundElement(0, 0, False), BackgroundElement(GAME_SCREEN_WIDTH, 0, True)
        )

    def move_background(self) -> None:
        for el in self.background_elements_group:
            el.slide_to_left()
            el.check_right()

    def draw_background(self, screen: pg.Surface) -> None:
        self.background_elements_group.draw(screen)

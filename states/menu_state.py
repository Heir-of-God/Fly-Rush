"""Module which contain state for main game"""

import sys
import os

# for importing from parent directory
scipt_dir: str = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(scipt_dir))

import pygame as pg
from .base_state import State


class MenuState(State):
    def __init__(self) -> None:
        super().__init__()

    def get_event(self, event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.next = "gameplay"

    def update(self) -> None:
        pass

    def draw(self, screen) -> None:
        screen.fill((255, 0, 0))

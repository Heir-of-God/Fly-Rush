"""Module which contains Particle class just for beautiful visual effect"""

import pygame as pg


class Particle(pg.sprite.Sprite):

    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.transform.rotozoom(pg.image.load(f"assets/graphics/particle/particle{i}.png"), 0, 0.2).convert_alpha()
            for i in range(0, 15, 1)
        ]

    def __init__(self, center: tuple[int, int]) -> None:
        super().__init__()
        self.image: pg.Surface = self.images[0]
        self.rect: pg.Rect = self.image.get_rect(center=center)
        self.current_animation_step = 0

    def animation(self) -> None:
        if self.current_animation_step < 30:
            self.image = self.images[self.current_animation_step // 2]
            self.current_animation_step += 1
            self.rect.y += 4.5
        else:
            self.kill()

    def update(self) -> None:
        self.animation()

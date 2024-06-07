"""Module which contains Explosion class for explosion animation in game"""

import pygame as pg


class Explosion(pg.sprite.Sprite):
    @classmethod
    def load_graphics(cls) -> None:
        cls.images: list[pg.Surface] = [
            pg.image.load(f"assets/graphics/explosion/explosion_0{i}.png").convert_alpha() for i in range(1, 10, 1)
        ]

    def __init__(self, center: tuple[int, int], size_coefficient: float) -> None:
        super().__init__()
        self.images = [pg.transform.scale_by(img, size_coefficient) for img in self.images]
        self.image: pg.Surface = self.images[0]
        self.rect: pg.Rect = self.image.get_rect(center=center)
        self.current_animation_step = 0

    def explosion_animation(self) -> None:
        # If animation still running
        if self.current_animation_step <= 17:
            self.image = self.images[self.current_animation_step // 2]
            self.current_animation_step += 1
        else:
            self.kill()

    def update(self) -> None:
        self.explosion_animation()

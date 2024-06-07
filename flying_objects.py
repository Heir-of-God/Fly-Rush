# """Module which contains classes for some collectable flying objects in game sich as coins, stars etc"""

# import pygame as pg


# class FlyingObject(pg.sprite.Sprite):
#     """Base class for all flying objects in game"""

#     def __init__(self) -> None:
#         super().__init__()

#     def check_right_board(self) -> None:
#         if self.rect.right <= 0:
#             self.kill()


# class Coin(FlyingObject):
#     types_to_choose: list[str] = [] # fill this list with str from constant

#     @classmethod
#     def load_graphics(cls) -> None:
#         cls.images: dict[str, list[pg.Surface]] = {}  # coin type name -> list of images for this coin
#         for t in ["bronze", "silver", "gold"]:
#             cls.images[t] = [
#                 pg.transform.rotozoom(
#                     pg.image.load(f"assets/graphics/flying_objects/coins/{t}/coin_{i}.png"), 0, 0.7
#                 ).convert_alpha()
#                 for i in range(0, 15, 1)
#             ]

#     def __init__(self) -> None:
#         super().__init__()
#         self.type = # set random type

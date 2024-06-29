"""Module which contains Player class to handle player's variables"""

from objects.planes import PlayerPlane


class Player:
    def __init__(self) -> None:
        self.extra_life: int = True
        self.score: int = 0
        self.coins: int = 0

    def recover_extra_life(self) -> None:
        self.extra_life = True

    def add_to_score(self, value) -> None:
        self.score += value
        if self.score > 999_999:
            self.score = 999_999

    def add_to_coins(self, value) -> None:
        self.coins += value
        if self.coins > 99_999:
            self.coins = 99_999

    def reset_score(self) -> None:
        self.score = 0

    def reset_coins(self) -> None:
        self.coins = 0

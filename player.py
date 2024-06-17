"""Module which contains Player class to handle player's variables"""

from objects.planes import PlayerPlane


class Player:
    def __init__(self) -> None:
        self.player_plane = PlayerPlane()
        self.score: int = 0
        self.record: int = 0
        self.coins: int = 0

    def add_to_score(self, value) -> None:
        self.score += value
        if self.score > self.record:
            self.record = self.score

    def add_to_coins(self, value) -> None:
        self.coins += value

    def reset_score(self) -> None:
        self.score = 0

    def reset_coins(self) -> None:
        self.coins = 0
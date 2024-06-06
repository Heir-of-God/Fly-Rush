"""Module which store all constants (and parameters that you can change as settings)"""

# Games FPS (clock.time())
FPS: int = 60

# Window sizes
GAME_SCREEN_WIDTH: int = 1413
GAME_SCREEN_HEIGHT: int = 768

# Game background
BACKGROUND_SPEED = 2  # px per frame

# Player
PLAYER_SPEED_Y: int = 8  # px per frame
PLAYER_SPEED_X_RIGHT: int = 10  # px per frame
PLAYER_SPEED_X_LEFT: int = 7  # px per frame

# Enemies
ENEMY_SPEED_X = 5  # px per frame
ENEMY_SPEED_Y = 1  # px per frame
ENEMY_DELTA_Y: tuple[int, int] = (90, 280)  # (minimum, maximum) delta y on which enemy's plane can deviate

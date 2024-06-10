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
PLAYER_BULLET_SPEED: int = 12  # px per frame
PLAYER_RELOAD_TIME: int = 25  # frames to reload
PLAYER_START_X: int = 706.5  # start player position on x axis
PLAYER_START_y: int = 384  # start player pisutuib on y axis

# Enemies
ENEMY_SPEED_X = 5  # px per frame
ENEMY_SPEED_Y = 1  # px per frame
ENEMY_DELTA_Y: tuple[int, int] = (90, 280)  # (minimum, maximum) delta y on which enemy's plane can deviate
ENEMY_BULLET_SPEED: int = 12  # px per frame
ENEMY_RELOAD_RANGE: tuple[int, int] = (90, 180)  # (minimum, maximum) frames until EnemyPlane can shoot again

# Explosions
PLANE_EXPLOSION_SIZE_COEFFICIENT: float = 0.35  # value which set the size of explosion animation

# Coins
# For coin there's (NUMBER OF THIS COIN) / (SUM OF ALL NUMBERS) chance that this coin will be spawned
BRONZE_COINS_NUMBER: int = 6
SILVER_COINS_NUMBER: int = 4
GOLD_COINS_NUMBER: int = 2

# How many coins player will receive when collect this type of coin
BRONZE_COIN_VALUE: int = 1
SILVER_COIN_VALUE: int = 3
GOLD_COIN_VALUE: int = 5

COINS_SPEED_Y: int = 7  # px per frame
COINS_SPEED_X: int = 4  # px_per_frame


# Score stars
SCORE_STAR_ANGLE_SPEED: int = 3  # degrees per frame
SCORE_STAR_VALUE_RANGE: tuple[int, int] = (80, 150)  # (minimum, maximum) value star will give to player
SCORE_STAR_SPEED_X: int = 10  # px per frame

# Flying hearts
FLYING_HEART_DELTA_Y: tuple[int, int] = (120, 180)  # (minimum, maximum) delta y on which flying heart can deviate
FLYING_HEART_SPEED_Y: int = 2  # px per frame
FLYING_HEART_SPEED_X: int = 4  # px per frame

"""Module which store all constants (and parameters that you can change as settings)"""

# Games FPS (clock.time())
from os import getcwd


FPS: int = 60

# Window sizes (please don't change, some positions and sizes of objects in game are hardcoded and so will break if size will be changed)
GAME_SCREEN_WIDTH: int = 1413
GAME_SCREEN_HEIGHT: int = 768

# Game sounds volume
TORPEDO_SOUND_VOLUME: float = 0.2
GAME_OVER_SOUND_VOLUME: float = 0.35
SHOT_SOUND_VOLUME: float = 0.05
BUTTON_CHANGE_SOUND_VOLUME: float = 0.2
BUTTON_CONFIRM_SOUND_VOLUME: float = 0.2
PARTICLE_SOUND_VOLUME: float = 0.4
EXPLOSION_SOUND_VOLUME1: float = 0.3  # This volume will be applied for enemies
EXPLOSION_SOUND_VOLUME2: float = 0.4  # This volume will be applied for player and torpedo

# Game timers in milliseconds how often some event will have chance to occur
ENEMY_SPAWN_EVENT_TIMER: int = 1200
COIN_SPAWN_EVENT_TIMER: int = 8000
STAR_SPAWN_EVENT_TIMER: int = 7000
FLYING_HEART_SPAWN_EVENT_TIMER: int = 15000
SCORE_ADD_EVENT_TIMER: int = 1000

# Event chances (the chance that event will ocur is 1/{value specified})
ENEMY_SPAWN_EVENT_CHANCE_DENOMINATOR: int = 2
COIN_SPAWN_EVENT_CHANCE_DENOMINATOR: int = 3
STAR_SPAWN_EVENT_CHANCE_DENOMINATOR: int = 2
FLYING_HEART_SPAWN_EVENT_CHANCE_DENOMINATOR: int = 2

# Music volume
MENU_MUSIC_VOLUME: float = 0.2
GAMEPLAY_MUSIC_VOLUME: float = 0.2

# Game background
BACKGROUND_SPEED = 2  # px per frame

# Player
PLAYER_SPEED_Y: int = 8  # px per frame
PLAYER_SPEED_X_RIGHT: int = 10  # px per frame
PLAYER_SPEED_X_LEFT: int = 7  # px per frame
PLAYER_BULLET_SPEED: int = 12  # px per frame
PLAYER_RELOAD_TIME: int = 30  # frames to reload
PLAYER_START_X: int = 706.5  # start player position on x axis
PLAYER_START_y: int = 384  # start player pisutuib on y axis
PLAYER_IMMORTAL_AFTER_HIT: int = 90  # How many frames player will be immortal after one bullet hits him
PLAYER_PLANE_EXPLOSION_SIZE_COEFFICIENT: float = 0.5  # value which set the size of explosion animation

# Enemies
MAXIMUM_NUMBER_OF_ENEMIES_ON_THE_SCREEN: int = 25
ENEMY_SPEED_X = 5  # px per frame
ENEMY_SPEED_Y = 1  # px per frame
ENEMY_DELTA_Y: tuple[int, int] = (90, 280)  # (minimum, maximum) delta y on which enemy's plane can deviate
ENEMY_BULLET_SPEED: int = 12  # px per frame
ENEMY_RELOAD_RANGE: tuple[int, int] = (90, 180)  # (minimum, maximum) frames until EnemyPlane can shoot again
ENEMY_SCORE_RANGE: tuple[int, int] = (4, 16)  # (minimum, maximum) score player will get for killing enemy

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

# Data saving
ABSOLUTE_DATA_FOLDER_PATH: str = getcwd()  # path to folder which will contain data folder
DATA_FOLDER_NAME: str = "data_folder"
DATA_FILE_EXTENSION: str = ".data"
BEST_SCORE_FILE_NAME: str = "record"

# Torpedo
TORPEDO_TIME_RELOAD: int = 1800  # This value divided by FPS is seconds for reload
TORPEDO_DELTA_X: int = (
    100  # Torpedo will explode in range [GAME_SCREEN_WIDTH * 0.85 - TORPEDO_DELTA_X, GAME_SCREEN_WIDTH * 0.85 + TORPEDO_DELTA_X]
)
TORPEDO_SPEED_X: int = 8  # px per frame
TORPEDO_SPEED_Y: int = 2.5  # px per frame
TORPEDO_DELTA_Y: float = 37.5  # px (range in which torpedo will fly from bottom to top)
TORPEDO_EXPLOSION_RECT_SIDE: int = 260  # px (in this range all enemies planes will be killed)
TORPEDO_EXPLOSION_SIZE_COEFFICIENT: float = (
    0.7  # value which set the size of explosion animation (impacts only on visual effect)
)
TORPEDO_COIN_PRICE: int = 10  # Price for player to launch torpedo


# PREPARE TIMERS TO CALCULATE AMOUNT OF FRAMES INSTEAD OF MILLISECONDS (DON'T CHANGE)
ENEMY_SPAWN_EVENT_TIMER: int = round(ENEMY_SPAWN_EVENT_TIMER / 1000) * FPS
COIN_SPAWN_EVENT_TIMER: int = round(COIN_SPAWN_EVENT_TIMER / 1000) * FPS
STAR_SPAWN_EVENT_TIMER: int = round(STAR_SPAWN_EVENT_TIMER / 1000) * FPS
FLYING_HEART_SPAWN_EVENT_TIMER: int = round(FLYING_HEART_SPAWN_EVENT_TIMER / 1000) * FPS
SCORE_ADD_EVENT_TIMER: int = round(SCORE_ADD_EVENT_TIMER / 1000) * FPS

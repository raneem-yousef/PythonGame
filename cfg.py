import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 250, 5)
RED = (255, 0, 0)

SMALL_ENEMY_COLOR = GREEN
MEDIUM_ENEMY_COLOR = (255, 255, 0)
LARGE_ENEMY_COLOR = (180, 0, 255)

SPACE_BLUE = (5, 15, 35)

AIRCRAFT_COLOR = GREEN
BULLET_COLOR = WHITE
ENEMY_COLOR = WHITE
ENEMY_BULLET_COLOR = RED
UFO_COLOR = RED
TEXT_COLOR = WHITE

FPS = 60

BGMPATH = os.path.join(os.getcwd(), 'resources/bgm.wav')
SHOOT_SOUND = os.path.join(os.getcwd(), 'resources/shoot.wav')
WIN_SOUND = os.path.join(os.getcwd(), 'resources/win.wav')
LOSE_SOUND = os.path.join(os.getcwd(), 'resources/lose.wav')
DEAD_SOUND = os.path.join(os.getcwd(), 'resources/dead.wav')

WIN_SCORE = 1000

SCREENSIZE = (800, 600)
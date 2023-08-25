from pygame.math import Vector2


FPS = 60
BG_COLOR = (0, 0, 0)
GRID_COLOR = (35, 35, 35)

ROWS = 20
COLS = 10
BLOCK_SIZE = 25
SCREEN_SIZE = COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE

INIT_POS_OFFSET = Vector2(COLS // 2 - 1, 4)

TETROMINOS = {
    'I': [(0, 0), (-1, 0), (-2, 0), (1, 0)],
    'J': [(0, 0), (-1, 0), (-1, -1), (1, 0)],
    'L': [(0, 0), (-1, 0), (1, 0), (1, -1)],
    'O': [(0, 0), (-1, 0), (-1, -1), (0, -1)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'Z': [(0, 0), (0, -1), (-1, -1), (1, 0)],
}

MOVE_DIRECTIONS = {
    'left': Vector2(-1, 0),
    'right': Vector2(1, 0),
    'down': Vector2(0, 1),
}

ANIM_TIME_INTERVAL = 150    # 毫秒数

"""
shape refer:  https://tetris.wiki/Arika_Rotation_System

"""

import sys
import typing
import random
import pygame


ROWS = 20
COLS = 10
GRID_SIZE = 25
WIDTH = COLS * GRID_SIZE + 200
HEIGHT = ROWS * GRID_SIZE

COLORS = {
    'I': (246, 125, 3),
    'T': (0, 205, 221),
    'L': (233, 146, 0),
    'J': (0, 133, 235),
    'S': (222, 28, 222),
    'Z': (85, 229, 0),
    'O': (212, 197, 0),
}


class Shape:
    TYPE = ''
    BLOCKS = []
    IMAGE = None

    def __init__(self, row, col):
        self.row_in_grids = row
        self.col_in_grids = col
        self.color = COLORS.get(self.TYPE)
        self.rotation = 0
        self.hold = False

    @property
    def block(self):
        return self.BLOCKS[self.rotation]

    def rotate(self, clockwise: bool):
        if clockwise:
            self.rotation = (self.rotation + 1) % len(self.BLOCKS)
        else:
            self.rotation = (self.rotation - 1) % len(self.BLOCKS)


class IShape(Shape):
    TYPE = 'I'
    BLOCKS = [
        [4, 5, 6, 7],
        [2, 6, 10, 14],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-I.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-I.png')


class TShape(Shape):
    TYPE = 'T'
    BLOCKS = [
        [4, 5, 6, 9],
        [1, 4, 5, 9],
        [5, 8, 9, 10],
        [1, 5, 6, 9],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-T.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-T.png')


class LShape(Shape):
    TYPE = 'L'
    BLOCKS = [
        [4, 5, 6, 8],
        [0, 1, 5, 9],
        [6, 8, 9, 10],
        [1, 5, 9, 10],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-L.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-L.png')


class JShape(Shape):
    TYPE = 'J'
    BLOCKS = [
       [4, 5, 6, 10],
       [1, 5, 8, 9],
       [4, 8, 9, 10],
       [1, 2, 5, 9],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-J.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-J.png')


class SShape(Shape):
    TYPE = 'S'
    BLOCKS = [
        [5, 6, 8, 9],
        [0, 4, 5, 9],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-S.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-S.png')


class ZShape(Shape):
    TYPE = 'Z'
    BLOCKS = [
        [4, 5, 9, 10],
        [2, 5, 6, 9],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-Z.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-Z.png')


class OShape(Shape):
    TYPE = 'O'
    BLOCKS = [
        [5, 6, 9, 10],
    ]
    IMAGE = pygame.image.load(f'./assets/images/mino-normal-O.png')
    LOCKED_IMAGE = pygame.image.load(f'./assets/images/mino-locked-O.png')


class Tetris:
    def __init__(self):
        self.block: typing.Optional[Shape] = None
        self.grids = [['' for _ in range(COLS)] for _ in range(ROWS)]
        self.state = 'running'
        self.score = 0
        self.level = 1
        self.next_blocks = []
        self.hold_block = None
        self.dead_blocks = []

    def get_locked_image(self, block_type):
        shapes = [IShape, TShape, LShape, JShape, SShape, ZShape, OShape]
        for s in shapes:
            if block_type == s.__name__[0]:
                return s.LOCKED_IMAGE

    def draw_grids(self):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * GRID_SIZE + 1, row * GRID_SIZE + 1, GRID_SIZE - 1, GRID_SIZE - 1)
                pygame.draw.rect(screen, 'black', rect, 0, 2)
                # 画底部落下来的方块
                shape_type = self.grids[row][col]
                if shape_type != '':
                    # pygame.draw.rect(screen, COLORS[shape_type], rect, 0, 2)
                    image = self.get_locked_image(shape_type)
                    screen.blit(image, rect)

    def draw_dead_blocks(self):
        # todo: clear lines effect
        pass

    def draw_block(self):
        if self.block is None:
            return
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    x = (col + self.block.col_in_grids) * GRID_SIZE + 1
                    y = (row + self.block.row_in_grids) * GRID_SIZE + 1
                    rect = pygame.Rect(x, y, GRID_SIZE - 1, GRID_SIZE - 1)
                    screen.blit(self.block.IMAGE, rect)
                    # pygame.draw.rect(screen, self.block.color, rect, 0, 2)

    def generate_shape(self):
        shapes = [IShape, TShape, LShape, JShape, SShape, ZShape, OShape]
        while len(self.next_blocks) < 4:
            shape_class = random.choice(shapes)
            shape = shape_class(-1, 3)      # 屏幕上方生成
            self.next_blocks.append(shape)
            print(1)
        self.block = self.next_blocks.pop(0)

    def go_down(self):
        if self.block is None:
            return
        self.block.row_in_grids += 1
        if self.is_intersected():
            self.block.row_in_grids -= 1
            self.freeze()

    def is_intersected(self) -> bool:
        intersection = False
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    row_in_grids = row + self.block.row_in_grids
                    col_in_grids = col + self.block.col_in_grids
                    if row_in_grids < 0:
                        continue            # 因为在屏幕上方生成，row_in_grids是负数，此时不能检测
                    if col_in_grids > COLS - 1:
                        intersection = True
                    elif col_in_grids < 0:
                        intersection = True
                    elif row_in_grids > ROWS - 1:
                        intersection = True
                    elif self.grids[row_in_grids][col_in_grids] != '':
                        intersection = True
        return intersection

    def freeze(self):
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    row_in_grids = row + self.block.row_in_grids
                    col_in_grids = col + self.block.col_in_grids
                    if row_in_grids < 0:
                        continue
                    self.grids[row_in_grids][col_in_grids] = self.block.TYPE
        self.block = None

    def wall_kick(self):
        if self.block is None:
            return
        old_row_in_grids = self.block.row_in_grids
        old_col_in_grids = self.block.col_in_grids
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    row_in_grids = row + self.block.row_in_grids
                    col_in_grids = col + self.block.col_in_grids
                    if col_in_grids < 0:
                        self.block.col_in_grids -= col_in_grids
                    elif col_in_grids > COLS - 1:
                        self.block.col_in_grids -= (col_in_grids - COLS + 1)
        if self.is_intersected():
            self.block.row_in_grids = old_row_in_grids
            self.block.col_in_grids = old_col_in_grids
            return False
        return True

    def rotate(self, clockwise: bool):
        if self.block is None:
            return
        old_rotation = self.block.rotation
        self.block.rotate(clockwise)
        res = self.wall_kick()
        if not res:
            self.block.rotation = old_rotation

    def go_side(self, dx):
        if self.block is None:
            return
        self.block.col_in_grids += dx
        if self.is_intersected():
            self.block.col_in_grids -= dx

    def go_space(self):
        if self.block is None:
            return
        while not self.is_intersected():
            self.block.row_in_grids += 1
        self.block.row_in_grids -= 1
        self.freeze()

    def clear_lines(self):
        lines = 0
        for row in range(1, ROWS):
            full = False if '' in self.grids[row] else True
            if full:
                lines += 1
                for i in range(row, 1, -1):
                    for col in range(COLS):
                        self.grids[i][col] = self.grids[i - 1][col]
                        self.dead_blocks.append(self.grids[i - 1][col])
        self.score += lines ** 2

    def update_state(self):
        # 结束判断的条件: 产生方块的中间区域首是否被占了
        if self.grids[0][4] != '' or self.grids[0][5] != '':
            self.state = 'over'
            self.block = None

    def draw_game_over(self):
        pass

    def draw_next_blocks(self):
        for index, block in enumerate(self.next_blocks):
            pos_x = 350
            pos_y = 150 * index
            for row in range(4):
                for col in range(4):
                    i = row * 4 + col
                    if i in block.block:
                        rect = pygame.Rect(pos_x + col * GRID_SIZE, pos_y + row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        pygame.draw.rect(screen, COLORS[block.TYPE], rect, 0)
                        pygame.draw.rect(screen, 'grey', rect, 1)

    def hold(self):
        if self.block.hold:
            return
        self.block.hold = True
        self.block, self.hold_block = self.hold_block, self.block
        self.hold_block.rotation = 0
        self.hold_block.col_in_grids = 3
        self.hold_block.row_in_grids = -1

    def draw_shadow(self):
        if self.block is None:
            return
        old_row = self.block.row_in_grids
        while not self.is_intersected():
            self.block.row_in_grids += 1
        shadow_row = self.block.row_in_grids - 1
        self.block.row_in_grids = old_row

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    x = (col + self.block.col_in_grids) * GRID_SIZE
                    y = (row + shadow_row) * GRID_SIZE
                    rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, self.block.color, rect, 1, 2)


pygame.init()
pygame.display.set_caption('俄罗斯方块/Tetris')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 60

GO_DOWN = pygame.USEREVENT
pygame.time.set_timer(GO_DOWN, 500)

GO_LEFT = pygame.USEREVENT + 1
GO_RIGHT = pygame.USEREVENT + 2


game = Tetris()
pygame.key.set_repeat(50)
left_repeat_counts = 0
right_repeat_counts = 0
sparkle = pygame.image.load('./assets/images/sparkle.png').convert_alpha()
count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game.state == 'running' and event.type == GO_DOWN:
            game.go_down()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                game.state = 'pause'
            if event.key == pygame.K_RETURN:
                game.state = 'running'
            if event.key == pygame.K_UP:
                game.rotate(True)
            if event.key == pygame.K_z:
                game.rotate(False)
            if event.key == pygame.K_SPACE:
                # hard drop
                game.go_space()
            if event.key == pygame.K_c:
                game.hold()
            if event.key == pygame.K_LEFT:
                left_repeat_counts = 0
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                right_repeat_counts = 0
                game.go_side(1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game.go_down()
            if event.key == pygame.K_LEFT:
                left_repeat_counts += 1
                if left_repeat_counts >= 5:
                    game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                right_repeat_counts += 1
                if right_repeat_counts >= 5:
                    game.go_side(1)

    # 游戏逻辑
    if game.state == 'running' and game.block is None:
        game.generate_shape()

    game.clear_lines()
    game.update_state()

    # 画图
    screen.fill((36, 35, 35))
    game.draw_grids()
    game.draw_dead_blocks()
    game.draw_block()
    game.draw_shadow()
    game.draw_next_blocks()
    if game.state == 'over':
        game.draw_game_over()
    pygame.display.flip()
    clock.tick(60)

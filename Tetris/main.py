"""
shape refer:  https://tetris.wiki/Arika_Rotation_System

"""

import sys
import typing
import random
import pygame


ROWS = 20
COLS = 10
GRID_SIZE = 30
WIDTH = COLS * GRID_SIZE
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

    def __init__(self, row, col):
        self.row_in_grids = row
        self.col_in_grids = col
        self.color = COLORS.get(self.TYPE)
        self.rotation = 0

    @property
    def block(self):
        return self.BLOCKS[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.BLOCKS)


class IShape(Shape):
    TYPE = 'I'
    BLOCKS = [
        [4, 5, 6, 7],
        [2, 6, 10, 14],
    ]


class TShape(Shape):
    TYPE = 'T'
    BLOCKS = [
        [4, 5, 6, 9],
        [1, 4, 5, 9],
        [5, 8, 9, 10],
        [1, 5, 6, 9],
    ]


class LShape(Shape):
    TYPE = 'L'
    BLOCKS = [
        [4, 5, 6, 8],
        [0, 1, 5, 9],
        [6, 8, 9, 10],
        [1, 5, 9, 10],
    ]


class JShape(Shape):
    TYPE = 'J'
    BLOCKS = [
       [4, 5, 6, 10],
       [1, 5, 8, 9],
       [4, 8, 9, 10],
       [1, 2, 5, 9],
    ]


class SShape(Shape):
    TYPE = 'S'
    BLOCKS = [
        [5, 6, 8, 9],
        [0, 4, 5, 9],
    ]


class ZShape(Shape):
    TYPE = 'Z'
    BLOCKS = [
        [4, 5, 9, 10],
        [2, 5, 6, 9],
    ]


class OShape(Shape):
    TYPE = 'O'
    BLOCKS = [
        [5, 6, 9, 10],
    ]


class Tetris:
    def __init__(self):
        self.block: typing.Optional[Shape] = None
        self.grids = [['' for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.state = 'running'

    def draw_grids(self):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, 'grey', rect, 1)
                # 画底部落下来的方块
                shape_type = self.grids[row][col]
                if shape_type != '':
                    rect.move_ip(1, 1)
                    rect.width -= 2
                    rect.height -= 2
                    pygame.draw.rect(screen, COLORS[shape_type], rect, 0)

    def draw_block(self):
        if self.block is None:
            return
        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index in self.block.block:
                    x = (col + self.block.col_in_grids) * GRID_SIZE + 1
                    y = (row + self.block.row_in_grids) * GRID_SIZE + 1
                    rect = pygame.Rect(x, y, GRID_SIZE - 2, GRID_SIZE - 2)
                    pygame.draw.rect(screen, self.block.color, rect)

    def generate_shape(self):
        shapes = [IShape, TShape, LShape, JShape, SShape, ZShape, OShape]
        shape = random.choice(shapes)
        self.block = shape(-3, 3)       # 屏幕上方生成

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

    def rotate(self):
        if self.block is None:
            return
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.is_intersected():
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

    def clear_rows(self):
        pass

    def update_state(self):
        # 结束判断的条件: 产生方块的中间区域首是否被占了
        if self.grids[0][4] != '' or self.grids[0][5] != '':
            self.state = 'over'
            self.block = None

    def draw_game_over(self):
        pass


pygame.init()
pygame.display.set_caption('俄罗斯方块/Tetris')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 60

GO_DOWN = pygame.USEREVENT
pygame.time.set_timer(GO_DOWN, 800)


game = Tetris()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == GO_DOWN:
            game.go_down()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()

    # 游戏逻辑
    if game.state == 'running' and game.block is None:
        game.generate_shape()
    game.clear_rows()
    game.update_state()

    # 画图
    screen.fill('white')
    game.draw_grids()
    game.draw_block()
    if game.state == 'over':
        game.draw_game_over()
    pygame.display.flip()
    clock.tick(fps)

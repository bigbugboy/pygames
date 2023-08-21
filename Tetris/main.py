"""
shape refer:  https://tetris.wiki/Arika_Rotation_System

"""

import sys

import pygame


ROWS = 20
COLS = 10
GRID_SIZE = 30
WIDTH = COLS * GRID_SIZE + 50
HEIGHT = ROWS * GRID_SIZE + 10

COLORS = {
    'I': 'cyan',
    'T': 'purple',
    'L': 'orange',
    'J': 'blue',
    'S': 'green',
    'Z': 'red',
    'O': 'yellow',
}


class Shape:
    TYPE = ''
    BLOCKS = []

    def __init__(self, row, col):
        self.row_in_grids = row
        self.col_in_grids = col
        self.color = COLORS.get(self.TYPE)
        self.rotation = 0

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
        [1, 1, 5, 9],
        [5, 8, 9, 10],
        [2, 6, 7, 10],
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
        self.block = None
        self.grids = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.state = 'running'

    def generate_block(self):
        pass

    def go_down(self):
        pass

    def can_move(self) -> bool:
        pass

    def freeze(self):
        pass

    def rotate(self):
        pass

    def go_side(self, dx):
        pass

    def go_space(self):
        pass

    def clear_rows(self):
        pass





pygame.init()
pygame.display.set_caption('俄罗斯方块/Tetris')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 60


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(fps)

import pygame

from settings import *
from tetromino import Tetromino


class Tetris:

    def __init__(self, app):
        self.app = app
        self.sprite_group = pygame.sprite.Group()
        self.grids = self.get_grids()
        self.tetromino = Tetromino(self)

    def check_full_lines(self):
        point_row = ROWS - 1
        for row in range(ROWS - 1, -1, -1):
            for col in range(COLS):
                self.grids[point_row][col] = self.grids[row][col]
                # todo:
                if self.grids[row][col]:
                    self.grids[point_row][col].pos = Vector2(col, row)

            if not all([b for b in self.grids[point_row]]):
                point_row -= 1
            else:
                for col in range(COLS):
                    self.grids[point_row][col].alive = False
                    self.grids[point_row][col] = 0

    def get_grids(self):
        return [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def put_tetromino_blocks_in_grids(self):
        for block in self.tetromino.blocks:
            row, col = int(block.pos.y), int(block.pos.x)
            self.grids[row][col] = block

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            self.put_tetromino_blocks_in_grids()
            self.tetromino = Tetromino(self)

    def control(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move('left')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move('right')
        elif pressed_key == pygame.K_UP:
            self.tetromino.rotate()

    def update(self):
        if self.app.anim_trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
        self.sprite_group.update()

    def draw_grids(self):
        # 画方块的方式
        # for row in range(ROWS):
        #     for col in range(COLS):
        #         rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        #         pygame.draw.rect(self.app.screen, GRID_COLOR, rect, 1)

        # 画线的方式
        for row in range(1, ROWS):
            pos_y = row * BLOCK_SIZE
            pygame.draw.line(self.app.screen, GRID_COLOR, (0, pos_y), (SCREEN_SIZE[0], pos_y))
        for col in range(1, COLS):
            pos_x = col * BLOCK_SIZE
            pygame.draw.line(self.app.screen, GRID_COLOR, (pos_x, 0), (pos_x, SCREEN_SIZE[1]))

    def draw(self):
        self.draw_grids()
        self.sprite_group.draw(self.app.screen)

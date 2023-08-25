import random

import pygame

from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, tetromino, pos: Vector2):
        super().__init__(tetromino.tetris.sprite_group)
        self.tetromimo = tetromino
        self.alive = True
        self.pos = pos + INIT_POS_OFFSET
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.image, 'orange', [1, 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2], border_radius=2)
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        if self.tetromimo.shape == 'O':
            return self.pos
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        if self.tetromimo.shape == 'I':
            rotated.x *= -1     # 水平方向调整，保证不会左右横跳
        return rotated + pivot_pos

    def update_rect_pos(self):
        self.rect.topleft = (self.pos * BLOCK_SIZE)

    def update(self):
        self.is_alive()
        self.update_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < COLS and y < ROWS and (y < 0 or not self.tetromimo.tetris.grids[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOS.keys()))
        self.blocks = [Block(self, Vector2(pos)) for pos in TETROMINOS[self.shape]]
        self.landing = False

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    def is_collide(self, block_positions):
        # return any(map(Block.is_collide, self.blocks, block_positions))
        return any([b.is_collide(block_positions[i]) for i, b in enumerate(self.blocks)])

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)
        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move('down')

import random
import sys

import pygame


pygame.init()

WIDTH = 880
HEIGHT = 600
MODE = 4


pygame.display.set_caption("拼图")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 10

image = pygame.image.load("elephant.jpg").convert()
image_rect = image.get_rect()


def shuffle(bs):
    random.shuffle(bs)
    for i, b in enumerate(bs):
        b.index = i
        b.init_pos()


def try_swap(first, second):
    if first.row == second.row and abs(first.col - second.col) == 1:
        # 左右相邻
        first.index, second.index = second.index, first.index
        first.init_pos()
        second.init_pos()
    elif first.col == second.col and abs(first.row - second.row) == 1:
        # 上下相邻
        first.index, second.index = second.index, first.index
        first.init_pos()
        second.init_pos()

    first.selected = False
    second.selected = False


class Block:

    BLOCK_WIDTH = WIDTH // MODE
    BLOCK_HEIGHT = HEIGHT // MODE

    def __init__(self, no):
        self.no = no    # 从1开始
        self.index = no - 1     # 索引值从0开始
        self.init_pos()
        self.surf = image.subsurface(self.rect)     # 只能实例化一次
        self.selected = False

    def init_pos(self):
        self.row, self.col = divmod(self.index, MODE)
        self.rect = pygame.rect.Rect(
            self.col * self.BLOCK_WIDTH,
            self.row * self.BLOCK_HEIGHT,
            self.BLOCK_WIDTH,
            self.BLOCK_HEIGHT
        )

    def draw(self):
        screen.blit(self.surf, self.rect)
        if self.selected:
            pygame.draw.rect(screen, "red", self.rect, 5)
        else:
            pygame.draw.rect(screen, "white", self.rect, 1)


blocks = [Block(i + 1) for i in range(MODE * MODE)]
shuffle(blocks)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for block in blocks:
                if block.rect.collidepoint(*mouse_pos):
                    block.selected = not block.selected
                    break
            selected_blocks = [b for b in blocks if b.selected]
            if len(selected_blocks) == 2:
                try_swap(*selected_blocks)

    # screen.blit(image, (0, 0))
    for block in blocks:
        block.draw()

    pygame.display.flip()
    clock.tick(fps)

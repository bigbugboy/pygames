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


class Block:

    BLOCK_WIDTH = WIDTH // MODE
    BLOCK_HEIGHT = HEIGHT // MODE

    def __init__(self, no):
        self.no = no    # 从1开始
        self.index = no - 1     # 索引值从0开始
        self.init_pos()
        self.surf = image.subsurface(self.rect)     # 只能实例化一次

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
        pygame.draw.rect(screen, "blue", self.rect, 1)


blocks = [Block(i + 1) for i in range(MODE * MODE)]
shuffle(blocks)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)

    # screen.blit(image, (0, 0))
    for block in blocks:
        block.draw()

    pygame.display.flip()
    clock.tick(fps)

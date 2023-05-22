import sys

import pygame

pygame.init()

MODE = 4
BLOCK_SIZE = 100
WIDTH = MODE * BLOCK_SIZE
HEIGHT = MODE * BLOCK_SIZE

pygame.display.set_caption("数字华容道")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 60


def draw_grid():
    # 画辅助网格线
    for i in range(MODE):
        pos_y = i * BLOCK_SIZE
        pygame.draw.line(screen, "black", (0, pos_y), (WIDTH, pos_y))
    for i in range(MODE):
        pos_x = i * BLOCK_SIZE
        pygame.draw.line(screen, "black", (pos_x, 0), (pos_x, HEIGHT))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)

    screen.fill("white")

    draw_grid()

    pygame.display.flip()
    clock.tick(fps)

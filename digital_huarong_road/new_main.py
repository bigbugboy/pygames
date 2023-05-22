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


class Block:
    def __init__(self, value):
        self.value = value
        self.index = value - 1
        self.row, self.col = divmod(self.index, MODE)
        self.surf = pygame.surface.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.surf.fill("grey")
        self.rect = self.surf.get_rect(center=(
            BLOCK_SIZE // 2 + self.col * BLOCK_SIZE,
            BLOCK_SIZE // 2 + self.row * BLOCK_SIZE
        ))

    def draw(self):
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "orange", self.rect, 1)


blocks = [Block(i + 1) for i in range(MODE * MODE)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)

    screen.fill("white")

    # draw_grid()   # 网格线不是我们想要的，我们想要每个方块有自己的边框
    for b in blocks:
        b.draw()

    pygame.display.flip()
    clock.tick(fps)

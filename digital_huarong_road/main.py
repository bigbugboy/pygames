import random
import typing

import pygame

"""
6x6的数字华容道
"""

CELL_NUMS = 6
CELL_SIZE = 100
SIZE = WIDTH, HEIGHT = CELL_NUMS * CELL_SIZE, CELL_NUMS * CELL_SIZE

pygame.init()


screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("数字华容道")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 50)


class Block:
    MODE = 6

    @classmethod
    def shuffle(cls, bs: typing.List["Block"]):
        random.shuffle(bs)
        for i, b in enumerate(bs):     # note start=1
            b.index = i
            b.init_pos()

    def __init__(self, no):
        self.no = no
        self.index = no - 1     # 从0开始的实际索引值
        self.init_pos()

    def init_pos(self):
        self.row, self.col = divmod(self.index, self.MODE)
        self.surf = pygame.surface.Surface((100, 100))
        self.surf.fill("grey")
        self.rect = self.surf.get_rect(center=(
            50 + self.col * 100,
            50 + self.row * 100
        ))
        self.sub_surf = FONT.render(str(self.no), True, "blue")
        # note 永远都在surf的中心点贴上数字，不随着surf所在位置变化
        self.surf.blit(self.sub_surf, self.sub_surf.get_rect(center=(50, 50)))

    def draw(self):
        if self.no <= 35:
            screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "orange", self.rect, 1)

    def try_move(self):
        to_down_index = self.index + 6
        blank_block = blocks[to_down_index]
        if to_down_index <= 35 and blank_block.no == 36:
            print(self.index, to_down_index)
            self.index, blank_block.index = blank_block.index, self.index
            self.init_pos()
            blank_block.init_pos()


blocks = [Block(i + 1) for i in range(36)]
Block.shuffle(blocks[:-1])      # note 为了方便移动位置，和36空白位置作比较做标识


def draw_grid():
    for row in range(5):
        pos_y = 100 * (row + 1)
        pygame.draw.line(screen, "black", (0, pos_y), (WIDTH, pos_y))
    for col in range(5):
        pos_x = 100 * (col + 1)
        pygame.draw.line(screen, "black", (pos_x, 0), (pos_x, HEIGHT))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for b in blocks:
                if b.rect.collidepoint(*mouse_pos):
                    b.try_move()

    screen.fill("white")
    # draw_grid()

    for b in blocks:
        b.draw()

    pygame.display.flip()
    clock.tick(60)



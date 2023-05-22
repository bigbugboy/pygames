import random
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
font = pygame.font.Font(None, 50)


def draw_grid():
    # 画辅助网格线
    for i in range(MODE):
        pos_y = i * BLOCK_SIZE
        pygame.draw.line(screen, "black", (0, pos_y), (WIDTH, pos_y))
    for i in range(MODE):
        pos_x = i * BLOCK_SIZE
        pygame.draw.line(screen, "black", (pos_x, 0), (pos_x, HEIGHT))


def shuffle_blocks(bs):
    random.shuffle(bs)  # 在此处 bs[:-1] 没有效果
    for i, b in enumerate(bs):
        b.index = i
        b.init_pos()
    while all([b.no == b.index + 1 for b in bs]):
        # 避免打乱的顺序，碰巧还是原来的顺序，导致游戏开始就game over.
        shuffle_blocks(bs)


class Block:
    def __init__(self, value):
        self.value = value
        self.index = value - 1
        self.init_pos()

    def init_pos(self):
        self.row, self.col = divmod(self.index, MODE)
        self.surf = pygame.surface.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.surf.fill("grey")
        self.rect = self.surf.get_rect(center=(
            BLOCK_SIZE // 2 + self.col * BLOCK_SIZE,
            BLOCK_SIZE // 2 + self.row * BLOCK_SIZE
        ))
        self.value_text = font.render(str(self.value), True, "blue")
        # note 永远都在surf的中心点贴上数字，不随着surf所在位置变化
        self.surf.blit(self.value_text, self.value_text.get_rect(center=(
            BLOCK_SIZE // 2, BLOCK_SIZE // 2
        )))

    def draw(self):
        if self.value < MODE * MODE:
            # 最后一数字空白展示
            screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "orange", self.rect, 1)

    def try_move(self):
        # 尝试向下移动
        to_down_index = self.index + MODE
        if to_down_index < MODE * MODE:
            _block = blocks[to_down_index]
            if _block.value == MODE * MODE:
                blocks[self.index], blocks[to_down_index] = blocks[to_down_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向上移动
        to_up_index = self.index - MODE
        if to_up_index >= 0:
            _block = blocks[to_up_index]
            if _block.value == MODE * MODE:
                blocks[self.index], blocks[to_up_index] = blocks[to_up_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向右移动
        to_right_index = self.index + 1
        # if self.index not in [5, 11, 17, 23, 29, 35]
        if self.index not in list(range(MODE - 1, MODE*MODE, MODE)):
            _block = blocks[to_right_index]
            if _block.value == MODE * MODE:
                blocks[self.index], blocks[to_right_index] = blocks[to_right_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向左移动
        to_left_index = self.index - 1
        # if self.index not in [0, 6, 12, 18, 24, 30]
        if self.index not in list(range(0, MODE*MODE, MODE)):
            _block = blocks[to_left_index]
            if _block.value == MODE * MODE:
                blocks[self.index], blocks[to_left_index] = blocks[to_left_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return


game_over = False
blocks = [Block(i + 1) for i in range(MODE * MODE)]

shuffle_blocks(blocks[:-1])     # 最后一个数字不动


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
        if not game_over and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for b in blocks:
                if b.rect.collidepoint(*mouse_pos):
                    b.try_move()
        if game_over and event.type == pygame.KEYUP:
            # 刷新游戏
            game_over = False
            blocks = [Block(i + 1) for i in range(MODE * MODE)]
            shuffle_blocks(blocks[:-1])

    screen.fill("white")

    # draw_grid()   # 网格线不是我们想要的，我们想要每个方块有自己的边框
    for b in blocks:
        b.draw()

    # 判断游戏是否结束
    game_over = all([b.value == b.index + 1 for b in blocks])
    if game_over:
        over_text = font.render("Success", True, "black")
        rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, "red", rect)
        screen.blit(over_text, rect)

    pygame.display.flip()
    clock.tick(fps)

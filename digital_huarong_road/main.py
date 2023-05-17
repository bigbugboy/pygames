import random
import typing

import pygame

"""
6x6的数字华容道
核心思想：
    1. 确定好游戏的模式，如4*4，6*6
    2. 根据模式确定游戏中需要多少个方块，按照顺序依次花在屏幕上，方块用Block对象表示，所有的block对象存放在blocks列表中
    3. 每个方块上面贴上数字标识，但最后一个方块贴上白色(表示空格)
    4. 初始化时，打乱方块的顺序（最后一个固定在右下角）
    5. 使用pygame.mouse.get_pos获取鼠标左键点击的坐标位置，依次遍历所以方块，确定点击了哪个方块
    6. 被点击的方块在上下左右四个方向做判断，是否有空格可以移动（空格的标示就是no==mode*mode）
    7. 如果一个方向可以移动，则交换两个方块的索引值和在blocks中的位置，并做位置初始化init_pos
    8. 判断游戏是否结束，优化方块打乱逻辑和刷新逻辑
"""

MODE = 4
CELL_SIZE = 100
SIZE = WIDTH, HEIGHT = MODE * CELL_SIZE, MODE * CELL_SIZE

pygame.init()


screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("数字华容道")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 50)

blocks = []


class Block:

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
        self.row, self.col = divmod(self.index, MODE)
        self.surf = pygame.surface.Surface((CELL_SIZE, CELL_SIZE))
        self.surf.fill("grey")
        self.rect = self.surf.get_rect(center=(
            CELL_SIZE // 2 + self.col * CELL_SIZE,
            CELL_SIZE // 2 + self.row * CELL_SIZE
        ))
        self.sub_surf = FONT.render(str(self.no), True, "blue")
        # note 永远都在surf的中心点贴上数字，不随着surf所在位置变化
        self.surf.blit(self.sub_surf, self.sub_surf.get_rect(center=(CELL_SIZE//2, CELL_SIZE//2)))

    def draw(self):
        if self.no <= MODE * MODE - 1:  # 35, 6*6-1
            screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "orange", self.rect, 1)

    def try_move(self):
        # 尝试向下移动
        to_down_index = self.index + MODE   # self.index + 6
        if to_down_index <= MODE * MODE - 1:
            _block = blocks[to_down_index]
            if _block.no == MODE * MODE:    # 36
                blocks[self.index], blocks[to_down_index] = blocks[to_down_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向上移动
        to_up_index = self.index - MODE     # self.index - 6
        if to_up_index >= 0:
            _block = blocks[to_up_index]
            if _block.no == MODE * MODE:     # 36
                blocks[self.index], blocks[to_up_index] = blocks[to_up_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向右移动
        to_right_index = self.index + 1
        # if self.index not in [5, 11, 17, 23, 29, 35] and to_right_index <= 35:
        if self.index not in list(range(MODE - 1, MODE*MODE, MODE)) and to_right_index <= MODE * MODE - 1:
            _block = blocks[to_right_index]
            if _block.no == MODE * MODE:    # 36
                blocks[self.index], blocks[to_right_index] = blocks[to_right_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return
        # 尝试向左移动
        to_left_index = self.index - 1
        # if self.index not in [0, 6, 12, 18, 24, 30] and to_left_index >= 0:
        if self.index not in list(range(0, MODE*MODE, MODE)) and to_left_index >= 0:
            _block = blocks[to_left_index]
            if _block.no == MODE * MODE:    # 36
                blocks[self.index], blocks[to_left_index] = blocks[to_left_index], blocks[self.index]
                self.index, _block.index = _block.index, self.index
                self.init_pos()
                _block.init_pos()
                return


def init_blocks():
    global blocks
    blocks = [Block(i + 1) for i in range(MODE * MODE)]  # range(36)
    Block.shuffle(blocks[:-1])  # note 为了方便移动位置，和36空白位置作比较做标识
    while all([b.no == b.index + 1 for b in blocks]):
        # 避免打乱的顺序，碰巧还是原来的顺序，导致游戏开始就game over.
        Block.shuffle(blocks[:-1])


def draw_grid():
    for row in range(MODE - 1):     # 5
        pos_y = CELL_SIZE * (row + 1)   # 100*(row+1)
        pygame.draw.line(screen, "black", (0, pos_y), (WIDTH, pos_y))
    for col in range(MODE - 1):
        pos_x = CELL_SIZE * (col + 1)
        pygame.draw.line(screen, "black", (pos_x, 0), (pos_x, HEIGHT))


game_over = False
init_blocks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not game_over and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for b in blocks:
                if b.rect.collidepoint(*mouse_pos):
                    b.try_move()
                    break   # note 需要break，因为交换两个方块，着急需要判断一个就好了
        if not game_over and event.type == pygame.KEYUP and event.key == pygame.K_r:
            # 刷新游戏
            init_blocks()

    screen.fill("white")
    # draw_grid()

    for b in blocks:
        b.draw()

    # 判断游戏是否结束
    game_over = all([b.no == b.index + 1 for b in blocks])
    if game_over:
        over_text = FONT.render("Success", True, "black")
        rect = over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(screen, "red", rect)
        screen.blit(over_text, rect)

    pygame.display.flip()
    clock.tick(60)



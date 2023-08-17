import random
import sys

import pygame as pg

MODE = 4
BLOCK_SIZE = 100
WIDTH = MODE * BLOCK_SIZE
HEIGHT = MODE * BLOCK_SIZE

BG_COLOR = (110, 50, 30)
NUM_COLOR = (70, 31, 18)
BLOCK_COLOR = (233, 190, 136)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('数字华容道')
clock = pg.time.Clock()
font = pg.font.Font(None, 50)


class Block:
    def __init__(self, no):
        self.no = no
        self.image = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(BLOCK_COLOR)
        _text = font.render(str(self.no), True, NUM_COLOR)
        _rect = _text.get_rect(center=self.image.get_rect().center)
        self.image.blit(_text, _rect)

    def get_rect(self, index):
        row, col = divmod(index, MODE)
        return pg.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)


def get_clicked_block(pos):
    for i, b in enumerate(blocks):
        if b.get_rect(i).collidepoint(*pos):
            return b


def get_blank_block():
    for b in blocks:
        if b.no == MODE * MODE:
            return b


def try_swap_block(pos):
    the_block = get_clicked_block(pos)
    blank_block = get_blank_block()
    if the_block == blank_block:
        return

    index_bb = blocks.index(blank_block)
    index_cb = blocks.index(the_block)
    gap = abs(index_cb - index_bb)
    if gap == 1 or gap == MODE:
        blocks[index_cb], blocks[index_bb] = blocks[index_bb], blocks[index_cb]


def draw_game_over():
    title_text = font.render('Congratulation', True, 'red')
    title_rect = title_text.get_rect(center=screen.get_rect().center)

    content_text = font.render('Press any key to continue', True, 'orange')
    content_rect = content_text.get_rect(center=title_rect.center)
    content_rect.bottom += 40

    screen.blit(title_text, title_rect)
    screen.blit(content_text, content_rect)


def init_game():
    global blocks, game_status
    blocks = [Block(i + 1) for i in range(MODE * MODE)]
    last_block = blocks.pop()
    random.shuffle(blocks)
    blocks.append(last_block)
    game_status = 'RUN'


blocks = []
game_status = 'RUN'

init_game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if game_status == 'RUN' and event.type == pg.MOUSEBUTTONUP and event.button == 1:
            try_swap_block(event.pos)
        if game_status == 'OVER' and event.type == pg.KEYUP:
            init_game()

    # 游戏逻辑
    if game_status == 'RUN':
        success = all([i + 1 == block.no for i, block in enumerate(blocks)])
        if success:
            game_status = 'OVER'

    # 画图
    screen.fill(BG_COLOR)
    for i, block in enumerate(blocks):
        rect = block.get_rect(i)
        screen.blit(block.image, rect)
        pg.draw.rect(screen, BG_COLOR, rect, 1)
        if block.no == MODE * MODE:
            pg.draw.rect(screen, BG_COLOR, rect, 0)

    if game_status == 'OVER':
        draw_game_over()

    pg.display.flip()
    clock.tick(60)

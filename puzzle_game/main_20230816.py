import random
import sys

import pygame as pg
import pygame.event

WIDTH = 500
HEIGHT = 375
MODE = 3
STATUS_RUN = 'RUN'
STATUS_INIT = 'INIT'
STATUS_OVER = 'OVER'

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
picture = pg.image.load('./dog.jpg').convert()
clock = pg.time.Clock()
title_font = pygame.font.Font('./avocado.ttf', 40)
content_font = pygame.font.Font('./avocado.ttf', 30)


class Block:
    def __init__(self, index):
        self.index = index
        self.image = picture.subsurface(self.get_rect(index))
        self.selected = False

    def get_rect(self, index):
        row, col = divmod(index, MODE)
        block_width = int(WIDTH / MODE)
        block_height = int(HEIGHT / MODE)
        return pg.Rect(col * block_width, row * block_height, block_width, block_height)

    def __str__(self):
        return f'index: {self.index}'


def get_selected_block():
    for b in blocks:
        if b.selected:
            return b


def get_new_block():
    for i, b in enumerate(blocks):
        if b.get_rect(i).collidepoint(*event.pos):
            return b


def try_swap_blocks(selected, new):
    if not selected:
        new.selected = True
        return
    index_selected = blocks.index(selected)
    index_new = blocks.index(new)
    gap = abs(index_selected - index_new)
    if gap == 1 or gap == MODE:
        blocks[index_selected], blocks[index_new] = blocks[index_new], blocks[index_selected]
        selected.selected = False
        new.selected = False


def draw_game_over():
    title_text = title_font.render('Congratulation', True, 'red')
    title_rect = title_text.get_rect(center=screen.get_rect().center)

    content_text = content_font.render('Press any key to continue', True, 'orange')
    content_rect = content_text.get_rect(center=title_rect.center)
    content_rect.bottom += 40

    screen.blit(title_text, title_rect)
    screen.blit(content_text, content_rect)


def draw_init():
    title_text = title_font.render('Image Puzzle', True, (220, 20, 60))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

    choose_text = content_font.render('Choose your difficulty', True, (220, 20, 60))
    choose_rect = choose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

    easy_text = content_font.render("Press 'E' - Easy (3x3)", True, "orange")
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

    medium_text = content_font.render("Press 'M' - Medium (4x4)", True, "orange")
    medium_rect = medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))

    hard_text = content_font.render("Press 'H' - Hard (5x5)", True, "orange")
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

    screen.blit(title_text, title_rect)
    screen.blit(choose_text, choose_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)


def success():
    return all([i == block.index for i, block in enumerate(blocks)])


def init_game(mode):
    global MODE, blocks, game_status

    MODE = mode
    blocks = [Block(i) for i in range(MODE * MODE)]
    random.shuffle(blocks)
    while success():
        random.shuffle(blocks)
    game_status = STATUS_RUN


blocks = []
game_status = STATUS_INIT

while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if game_status == STATUS_RUN and event.type == pg.MOUSEBUTTONUP and event.button == 1:
            selected_block = get_selected_block()
            new_block = get_new_block()
            try_swap_blocks(selected_block, new_block)
        if game_status == STATUS_OVER and event.type == pg.KEYUP:
            game_status = STATUS_INIT
        if game_status == STATUS_INIT and event.type == pg.KEYUP:
            if event.key == pg.K_e:
                init_game(3)
            elif event.key == pg.K_m:
                init_game(4)
            elif event.key == pg.K_h:
                init_game(5)

    # 游戏逻辑
    if game_status == STATUS_RUN:
        if success():
            game_status = STATUS_OVER

    # 画图
    screen.fill('black')
    if game_status == STATUS_INIT:
        draw_init()
    if game_status != STATUS_INIT:
        for i, block in enumerate(blocks):
            rect = block.get_rect(i)
            screen.blit(block.image, rect)
            board_color = 'red' if block.selected else 'grey'
            border_width = 2 if block.selected else 1
            pg.draw.rect(screen, board_color, rect, border_width)
    if game_status == STATUS_OVER:
        draw_game_over()

    pg.display.flip()
    clock.tick(60)

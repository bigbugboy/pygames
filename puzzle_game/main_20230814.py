import random
import sys

import pygame


WIDTH = 500
HEIGHT = 341
MODE = 3
STATUS_RUN = 'RUN'
STATUS_INIT = 'INIT'
STATUS_OVER = 'OVER'


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
picture = pygame.image.load('./elephant.jpg').convert()
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
        return pygame.Rect(col * block_width, row * block_height, block_width, block_height)

    def __str__(self):
        return f'index: {self.index}'


def get_selected_block():
    for block in blocks:
        if block.selected:
            return block


def get_block_by_mouse_pos(pos):
    for i, block in enumerate(blocks):
        if block.get_rect(i).collidepoint(*pos):
            return block


def try_swap(first, second):
    if first is None:
        second.selected = True
        return
    # 相邻的两个块，它们索引的差的绝对值要么是1(左右相邻)，要么是 MODE(上下相邻)
    index_first = blocks.index(first)
    index_second = blocks.index(second)
    gap = abs(index_first - index_second)
    if gap == 1 or gap == MODE:
        blocks[index_first], blocks[index_second] = blocks[index_second], blocks[index_first]
        first.selected = False
        second.selected = False


def draw_game_over():
    title_text = title_font.render("Congratulation", True, "red")
    content_text = content_font.render("Press Any Key to continue", True, "orange")
    title_rect = title_text.get_rect(center=screen.get_rect().center)
    content_rect = content_text.get_rect(center=screen.get_rect().center)
    content_rect.top = title_rect.bottom + 20

    screen.blit(title_text, title_rect)
    screen.blit(content_text, content_rect)


def draw_init():
    # game init display text
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


def init_mode(mode):
    global MODE, game_status, blocks

    MODE = mode
    blocks = [Block(i) for i in range(MODE * MODE)]
    random.shuffle(blocks)
    game_status = STATUS_RUN


blocks = []
game_status = STATUS_INIT


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_status == STATUS_RUN and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            selected_block = get_selected_block()
            new_selected_block = get_block_by_mouse_pos(event.pos)
            try_swap(selected_block, new_selected_block)

        if game_status == STATUS_OVER and event.type == pygame.KEYUP:
            game_status = STATUS_INIT

        if game_status == STATUS_INIT and event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                init_mode(3)
            elif event.key == pygame.K_m:
                init_mode(4)
            elif event.key == pygame.K_h:
                init_mode(5)

    # 游戏逻辑
    if game_status == STATUS_RUN:
        success = all([i == b.index for i, b in enumerate(blocks)])
        if success:
            game_status = STATUS_OVER

    # 画图
    screen.fill('black')
    if game_status == STATUS_INIT:
        draw_init()

    if game_status != STATUS_INIT:
        for i, b in enumerate(blocks):
            rect = b.get_rect(i)
            screen.blit(b.image, rect)
            if b.selected:
                pygame.draw.rect(screen, 'red', rect, 2)
            else:
                pygame.draw.rect(screen, 'grey', rect, 1)

    if game_status == STATUS_OVER:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)

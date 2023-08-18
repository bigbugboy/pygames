import random
import sys

import pygame


WIDTH = 500
HEIGHT = 375
MODE = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
picture = pygame.image.load('./dog.jpg').convert()
title_font = pygame.font.Font('./avocado.ttf', 40)
content_font = pygame.font.Font('./avocado.ttf', 30)


class Block:
    def __init__(self, no):
        self.no = no
        self.image = picture.subsurface(self.get_rect(no - 1))
        self.selected = False

    def get_rect(self, index):
        row, col = divmod(index, MODE)
        block_width = int(WIDTH / MODE)
        block_height = int(HEIGHT / MODE)
        return pygame.Rect(col * block_width, row * block_height, block_width, block_height)

    def __str__(self):
        return str(self.no)


def get_selected_block():
    for b in blocks:
        if b.selected:
            return b


def get_new_block(pos):
    for i, b in enumerate(blocks):
        if b.get_rect(i).collidepoint(*pos):
            return b


def try_swap_blocks(pos):
    selected_block = get_selected_block()
    new_block = get_new_block(pos)

    if selected_block is None:
        new_block.selected = True
        return
    index_selected = blocks.index(selected_block)
    index_new = blocks.index(new_block)
    gap = abs(index_selected - index_new)
    if gap == 1 or gap == MODE:
        blocks[index_selected], blocks[index_new] = blocks[index_new], blocks[index_selected]
        selected_block.selected = False


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


def init_game(mode):
    global MODE, blocks, game_status
    MODE = mode
    blocks = [Block(i + 1) for i in range(MODE * MODE)]
    random.shuffle(blocks)
    game_status = 'RUN'


blocks = []
game_status = 'INIT'


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_status == 'RUN' and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            try_swap_blocks(event.pos)
        if game_status == 'OVER' and event.type == pygame.KEYUP:
            game_status = 'INIT'
        if game_status == 'INIT' and event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                init_game(3)
            elif event.key == pygame.K_m:
                init_game(4)
            elif event.key == pygame.K_h:
                init_game(5)

    # 游戏逻辑
    if game_status == 'RUN':
        success = all([index + 1 == block.no for index, block in enumerate(blocks)])
        if success:
            game_status = 'OVER'
            print('success')

    # 画图
    if game_status != 'INIT':
        for index, block in enumerate(blocks):
            rect = block.get_rect(index)
            screen.blit(block.image, rect)
            color = 'red' if block.selected else 'white'
            width = 2 if block.selected else 1
            pygame.draw.rect(screen, color, rect, width)

    if game_status == 'OVER':
        draw_game_over()
    if game_status == 'INIT':
        draw_init()

    pygame.display.flip()
    clock.tick(20)

import random
import sys

import pygame


pygame.init()

WIDTH = 880
HEIGHT = 600
GAME_INIT = "int"
GAME_RUN = "run"
GAME_OVER = "over"


pygame.display.set_caption("拼图")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 10

image = pygame.image.load("elephant.old.jpg").convert()
image_rect = image.get_rect()
title_font = pygame.font.Font("avocado.ttf", 60)
content_font = pygame.font.Font("avocado.ttf", 40)

# game over display text
game_over_title_text = title_font.render("Congratulation", True, "red")
game_over_content_text = content_font.render("Press Any Key to continue", True, "orange")

game_over_title_rect = game_over_title_text.get_rect(center=screen.get_rect().center)
game_over_content_rect = game_over_content_text.get_rect(center=screen.get_rect().center)
game_over_content_rect.top = game_over_title_rect.bottom + 20

# game init display text
game_init_title_text = title_font.render('Puzzle Game', True, (220, 20, 60))
game_init_title_rect = game_init_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

game_init_choose_text = content_font.render('Choose your difficulty', True, (220, 20, 60))
game_init_choose_rect = game_init_choose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

game_init_easy_text = content_font.render("Press 'E' - Easy (3x3)", True, "orange")
game_init_easy_rect = game_init_easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

game_init_medium_text = content_font.render("Press 'M' - Medium (4x4)", True, "orange")
game_init_medium_rect = game_init_medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))

game_init_hard_text = content_font.render("Press 'H' - Hard (5x5)", True, "orange")
game_init_hard_rect = game_init_hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))


def shuffle(bs):
    random.shuffle(bs)
    for i, b in enumerate(bs):
        b.index = i
        b.init_pos()


def try_swap(first, second):
    if first.row == second.row and abs(first.col - second.col) == 1 or \
            first.col == second.col and abs(first.row - second.row) == 1:
        # 左右相邻 & 上下相邻
        first.index, second.index = second.index, first.index
        first.init_pos()
        second.init_pos()

    # 清楚选中状态
    first.selected = False
    second.selected = False


def draw_game_status():
    if game_status == GAME_OVER:
        screen.blit(game_over_title_text, game_over_title_rect)
        screen.blit(game_over_content_text, game_over_content_rect)
    elif game_status == GAME_INIT:
        screen.fill("black")
        screen.blit(game_init_title_text, game_init_title_rect)
        screen.blit(game_init_choose_text, game_init_choose_rect)
        screen.blit(game_init_easy_text, game_init_easy_rect)
        screen.blit(game_init_medium_text, game_init_medium_rect)
        screen.blit(game_init_hard_text, game_init_hard_rect)


class Block:

    def __init__(self, no, mode):
        self.mode = mode
        self.BLOCK_WIDTH = WIDTH // mode
        self.BLOCK_HEIGHT = HEIGHT // mode
        self.no = no    # 从1开始
        self.index = no - 1     # 索引值从0开始
        self.init_pos()
        self.surf = image.subsurface(self.rect)     # 只能实例化一次
        self.selected = False

    def init_pos(self):
        self.row, self.col = divmod(self.index, self.mode)
        self.rect = pygame.rect.Rect(
            self.col * self.BLOCK_WIDTH,
            self.row * self.BLOCK_HEIGHT,
            self.BLOCK_WIDTH,
            self.BLOCK_HEIGHT
        )

    def draw(self):
        screen.blit(self.surf, self.rect)
        if self.selected:
            pygame.draw.rect(screen, "red", self.rect, 5)
        else:
            pygame.draw.rect(screen, "white", self.rect, 1)


game_status = GAME_INIT
blocks = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
        if game_status == GAME_RUN and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for block in blocks:
                if block.rect.collidepoint(*mouse_pos):
                    block.selected = not block.selected
                    break
            selected_blocks = [b for b in blocks if b.selected]
            if len(selected_blocks) == 2:
                try_swap(*selected_blocks)
        elif game_status == GAME_OVER and event.type == pygame.KEYUP:
            game_status = GAME_INIT
        elif game_status == GAME_INIT and event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                mode = 3
                game_status = GAME_RUN
                blocks = [Block(i + 1, mode) for i in range(mode * mode)]
                shuffle(blocks)
            elif event.key == pygame.K_m:
                mode = 4
                game_status = GAME_RUN
                blocks = [Block(i + 1, mode) for i in range(mode * mode)]
                shuffle(blocks)
            elif event.key == pygame.K_h:
                mode = 6
                game_status = GAME_RUN
                blocks = [Block(i + 1, mode) for i in range(mode * mode)]
                shuffle(blocks)

    # screen.blit(image, (0, 0))
    for block in blocks:
        block.draw()

    # 判断游戏是否结束
    if game_status == GAME_RUN and blocks and all([b.no == b.index + 1 for b in blocks]):
        game_status = GAME_OVER

    draw_game_status()

    pygame.display.flip()
    clock.tick(fps)

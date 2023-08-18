import random
import sys

import pygame


WIDTH = 400
HEIGHT = 500

COLORS = {
    0: (204, 192, 179),     # 0表示格子上没有数字，此时格子的背景颜色
    2: (238, 228, 218),     # 2所在格子的背景颜色
    4: (237, 224, 200),     # ...
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'other': (0, 0, 0),                 # 大于2048的数字所在格子的背景颜色
    'light_text': (249, 246, 242),      # 表示数字值的颜色（大于等于8的数字）
    'dark_text': (119, 110, 101),       # 表示数字值的颜色（小于8的数字）
    'bg': (187, 173, 160),              # 游戏面板背景色
}


pygame.init()
pygame.display.set_caption('2048')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


# 4x4格子中默认都是0
block_values = [[0 for _ in range(4)] for _ in range(4)]


def draw_blocks():
    for i in range(4):
        for j in range(4):
            value = block_values[i][j]
            rect = pygame.Rect(16 + (16 + 80) * j, 16 + (16 + 80) * i, 80, 80)
            # 画格子和格子框
            pygame.draw.rect(screen, COLORS[value], rect, 0, 5)
            pygame.draw.rect(screen, 'black', rect, 2, 5)
            # 画数字
            if value == 0:
                continue
            font = pygame.font.Font(None, 50 - 4 * len(str(value)))
            color = COLORS['dark_text'] if value < 8 else COLORS['dark_text']
            value_text = font.render(str(value), True, color)
            value_rect = value_text.get_rect(center=rect.center)
            screen.blit(value_text, value_rect)


def gen_new_values():
    while any([0 in row for row in block_values]):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if block_values[row][col] == 0:
            value = 4 if random.randint(1, 10) == 10 else 2
            block_values[row][col] = value
            break


def take_turn():
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direction == 'UP':
        for i in range(1, 4):
            for j in range(4):
                # shift表示向上可以移动的距离
                shift = 0
                for q in range(i):
                    if block_values[q][j] == 0:
                        shift += 1
                if shift > 0:
                    block_values[i - shift][j] = block_values[i][j]
                    block_values[i][j] = 0
                if i - shift - 1 >= 0 and block_values[i - shift - 1][j] == block_values[i - shift][j]:
                    if not merged[i - shift - 1][j] and not merged[i - shift][j]:
                        block_values[i - shift - 1][j] *= 2
                        block_values[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direction == 'DOWN':
        for i in range(2, -1, -1):  # [2, 1, 0]
            for j in range(4):
                shift = 0
                for q in range(i + 1, 4):
                    if block_values[q][j] == 0:
                        shift += 1
                if shift > 0:
                    block_values[i + shift][j] = block_values[i][j]
                    block_values[i][j] = 0
                if i + shift + 1 <= 3 and block_values[i + shift + 1][j] == block_values[i + shift][j]:
                    if not merged[i + shift + 1][j] and not merged[i + shift][j]:
                        block_values[i + shift + 1][j] *= 2
                        block_values[i + shift][j] = 0
                        merged[i + shift + 1][j] = True

    elif direction == 'LEFT':
        for i in range(4):
            for j in range(1, 4):
                shift = 0
                for q in range(j):
                    if block_values[i][q] == 0:
                        shift += 1
                if shift > 0:
                    block_values[i][j - shift] = block_values[i][j]
                    block_values[i][j] = 0
                if j - shift - 1 >= 0 and block_values[i][j - shift - 1] == block_values[i][j - shift]:
                    if not merged[i][j - shift - 1] and not merged[i][j - shift]:
                        block_values[i][j - shift - 1] *= 2
                        block_values[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

    elif direction == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):
                shift = 0
                for q in range(j + 1, 4):
                    if block_values[i][q] == 0:
                        shift += 1
                if shift > 0:
                    block_values[i][j + shift] = block_values[i][j]
                    block_values[i][j] = 0
                if j + shift + 1 <= 3 and block_values[i][j + shift + 1] == block_values[i][j + shift]:
                    if not merged[i][j + shift + 1] and not merged[i][j + shift]:
                        block_values[i][j + shift + 1] *= 2
                        block_values[i][j + shift] = 0
                        merged[i][j + shift] = True


new_values = True
init_count = 0
direction = ''


while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            else:
                for b in block_values:
                    print(b)

    # 游戏逻辑
    if new_values or init_count < 2:
        gen_new_values()
        new_values = False
        init_count += 1

    if direction != '':
        take_turn()
        new_values = True
        direction = ''

    # 画图
    screen.fill('grey')
    pygame.draw.rect(screen, COLORS['bg'], [0, 0, 400, 400], 0, 10)
    draw_blocks()
    pygame.display.flip()
    clock.tick(60)

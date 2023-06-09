import sys
import random
import pygame


pygame.init()
WIDTH = 400
HEIGHT = 500
pygame.display.set_caption("2048")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 60
COLORS = {
    0: (204, 192, 179),     # 数字0表示空格上没有数字，0对应的颜色就是这个空格的背景色
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'other': (0, 0, 0),                 # 大于2048的数字所在空格的背景颜色
    'light_text': (249, 246, 242),      # 表示数字值的颜色
    'dark_text': (119, 110, 101),       # 表示数字值的颜色
    'bg': (187, 173, 160),              # 主面板背景色
}

# game variables init
board_values = [[0 for _ in range(4)] for _ in range(4)]
new_piece = True
piece_count = 0  # 方块数量
DIRECTION = ""
font = pygame.font.Font(None, 40)
game_over = False
score = 0
high_score = 0
try:
    f = open("high_score.txt", "r")
    high_score = int(f.readline())
    f.close()
except Exception:
    pass


# 画游戏主背景板
def draw_board():
    pygame.draw.rect(screen, COLORS["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


# 画游戏面板上的方块
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            value_bg_color = COLORS[value] if value <= 2048 else COLORS["other"]
            value_bg_rect = pygame.rect.Rect(j*100 + 15, i*100 + 15, 70, 70)
            pygame.draw.rect(screen, value_bg_color, value_bg_rect, 0, 5)   # 画方块
            pygame.draw.rect(screen, "black", value_bg_rect, 2, 5)  # 画方块的边框
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font(None, 50 - 4 * value_len)   # 数字越大，字体越小
                value_color = COLORS["dark_text"] if value < 8 else COLORS["light_text"]
                value_text = font.render(str(value), True, value_color)
                value_rect = value_text.get_rect(center=value_bg_rect.center)
                screen.blit(value_text, value_rect)     # 画方块上的数字


# 生成新的方块
def gen_new_piece(board):
    # 只要有位置是0就可以生成新方块，方块值在2和4之间随机，2的概率9/10, 4的概率1/10
    # 每次至多生成一个方块
    global game_over
    while any([0 in row for row in board]):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
            break
    else:
        game_over = True

    return board


# 2048的核心逻辑
# 改变方向后处理方块的移动与合并
def take_turn(direction, board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direction == "UP":
        for i in range(1, 4):
            for j in range(4):
                shift = 0
                # 从第2行开始判断向上移动的距离
                for q in range(i):
                    if board[q][j] == 0:
                        shift += 1
                if shift > 0:
                    # 将数字移动到新位置，并清空原位置上的数字
                    board[i - shift][j] = board[i][j]
                    board[i][j] = 0
                if i - shift - 1 >= 0 and board[i - shift - 1][j] == board[i - shift][j]:
                    if not merged[i - shift - 1][j] and not merged[i - shift][j]:
                        # 如果移动后位置上的数字和它上面的数字一样，并且都没有被合并过，则可以合并
                        # 上面位置的数字*2， 该位置数字清空为0， 上面的位置merge=True
                        board[i - shift - 1][j] *= 2
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                        increase_score(board[i - shift - 1][j])

    elif direction == "DOWN":
        for i in range(2, -1, -1):  # [2, 1, 0]
            for j in range(4):
                shift = 0
                for q in range(i + 1, 4):   # 向下判断
                    if board[q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[i + shift][j] = board[i][j]
                    board[i][j] = 0
                if i + shift + 1 <= 3 and board[i + shift + 1][j] == board[i + shift][j]:
                    if not merged[i + shift + 1][j] and not merged[i + shift][j]:
                        board[i + shift + 1][j] *= 2
                        board[i + shift][j] = 0
                        merged[i + shift + 1][j] = True
                        increase_score(board[i + shift + 1][j])

    elif direction == "LEFT":
        for i in range(4):
            for j in range(1, 4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if j - shift - 1 >= 0 and board[i][j - shift - 1] == board[i][j - shift]:
                    if not merged[i][j - shift - 1] and not merged[i][j - shift]:
                        board[i][j - shift - 1] *= 2
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True
                        increase_score(board[i][j - shift - 1])

    elif direction == "RIGHT":
        for i in range(4):
            for j in range(2, -1, -1):  # [2, 1, 0]
                shift = 0
                for q in range(j + 1, 4):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j + shift] = board[i][j]
                    board[i][j] = 0
                if j + shift + 1 <= 3 and board[i][j + shift + 1] == board[i][j + shift]:
                    if not merged[i][j + shift + 1] and not merged[i][j + shift]:
                        board[i][j + shift + 1] *= 2
                        board[i][j + shift] = 0
                        merged[i][j + shift + 1] = True
                        increase_score(board[i][j + shift + 1])


def increase_score(inc):
    global score
    score += inc


def draw_game_over():
    pygame.draw.rect(screen, 'black', [25, 50, 350, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


def save_high_score():
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()
            pygame.quit()
            sys.exit(-1)
        if not game_over and event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                DIRECTION = "UP"
            elif event.key == pygame.K_DOWN:
                DIRECTION = "DOWN"
            elif event.key == pygame.K_LEFT:
                DIRECTION = "LEFT"
            elif event.key == pygame.K_RIGHT:
                DIRECTION = "RIGHT"

        if game_over and event.key == pygame.K_RETURN:
            game_over = False
            new_piece = True
            score = 0
            board_values = [[0 for _ in range(4)] for _ in range(4)]
            piece_count = 0  # 方块数量
            DIRECTION = ""
            save_high_score()

    screen.fill("grey")
    draw_board()
    draw_pieces(board_values)

    if new_piece or piece_count < 2:
        gen_new_piece(board_values)
        new_piece = False
        piece_count += 1

    if game_over:
        draw_game_over()

    if DIRECTION != "":
        take_turn(DIRECTION, board_values)
        new_piece = True
        DIRECTION = ""

    if score > high_score:
        high_score = score

    pygame.display.flip()

import random
import sys

import pygame
from pygame.math import Vector2


BLOCK_SIZE = 40
X = 20
Y = 15
WIDTH = BLOCK_SIZE * X
HEIGHT = BLOCK_SIZE * Y

BG_COLOR = (175, 215, 70)
GRASS_COLOR = (167, 209, 61)
SCORE_TEXT_COLOR = (56, 74, 12)
SCORE_BOARD_COLOR = (167, 209, 61)

LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)


pygame.init()
pygame.display.set_caption('贪吃蛇')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
font = pygame.font.Font('./assets/fonts/poetsen.ttf', 20)

# 自定义事件-让蛇动起来
MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 150)


class Apple:
    def __init__(self):
        self.reset_pos()
        self.image = pygame.image.load('./assets/images/apple.png').convert_alpha()

    def reset_pos(self):
        self.x = random.randint(0, X - 1)
        self.y = random.randint(0, Y - 1)
        self.pos = Vector2(self.x, self.y)
        self.rect = pygame.Rect(self.pos.x * BLOCK_SIZE, self.pos.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        screen.blit(self.image, self.rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]   # 初始位置
        self.direction = RIGHT  # 初始蛇头向右
        self.eat = False

        self.head_up = pygame.image.load('assets/images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('assets/images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('assets/images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('assets/images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('assets/images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('assets/images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('assets/images/body_horizontal.png').convert_alpha()

        self.body_lt = pygame.image.load('assets/images/body_lt.png').convert_alpha()
        self.body_lb = pygame.image.load('assets/images/body_lb.png').convert_alpha()
        self.body_rt = pygame.image.load('assets/images/body_rt.png').convert_alpha()
        self.body_rb = pygame.image.load('assets/images/body_rb.png').convert_alpha()

        self.sound_eat = pygame.mixer.Sound('./assets/sounds/crunch.wav')

    def reset(self):
        self.body = [Vector2(7, 5), Vector2(6, 5), Vector2(5, 5)]  # 初始位置
        self.direction = RIGHT  # 初始蛇头向右

    def update_head(self):
        head_direction = self.body[0] - self.body[1]
        if head_direction == LEFT:
            self.head = self.head_left
        elif head_direction == RIGHT:
            self.head = self.head_right
        elif head_direction == UP:
            self.head = self.head_up
        elif head_direction == DOWN:
            self.head = self.head_down

    def update_tail(self):
        tail_direction = self.body[-1] - self.body[-2]
        if tail_direction == LEFT:
            self.tail = self.tail_left
        elif tail_direction == RIGHT:
            self.tail = self.tail_right
        elif tail_direction == UP:
            self.tail = self.tail_up
        elif tail_direction == DOWN:
            self.tail = self.tail_down

    def draw(self):
        self.update_head()
        self.update_tail()

        for i, b in enumerate(self.body):
            rect = pygame.Rect(b.x * BLOCK_SIZE, b.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if i == 0:
                screen.blit(self.head, rect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, rect)
            else:
                prev_block = self.body[i - 1]
                next_block = self.body[i + 1]
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, rect)
                else:
                    prev_direction = prev_block - b
                    next_direction = next_block - b
                    if prev_direction == DOWN and next_direction == LEFT or prev_direction == LEFT and next_direction == DOWN:
                        screen.blit(self.body_rt, rect)
                    elif prev_direction == LEFT and next_direction == UP or prev_direction == UP and next_direction == LEFT:
                        screen.blit(self.body_rb, rect)
                    elif prev_direction == UP and next_direction == RIGHT or prev_direction == RIGHT and next_direction == UP:
                        screen.blit(self.body_lb, rect)
                    elif prev_direction == RIGHT and next_direction == DOWN or prev_direction == DOWN and next_direction == RIGHT:
                        screen.blit(self.body_lt, rect)

    def move(self):
        if not self.eat:
            self.body.pop()
        new_head = self.body[0] + self.direction
        self.body = [new_head] + self.body
        self.eat = False


class Game:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.level = 1

    def draw_grass(self):
        for x in range(X):
            for y in range(Y):
                if (x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0):
                    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, GRASS_COLOR, rect, 0)

    def draw(self):
        self.draw_grass()
        self.apple.draw()
        self.snake.draw()
        self.draw_score()

    def handle_snake_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif keys[pygame.K_DOWN] and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif keys[pygame.K_LEFT] and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif keys[pygame.K_RIGHT] and self.snake.direction != LEFT:
            self.snake.direction = RIGHT

    def check_eat(self):
        head = self.snake.body[0]
        if head == self.apple.pos:
            self.snake.eat = True
            self.snake.sound_eat.play()
            self.apple.reset_pos()

    def check_hit_wall(self):
        head = self.snake.body[0]
        if head.x > X - 1 or head.x < 0:
            self.snake.reset()
        if head.y > Y - 1 or head.y < 0:
            self.snake.reset()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = font.render(score_text, True, SCORE_TEXT_COLOR)
        score_x = WIDTH - 60
        score_y = HEIGHT - 25
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.apple.image.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.x, apple_rect.y, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, SCORE_BOARD_COLOR, bg_rect)
        pygame.draw.rect(screen, SCORE_TEXT_COLOR, bg_rect, 2)
        screen.blit(self.apple.image, apple_rect)
        screen.blit(score_surface, score_rect)

    def upgrade_level(self):
        score = len(self.snake.body) - 3
        if score > 10 and self.level == 1:
            pygame.time.set_timer(MOVE_SNAKE, 130)
            self.level += 1
            # todo 升级音效
            # todo 画等级面板
        elif score > 50 and self.level == 2:
            pygame.time.set_timer(MOVE_SNAKE, 100)
            self.level += 1
        elif score > 100 and self.level == 3:
            pygame.time.set_timer(MOVE_SNAKE, 60)
            self.level += 1


game = Game()


while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOVE_SNAKE:
            game.snake.move()

    # 游戏逻辑
    game.handle_snake_direction()
    game.check_eat()
    game.check_hit_wall()
    game.upgrade_level()

    # 画图
    screen.fill(BG_COLOR)
    game.draw()
    pygame.display.flip()
    clock.tick(60)

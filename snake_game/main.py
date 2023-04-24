import pygame
from pygame.math import Vector2
import random


CELL_SIZE = 40
CELL_NUMS = 20
SIZE = WIDTH, HEIGHT = [CELL_NUMS * CELL_SIZE] * 2
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)


pygame.init()
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption("haha")


class Food:
    def __init__(self):
        self.reset()
        self.image = pygame.image.load("./assets/images/apple.png").convert_alpha()

    def reset(self):
        self.x = random.randint(0, CELL_NUMS - 1)
        self.y = random.randint(0, CELL_NUMS - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        self.rect = self.image.get_rect(topleft=(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE))
        screen.blit(self.image, self.rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  # Vector2(0, 0) 表示不移动，本质是蛇在不断reset
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

    def update_head(self):
        head_direction = self.body[0] - self.body[1]
        if head_direction == LEFT:
            self.head = self.head_left
        elif head_direction == RIGHT:
            self.head = self.head_right
        elif head_direction == UP:
            self.head = self.head_up
        else:
            self.head = self.head_down

    def update_tail(self):
        tail_direction = self.body[-1] - self.body[-2]
        if tail_direction == LEFT:
            self.tail = self.tail_left
        elif tail_direction == RIGHT:
            self.tail = self.tail_right
        elif tail_direction == UP:
            self.tail = self.tail_up
        else:
            self.tail = self.tail_down

    def draw(self):
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):
            rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if index == 0:
                screen.blit(self.head, rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, rect)
            else:
                prev_block = self.body[index - 1]
                next_block = self.body[index + 1]

                if prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, rect)
                elif prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, rect)
                else:
                    prev_direction = prev_block - block
                    next_direction = block - next_block
                    if prev_direction.x == -1 and next_direction.y == 1 or prev_direction.y == -1 and next_direction.x == 1:
                        screen.blit(self.body_rb, rect)
                    elif prev_direction.y == 1 and next_direction.x == 1 or prev_direction.x == -1 and next_direction.y == -1:
                        screen.blit(self.body_rt, rect)
                    elif prev_direction.y == -1 and next_direction.x == -1 or prev_direction.x == 1 and next_direction.y == 1:
                        screen.blit(self.body_lb, rect)
                    elif prev_direction.x == 1 and next_direction.y == -1 or prev_direction.y == 1 and next_direction.x == -1:
                        screen.blit(self.body_lt, rect)

    def move(self):
        if not self.eat:
            new_body = self.body[:-1]
        else:
            new_body = self.body[:]
            self.eat = False

        new_body.insert(0, self.body[0] + self.direction)
        self.body = new_body

    def handle_direction(self):
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP] and self.direction != Vector2(0, 1):
            self.direction = Vector2(0, -1)
        elif press_keys[pygame.K_DOWN] and self.direction != Vector2(0, -1):
            self.direction = Vector2(0, 1)
        elif press_keys[pygame.K_LEFT] and self.direction != Vector2(1, 0):
            self.direction = Vector2(-1, 0)
        elif press_keys[pygame.K_RIGHT] and self.direction != Vector2(-1, 0):
            self.direction = Vector2(1, 0)

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)


class Game:
    def __init__(self):
        self.food = Food()
        self.snake = Snake()

    def handle_snake_direction(self):
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP] and self.snake.direction != DOWN:
            self.snake.direction = Vector2(0, -1)
        elif press_keys[pygame.K_DOWN] and self.snake.direction != UP:
            self.snake.direction = Vector2(0, 1)
        elif press_keys[pygame.K_LEFT] and self.snake.direction != RIGHT:
            self.snake.direction = Vector2(-1, 0)
        elif press_keys[pygame.K_RIGHT] and self.snake.direction != LEFT:
            self.snake.direction = Vector2(1, 0)

    def draw_grass(self):
        # todo: feat bg
        for i in range(CELL_NUMS):
            pygame.draw.line(screen, "black", (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 1)
            pygame.draw.line(screen, "black", (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 1)

    def draw_score(self):
        # todo: score
        pass

    def check_eat(self):
        if self.food.pos == self.snake.body[0]:
            print("1")
            self.snake.eat = True
            self.food.reset()

    def check_hit_wall(self):
        # 检测是否撞墙
        if self.snake.body[0].x >= CELL_NUMS or self.snake.body[0].x < 0:
            self.snake.reset()
        if self.snake.body[0].y >= CELL_NUMS or self.snake.body[0].y < 0:
            self.snake.reset()

    def check_overlap(self):
        # 检测和自己重叠
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.snake.reset()


game = Game()

SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 150)
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == SNAKE_MOVE:
            game.snake.move()

    # 控制蛇运动的方向
    game.handle_snake_direction()
    game.check_eat()
    game.check_hit_wall()
    game.check_overlap()    # check it or not depend on yourself

    screen.fill("white")
    game.draw_glass()
    game.food.draw()
    game.snake.draw()

    pygame.display.flip()
    clock.tick(60)

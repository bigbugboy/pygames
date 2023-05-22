import sys

import pygame


pygame.init()

WIDTH = 880
HEIGHT = 600
MODE = 4


pygame.display.set_caption("拼图")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 10

image = pygame.image.load("elephant.jpg").convert()
image_rect = image.get_rect()
blocks = []
for i in range(MODE):
    for j in range(MODE):
        block_width = WIDTH // MODE
        block_height = HEIGHT // MODE
        sub_rect = pygame.rect.Rect(j * block_width, i * block_height, block_width, block_height)
        block_surf = image.subsurface(sub_rect)
        blocks.append((block_surf, sub_rect))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)

    # screen.blit(image, (0, 0))
    for block_surf, block_rect in blocks:
        screen.blit(block_surf, block_rect)
        pygame.draw.rect(screen, "blue", block_rect, 1)

    pygame.display.flip()
    clock.tick(fps)

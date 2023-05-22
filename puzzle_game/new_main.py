import sys

import pygame


pygame.init()

WIDTH = 880
HEIGHT = 600

pygame.display.set_caption("拼图")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
fps = 10

image = pygame.image.load("elephant.jpg").convert()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)

    screen.blit(image, (0, 0))
    pygame.display.flip()
    clock.tick(fps)

import sys

import pygame

from settings import *
from tetris import Tetris


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('俄罗斯方块/Tetris')
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.set_timer()

        self.tetris = Tetris(self)

    def set_timer(self):
        self.anim_trigger = False
        self.user_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)

    def check_events(self):
        self.anim_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True

    def update(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.tetris.draw()
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()

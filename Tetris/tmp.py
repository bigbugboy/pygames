import pygame
import sys

# 初始化 Pygame
pygame.init()

# 创建窗口
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('按键重复事件示例')

clock = pygame.time.Clock()

# 设置按键重复事件
pygame.key.set_repeat(200, 50)  # 延迟时间为200ms，间隔时间为50ms

while True:
    window.fill((0, 0, 0))  # 清空窗口

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print("空格键按下")

    pygame.display.update()
    clock.tick(60)  # 控制帧率为60
import pygame
from settings import LEVELS_INFO

SIZE = WIDTH, HEIGHT = 760 + 20, 506 + 94

pygame.init()
pygame.display.set_caption("美女找茬")
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FONT = pygame.font.Font("msyh.ttf", 50)

current_level = 1
spots = []      # 保存当前等级所有需要标记的区域
found_spots = []  # 保存找到的不同区域


def draw_image_by_no(image_id: int):
    image_one = pygame.image.load(f"images/image_{image_id}.jpg").convert()
    rect_left = pygame.rect.Rect(0, 0, image_one.get_width()//2, image_one.get_height())
    left_image = image_one.subsurface(rect_left)

    rect_right = pygame.rect.Rect(
        image_one.get_width()//2,
        0,
        image_one.get_width()//2,
        image_one.get_height()
    )
    right_image = image_one.subsurface(rect_right)

    screen.blit(left_image, left_image.get_rect(topleft=(0, 0)))
    screen.blit(right_image, right_image.get_rect(topleft=(image_one.get_width() // 2 + 20, 0)))


def draw_tip_text(count: int):
    tip_text = FONT.render(f"Spot {count} differences", True, "blue")
    tip_text_rect = tip_text.get_rect(center=(screen.get_width() // 2, 506 + 50))
    screen.blit(tip_text, tip_text_rect)


def init_spots_by_level(level: int):
    global spots, found_spots
    spots.clear()
    found_spots.clear()
    for key, value in LEVELS_INFO.get(level).items():
        spots.append(
            (pygame.rect.Rect(*key), pygame.rect.Rect(*value))
        )


init_spots_by_level(current_level)

while True:
    spot_counts = len(spots)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            for r1, r2 in spots:
                if r1.collidepoint(*pos) or r2.collidepoint(*pos):
                    found_spots.extend([r1, r2])
                    break

    screen.fill("white")
    draw_image_by_no(current_level)
    draw_tip_text(spot_counts)
    # 标识找到的区域
    for rect in found_spots:
        pygame.draw.rect(screen, "red", rect, 2, border_radius=2)

    # 判断是否完成该阶段的所有任务
    if len(found_spots) == spot_counts * 2:
        print("success")
        current_level += 1  # todo: 直接跳转到下一等级会太突然，需要让用户选择是否进入下一等级
        init_spots_by_level(current_level)

    pygame.display.flip()
    clock.tick(20)

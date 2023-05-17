import pygame

SIZE = WIDTH, HEIGHT = 760 + 20, 506 + 94

pygame.init()
pygame.display.set_caption("美女找茬")
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

image_one = pygame.image.load("images/image_1.jpg").convert()
rect_left = pygame.rect.Rect(0, 0, image_one.get_width()//2, image_one.get_height())
left_image = image_one.subsurface(rect_left)

rect_right = pygame.rect.Rect(
    image_one.get_width()//2,
    0,
    image_one.get_width()//2,
    image_one.get_height()
)
right_image = image_one.subsurface(rect_right)

FONT = pygame.font.Font("msyh.ttf", 50)
tip_text = FONT.render("Spot 5 differences", True, "blue")
tip_text_rect = tip_text.get_rect(center=(screen.get_width()//2, 506 + 50))

DIFFS = [

]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill("white")
    screen.blit(left_image, left_image.get_rect(topleft=(0, 0)))
    screen.blit(right_image, right_image.get_rect(topleft=(image_one.get_width()//2 + 20, 0)))

    screen.blit(tip_text, tip_text_rect)

    pygame.display.flip()
    clock.tick(20)

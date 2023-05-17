import pygame
import sys

pygame.init()
src_img = pygame.image.load("img1.png")  # takes command line argument for the image file's name
(width, height) = src_img.get_size()  # gets image size
window = pygame.display.set_mode((width, height))  # sets the window to image's size
window.blit(src_img, (0, 0))  # blits the image onto the screen
pygame.display.update()  # updates to show it on the window
choice = input('How would you like the differences to be shown?\n1.Red\n2.Green\n3.Blue\n4.Inverted color\n')


def choiceFunc(r, g, b):
    if choice == '1':
        return (255, 0, 0)
    elif choice == '2':
        return (0, 255, 0)
    else:  # if blue was chosen, or user input
        return (0, 0, 255)


flag = False

while not flag:  # loops until the x is clicked
    for e in pygame.event.get():  # waits for a pygame event
        if e.type == pygame.QUIT:  # if the 'X' button is clicked on the generated window
            flag = True  # stop the program

    divider = int(width / 2)

    for y in range(height):
        for x in range(divider):
            (r, g, b, _) = src_img.get_at((x, y))  # gets r,g,b, and ignores alpha
            (r2, g2, b2, _2) = src_img.get_at((x + divider, y))  # gets r,g,b, and ignores alpha
            if (r, g, b) != (r2, g2, b2):
                if choice == '4':
                    r2 = 255 - r2  # negative of red
                    g2 = 255 - g2  # negative of green
                    b2 = 255 - b2  # negative of blue
                    window.set_at((x + divider, y), (r2, g2,
                                                     b2))  # uses function set_at to place negative pixel over the pixel the r,g,b values were taken from
                else:
                    window.set_at((x + divider, y),
                                  choiceFunc(r2, g2, b2))  # uses function set_at to place the pixel given by choiceFunc
    pygame.display.update()  # updates the screen after the nested-loop

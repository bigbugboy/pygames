import random
import sys
import pygame


SIZE = WIDTH, HEIGHT = 880, 600

STATUS_INIT = 0
STATUS_MAIN = 1
STATUS_OVER = 2


pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("puzzle game by xl")
clock = pygame.time.Clock()


class Cell:
    def __init__(self, game, surface):
        self.game = game
        self.selected = False
        self.surface = surface
        self.order = 0
        self.index = 0
    
    @property
    def rect(self) -> pygame.rect.Rect:
        row, col = divmod(self.index, self.game.mode)
        left = col * self.game.cell_width
        top = row * self.game.cell_height
        return pygame.rect.Rect(left, top, self.game.cell_width, self.game.cell_height)


class PuzzleGame:

    MODE_EASY = 3
    MODE_MEDIUM = 4
    MODE_HARD = 5

    def __init__(self):
        self.status = STATUS_INIT
        self.font_title = pygame.font.Font('avocado.ttf', 64)
        self.font_content = pygame.font.Font('avocado.ttf', 40)
        self.init_text()
        self.bg = pygame.image.load("./elephant.jpg").convert()

        self.mode = 0
        self.cells = []
        self.cell_width = 0
        self.cell_height = 0
        self.selected_cell = None

    def init_text(self):
        self.title_text = self.font_title.render('Puzzle Game', True, (220, 20, 60))
        self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

        self.choose_text = self.font_content.render('Choose your difficulty', True, (220, 20, 60))
        self.choose_rect = self.choose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

        self.easy_text = self.font_content.render("Press 'E' - Easy (3x3)", True, "orange")
        self.easy_rect = self.easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

        self.medium_text = self.font_content.render("Press 'M' - Medium (4x4)", True, "orange")
        self.medium_rect = self.medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))

        self.hard_text = self.font_content.render("Press 'H' - Hard (5x5)", True, "orange")
        self.hard_rect = self.hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

    def draw_init_page(self):
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.choose_text, self.choose_rect)
        screen.blit(self.easy_text, self.easy_rect)
        screen.blit(self.medium_text, self.medium_rect)
        screen.blit(self.hard_text, self.hard_rect)

    def start(self, mode):
        self.mode = mode
        self.status = STATUS_MAIN
        self.cell_width = WIDTH // mode
        self.cell_height = HEIGHT // mode

        for i in range(self.mode * self.mode):
            row, col = divmod(i, self.mode)
            left = col * game.cell_width
            top = row * game.cell_height
            original_rect = pygame.rect.Rect(left, top, self.cell_width, self.cell_height)
            sub_surface = self.bg.subsurface(original_rect)
            cell = Cell(self, sub_surface)
            cell.order = i
            self.cells.append(cell)

        # 打乱顺序
        random.shuffle(self.cells)
        # 复赋值新的位置索引
        for i, cell in enumerate(self.cells):
            cell.index = i

    def get_cell_by_mouse_pos(self, pos) -> Cell: # type: ignore
        for cell in self.cells:
            if cell.rect.collidepoint(pos):
                return cell

    def check_swap(self, cell_a, cell_b):
        distance_x = abs(cell_a.rect.centerx - cell_b.rect.centerx)
        distance_y = abs(cell_a.rect.centery - cell_b.rect.centery)
        if distance_x == self.cell_width and cell_a.rect.centery == cell_b.rect.centery:
            return True
        if distance_y == self.cell_height and cell_a.rect.centerx == cell_b.rect.centerx:
            return True
        return False

    def run(self, mouse_pos):
        cell = self.get_cell_by_mouse_pos(mouse_pos)
        if not self.selected_cell:
            cell.selected = True
            self.selected_cell = cell
        else:
            current_cell = cell
            if current_cell == self.selected_cell:
                pass
            if self.check_swap(current_cell, self.selected_cell):
                # 交换位置
                current_cell.index, self.selected_cell.index = self.selected_cell.index, current_cell.index
                self.cells[current_cell.index] = current_cell
                self.cells[self.selected_cell.index] = self.selected_cell

                self.selected_cell.selected = False
                self.selected_cell = None
                self.check_success()

    def check_success(self):
        success = True
        for  cell in self.cells:
            if cell.index != cell.order:
                success = False
        if success:
            self.status = STATUS_OVER


game = PuzzleGame()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game.status == STATUS_INIT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                game.start(game.MODE_EASY)
            elif event.key == pygame.K_m:
                game.start(game.MODE_MEDIUM)
            elif event.key == pygame.K_h:
                game.start(game.MODE_HARD)
        if game.status == STATUS_MAIN and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            # 更新游戏逻辑
            game.run(mouse_pos)

    # 画图
    if game.status == STATUS_INIT:
        screen.fill("black")
        game.draw_init_page()
    elif game.status == STATUS_MAIN:
        screen.fill("black")
        for cell in game.cells:
            rect = cell.rect
            screen.blit(cell.surface, rect)
            color = "red" if cell.selected else "white"
            width = 5 if cell.selected else 1
            pygame.draw.rect(screen, color, rect, width)
    elif game.status == STATUS_OVER:
        # todo: success page
        print("success")
        game.status = STATUS_INIT

    pygame.display.flip()
    clock.tick(10)


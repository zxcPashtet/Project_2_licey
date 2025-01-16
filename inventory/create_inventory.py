import pygame
import os
import sys
import sqlite3


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' отсутствует")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_font(name):
    fullname = os.path.join('Fonts', name)
    if not os.path.isfile(fullname):
        print(f"Файл со шрифтом '{fullname}' не найден")
        sys.exit()
    font = fullname
    return font


font = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 35)
font_small = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 25)


class Inventory:
    def __init__(self, width, height):
        global tab_inventory, tab_equipment
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        tab_equipment = self.cursor.execute("""SELECT equipment FROM Data""").fetchone()[0].split(', ')
        tab_inventory = self.cursor.execute("""SELECT inventory FROM Data""").fetchone()[0].split(', ')
        tab_inventory[len(tab_inventory) - 1] = tab_inventory[len(tab_inventory) - 1][:-1]
        self.click = False
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 1110
        self.top = 590
        self.cell_size_x = 92
        self.cell_size_y = 68
        self.color = [(0, 0, 0), (0, 255, 0)]

    def set_view(self, left, top, cell_size):
        self.left, self.top, self.cell_size = left, top, cell_size

    def render(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (1080, 0, 520, 900))
        text_inventory = font.render('Инвентарь', True, (255, 255, 255))
        image_gold = pygame.transform.scale(load_image('gold.png'), (25, 25))
        result = self.cursor.execute("""SELECT money FROM Data""").fetchone()
        text_money = font_small.render(result[0], True, (255, 255, 0))
        screen.blit(text_money, (1145, 560))
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, self.color[self.board[y][x]],
                                 (self.left + x * self.cell_size_x,
                                  self.top + y * self.cell_size_y,
                                 self.cell_size_x, self.cell_size_y), 0)
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + x * self.cell_size_x,
                                  self.top + y * self.cell_size_y,
                                 self.cell_size_x, self.cell_size_y), 1)
        screen.blit(text_inventory, (1080 + 260 - text_inventory.get_width() // 2, 20))
        screen.blit(image_gold, (1110, 560))
        self.items()

    def items(self):
        for i in range(0, len(tab_inventory)):
            image = load_image(tab_inventory[i] + '.png')
            screen.blit(image, (1112 + ((i % 5) * 92), 592 + ((i // 5) * 68)))


    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 590) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 590) % 68)


    def get_click(self, event):
        global tab_inventory
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            if len(tab_inventory) >= self.cell[0] + 1 + self.cell[1] * 5 and self.cell[0] >= 0 and self.cell[1] >= 0:
                self.click = True
                self.temp = tab_inventory[(self.cell[0] + 1 * self.cell[1] + 1) - 1]
                del tab_inventory[(self.cell[0] + 1 * self.cell[1] + 1) - 1]
        if event.type == pygame.MOUSEBUTTONUP and self.click:
            self.cell = self.clicking_cell(event.pos)
            self.click = False
            if (event.pos[0] < 1100 or event.pos[0] > 1560) or (event.pos[1] > 862 or event.pos[1] < 590):
                tab_inventory.append(self.temp)

    def get_motion(self, x, y):
        if self.click:
            image = load_image(self.temp + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))


board_inv = Inventory(5, 4)
click = False
cell = int()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pass
        board_inv.get_click(event)
        if event.type == pygame.MOUSEMOTION:
            x_motion = event.pos[0]
            y_motion = event.pos[1]
    screen.fill((255, 255, 255))
    board_inv.render(screen)
    board_inv.get_motion(x_motion, y_motion)
    pygame.display.flip()
pygame.quit()
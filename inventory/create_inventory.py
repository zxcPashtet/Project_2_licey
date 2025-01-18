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
        tab_inventory = [None for i in range(5) for i in range(4)]
        result = self.cursor.execute("""SELECT inventory FROM Data""").fetchone()[0].split(', ')
        for i in range(len(result)):
            tab_inventory[i] = result[i]
        tab_inventory[len(result) - 1] = tab_inventory[len(result) - 1][:-1]
        tab_equipment = [None for i in range(5)]
        result = self.cursor.execute("""SELECT equipment FROM Data""").fetchone()[0].split(', ')
        for i in range(len(result)):
            tab_equipment[i] = result[i]
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
        text_equipment = font_small.render('Ваше снаряжение', True, (255, 255, 255))
        image_gold = pygame.transform.scale(load_image('gold.png'), (25, 25))
        result = self.cursor.execute("""SELECT money FROM Data""").fetchone()
        text_money = font_small.render(result[0], True, (255, 255, 0))
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
        screen.blit(text_money, (1145, 560))
        screen.blit(text_equipment, (1335 - text_equipment.get_width() // 2, 375))
        self.items()

    def items(self):
        for i in range(0, len(tab_inventory)):
            if tab_inventory[i] is not None:
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
            self.position = (self.cell[0] + (5 * self.cell[1] + 1)) - 1
            if tab_inventory[self.position] is not None and self.cell[0] >= 0 and self.cell[1] >= 0:
                self.click = True
                self.portable = tab_inventory[self.position]
                tab_inventory[self.position] = None
        if event.type == pygame.MOUSEBUTTONUP and self.click:
            self.cell = self.clicking_cell(event.pos)
            self.click = False
            if (event.pos[0] < 1100 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400):
                if (event.pos[0] > 1100 and event.pos[0] < 1560) and (event.pos[1] > 590 and event.pos[1] < 862):
                    if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] is None:
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    else:
                        temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                        tab_inventory[self.position] = temp
                else:
                    tab_inventory[self.position] = self.portable
            if (event.pos[0] > 1100 and event.pos[0] < 1560) and (event.pos[1] > 400 and event.pos[1] < 468):
                self.cell = board_equ.clicking_cell(event.pos)
                if tab_equipment[self.cell[0]] is None:
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_inventory[self.position] = temp



    def get_motion(self, x, y):
        if self.click and self.portable is not None:
            image = load_image(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))


class Equipment:
    def __init__(self, width, height):
        global tab_inventory, tab_equipment
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        self.click = False
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 1110
        self.top = 400
        self.cell_size_x = 92
        self.cell_size_y = 68
        self.color = [(0, 0, 0), (0, 255, 0)]

    def set_view(self, left, top, cell_size):
        self.left, self.top, self.cell_size = left, top, cell_size

    def render(self, screen):
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
        self.items()

    def items(self):
        for i in range(0, len(tab_equipment)):
            if tab_equipment[i] is not None:
                image = load_image(tab_equipment[i] + '.png')
                screen.blit(image, (1112 + ((i % 5) * 92), 402))


    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 400) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 400) % 68)


    def get_click(self, event):
        global tab_equipment
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            self.position = self.cell[0]
            if tab_equipment[self.position] is not None and self.cell[1] == 0:
                self.click = True
                self.portable = tab_equipment[self.cell[0]]
                tab_equipment[self.position] = None
        if event.type == pygame.MOUSEBUTTONUP and self.click:
            self.click = False
            self.cell = self.clicking_cell(event.pos)
            if (event.pos[0] < 1100 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400) and (event.pos[1] > 862 or event.pos[1] < 590):
                tab_equipment[self.position] = self.portable
            if (event.pos[0] > 1100 and event.pos[0] < 1560) and (event.pos[1] > 400 and event.pos[1] < 468):
                if tab_equipment[self.cell[0]] is None:
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_equipment[self.position] = temp
            if (event.pos[0] > 1100 and event.pos[0] < 1560) and (event.pos[1] > 590 and event.pos[1] < 862):
                print(1)
                self.cell = board_inv.clicking_cell(event.pos)
                if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] is None:
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                else:
                    temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    tab_equipment[self.position] = temp


    def get_motion(self, x, y):
        if self.click and self.portable is not None:
            image = load_image(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))


board_inv = Inventory(5, 4)
board_equ = Equipment(5, 1)
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
        board_equ.get_click(event)
        board_inv.get_click(event)
        if event.type == pygame.MOUSEMOTION:
            x_motion = event.pos[0]
            y_motion = event.pos[1]
    screen.fill((255, 255, 255))
    board_inv.render(screen)
    board_equ.render(screen)
    board_equ.get_motion(x_motion, y_motion)
    board_inv.get_motion(x_motion, y_motion)
    pygame.display.flip()
pygame.quit()
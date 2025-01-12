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


class Board:
    def __init__(self, width, height):
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        result = self.cursor.execute("""SELECT equipment FROM Data""").fetchone()[0].split(', ')
        self.equipment = result
        print(self.equipment)
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
        text_weapon = font_small.render('Оружие', True, (255, 255, 255))
        text_armor = font_small.render('Броня', True, (255, 255, 255))
        text_shoes = font_small.render('Обувь', True, (255, 255, 255))
        text_ring = font_small.render('Кольцо', True, (255, 255, 255))
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
        rect_weapon = pygame.draw.rect(screen, self.color[self.board[y][x]], (1080 + 20, 250, 92, 68))
        rect_armor = pygame.draw.rect(screen, self.color[self.board[y][x]], (1080 + 210, 250, 92, 68))
        rect_shoes = pygame.draw.rect(screen, self.color[self.board[y][x]], (1080 + 210, 400, 92, 68))
        rect_ring = pygame.draw.rect(screen, self.color[self.board[y][x]], (1080 + 400, 250, 92, 68))
        screen.blit(text_shoes, (1080 + 210, 470))
        screen.blit(text_armor, (1080 + 210, 320))
        screen.blit(text_weapon, (1080 + 20, 320))
        screen.blit(text_ring, (1080 + 400, 320))
        screen.blit(image_gold, (1110, 560))
        self.items()

    def items(self):
        result = self.cursor.execute("""SELECT inventory FROM Data""").fetchone()[0].split(', ')
        result[len(result) - 1] = result[len(result) - 1][:-1]
        result = ['Aghanim_Scepter_icon', 'Aghanim_Scepter_icon', 'Aghanim_Scepter_icon', 'Crystalys_icon', 'Crystalys_icon',
                  'Assault_Cuirass_icon', 'Assault_Cuirass_icon', 'Assault_Cuirass_icon', 'Platemail_icon', 'Platemail_icon']
        for i in range(0, len(result)):
            image = load_image(result[i] + '.png')
            screen.blit(image, (1112 + ((i % 5) * 92), 592 + ((i // 5) * 68)))
        if len(self.equipment) >= 1:
            image = load_image(self.equipment[0] + '.png')
            screen.blit(image, (1102, 252))


    def get_cell(self, mouse_pos):
        x = mouse_pos[0] - 1100
        y = mouse_pos[1] - 590
        return (x // 92, y // 68)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        #self.on_click(cell)



board = Board(5, 4)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((255, 255, 255))
    board.render(screen)
    pygame.display.flip()
pygame.quit()
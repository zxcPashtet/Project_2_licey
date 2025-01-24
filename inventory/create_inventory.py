import pygame
import os
import sys
import sqlite3


def load_font(name):
    fullname = os.path.join('Fonts', name)
    if not os.path.isfile(fullname):
        print(f"Файл со шрифтом '{fullname}' не найден")
        sys.exit()
    font = fullname
    return font


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)

font = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 35)
font_small = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 25)
font_smaller = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 20)

sound_buy_sell = pygame.mixer.Sound(os.path.join('sound', 'buy_1.mp3'))
sound_buy_sell.set_volume(0.1)


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


class Inventory:
    def __init__(self, width, height):
        global tab_inventory, tab_equipment, gold
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        tab_inventory = ["None" for i in range(20)]
        result = self.cursor.execute("""SELECT inventory FROM Data""").fetchone()[0].split()
        for i in range(len(result)):
            tab_inventory[i] = result[i]
        tab_equipment = ["None" for i in range(5)]
        result = self.cursor.execute("""SELECT equipment FROM Data""").fetchone()[0].split()
        for i in range(len(result)):
            tab_equipment[i] = result[i]
        gold = int(self.cursor.execute("""SELECT money FROM Data""").fetchone()[0])
        self.click = False
        self.image_showing_characteristics = None
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
        global gold
        pygame.draw.rect(screen, (50, 50, 50), (1080, 0, 520, 900))
        text_inventory = font.render('Инвентарь', True, (255, 255, 255))
        text_equipment = font_small.render('Ваше снаряжение', True, (255, 255, 255))
        image_gold = pygame.transform.scale(load_image('gold.png'), (25, 25))
        text_money = font_small.render(str(gold), True, (255, 255, 0))
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
        if self.image_showing_characteristics != 'None':
            k = -1
            screen.blit(load_image(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            dexterity = self.cursor.execute(f"""SELECT dexterity FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            armor = self.cursor.execute(f"""SELECT armor FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            health = self.cursor.execute(f"""SELECT health FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            mane = self.cursor.execute(f"""SELECT mana FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            physical_damage = self.cursor.execute(f"""SELECT physical_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            magic_damage = self.cursor.execute(f"""SELECT magic_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            speed = self.cursor.execute(f"""SELECT speed FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_selling_price = font_smaller.render('Цена при продаже ' + str(selling_price[0] // 2), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость +' + str(dexterity[0]), True, (255, 255, 255))
                screen.blit(text_dexterity, (1220, 150 + 20 * k))
            if armor[0] is not None:
                k += 1
                text_armor = font_smaller.render('Защита +' + str(armor[0]), True, (255, 255, 255))
                screen.blit(text_armor, (1220, 150 + 20 * k))
            if health[0] is not None:
                k += 1
                text_health = font_smaller.render('Здоровье +' + str(health[0]), True, (255, 255, 255))
                screen.blit(text_health, (1220, 150 + 20 * k))
            if mane[0] is not None:
                k += 1
                text_mane = font_smaller.render('Запас маны +' + str(mane[0]), True, (255, 255, 255))
                screen.blit(text_mane, (1220, 150 + 20 * k))
            if physical_damage[0] is not None:
                k += 1
                text_physical_damage = font_smaller.render('Физический урон +' + str(physical_damage[0]), True, (255, 255, 255))
                screen.blit(text_physical_damage, (1220, 150 + 20 * k))
            if magic_damage[0] is not None:
                k += 1
                text_magic_damage = font_smaller.render('Магический урон +' + str(magic_damage[0]), True, (255, 255, 255))
                screen.blit(text_magic_damage, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_selling_price, (1220, 150 + (20 * (k + 1))))


    def items(self):
        for i in range(0, len(tab_inventory)):
            if tab_inventory[i] != 'None':
                image = load_image(str(tab_inventory[i]) + '.png')
                screen.blit(image, (1112 + ((i % 5) * 92), 592 + ((i // 5) * 68)))

    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 590) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 590) % 68)


    def get_click(self, event):
        global tab_inventory, gold
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            self.position = (self.cell[0] + (5 * self.cell[1] + 1)) - 1
            if self.cell[0] >= 0 and self.cell[1] >= 0 and self.cell[0] <= 4 and self.cell[1] <= 3:
                self.click = True
                self.portable = tab_inventory[self.position]
                tab_inventory[self.position] = 'None'
                if self.portable != 'None':
                    self.image_showing_characteristics = str(self.portable) + '.png'
                    if flag_B and flag_bench:
                        gold += int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{str(self.portable) + '.png'}'""").fetchone()[0]) // 2
                        self.portable = 'None'
                        self.image_showing_characteristics = 'None'
                        self.click = False
                        sound_buy_sell.play()
        if event.type == pygame.MOUSEBUTTONUP and self.click and self.portable != 'None':
            self.cell = self.clicking_cell(event.pos)
            self.click = False
            if (event.pos[0] < 1110 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400):
                if (event.pos[0] > 1110 and event.pos[0] < 1560) and (event.pos[1] > 590 and event.pos[1] < 862):
                    if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] == 'None':
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    else:
                        temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                        tab_inventory[self.position] = temp
                else:
                    tab_inventory[self.position] = self.portable
            if (event.pos[0] > 1110 and event.pos[0] < 1560) and (event.pos[1] > 400 and event.pos[1] < 468):
                self.cell = board_equ.clicking_cell(event.pos)
                if tab_equipment[self.cell[0]] == 'None':
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_inventory[self.position] = temp



    def get_motion(self, x, y):
        if self.click and self.portable != 'None':
            image = load_image(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))

    def showing_characteristics(self, event):
        cell = self.clicking_cell(event.pos)
        if self.click is False:
            if cell[0] >= 0 and cell[1] >= 0 and cell[0] <= 4 and cell[1] <= 3:
                if tab_inventory[(cell[0] + (5 * cell[1] + 1)) - 1] != 'None':
                    self.image_showing_characteristics = str(tab_inventory[(cell[0] + (5 * cell[1] + 1)) - 1]) + '.png'
                else:
                    self.image_showing_characteristics = 'None'
            else:
                self.image_showing_characteristics = 'None'

    def completion(self):
        self.cursor.close()
        self.con.close()


class Equipment:
    def __init__(self, width, height):
        global tab_inventory, tab_equipment
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        self.click = False
        self.image_showing_characteristics = None
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
        if self.image_showing_characteristics != 'None':
            k = -1
            screen.blit(load_image(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            dexterity = self.cursor.execute(f"""SELECT dexterity FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            armor = self.cursor.execute(f"""SELECT armor FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            health = self.cursor.execute(f"""SELECT health FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            mane = self.cursor.execute(f"""SELECT mana FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            physical_damage = self.cursor.execute(f"""SELECT physical_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            magic_damage = self.cursor.execute(f"""SELECT magic_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            speed = self.cursor.execute(f"""SELECT speed FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_selling_price = font_smaller.render('Цена при продаже ' + str(selling_price[0] // 2), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость +' + str(dexterity[0]), True, (255, 255, 255))
                screen.blit(text_dexterity, (1220, 150 + 20 * k))
            if armor[0] is not None:
                k += 1
                text_armor = font_smaller.render('Защита +' + str(armor[0]), True, (255, 255, 255))
                screen.blit(text_armor, (1220, 150 + 20 * k))
            if health[0] is not None:
                k += 1
                text_health = font_smaller.render('Здоровье +' + str(health[0]), True, (255, 255, 255))
                screen.blit(text_health, (1220, 150 + 20 * k))
            if mane[0] is not None:
                k += 1
                text_mane = font_smaller.render('Запас маны +' + str(mane[0]), True, (255, 255, 255))
                screen.blit(text_mane, (1220, 150 + 20 * k))
            if physical_damage[0] is not None:
                k += 1
                text_physical_damage = font_smaller.render('Физический урон +' + str(physical_damage[0]), True, (255, 255, 255))
                screen.blit(text_physical_damage, (1220, 150 + 20 * k))
            if magic_damage[0] is not None:
                k += 1
                text_magic_damage = font_smaller.render('Магический урон +' + str(magic_damage[0]), True, (255, 255, 255))
                screen.blit(text_magic_damage, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_selling_price, (1220, 150 + (20 * (k + 1))))

    def items(self):
        for i in range(0, len(tab_equipment)):
            if tab_equipment[i] != 'None':
                image = load_image(str(tab_equipment[i]) + '.png')
                screen.blit(image, (1112 + ((i % 5) * 92), 402))

    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 400) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 400) % 68)


    def get_click(self, event):
        global tab_equipment, gold
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            self.position = self.cell[0]
            if self.cell[1] == 0 and self.cell[0] <= 4 and self.cell[0] >= 0:
                self.click = True
                self.portable = tab_equipment[self.position]
                tab_equipment[self.position] = 'None'
                if self.portable != 'None':
                    self.image_showing_characteristics = str(self.portable) + '.png'
                    if flag_B and flag_bench:
                        gold += int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{str(self.portable) + '.png'}'""").fetchone()[0]) // 2
                        self.portable = 'None'
                        self.image_showing_characteristics = 'None'
                        self.click = False
                        sound_buy_sell.play()
        if event.type == pygame.MOUSEBUTTONUP and self.click and self.portable != 'None':
            self.click = False
            self.cell = self.clicking_cell(event.pos)
            if (event.pos[0] < 1110 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400) and (event.pos[1] > 862 or event.pos[1] < 590):
                tab_equipment[self.position] = self.portable
            if (event.pos[0] > 1110 and event.pos[0] < 1560) and (event.pos[1] > 400 and event.pos[1] < 468):
                if tab_equipment[self.cell[0]] == 'None':
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_equipment[self.position] = temp
            if (event.pos[0] > 1110 and event.pos[0] < 1560) and (event.pos[1] > 590 and event.pos[1] < 862):
                self.cell = board_inv.clicking_cell(event.pos)
                if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] == 'None':
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                else:
                    temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    tab_equipment[self.position] = temp


    def get_motion(self, x, y):
        if self.click and self.portable != 'None':
            image = load_image(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))

    def showing_characteristics(self, event):
        cell = self.clicking_cell(event.pos)
        if self.click is False:
            if cell[1] == 0 and cell[0] <= 4 and cell[0] >= 0:
                if tab_equipment[cell[0]] != 'None':
                    self.image_showing_characteristics = str(tab_equipment[cell[0]]) + '.png'
                else:
                    self.image_showing_characteristics = 'None'
            else:
                self.image_showing_characteristics = 'None'

    def completion(self):
        self.cursor.close()
        self.con.close()


class Bench:
    def __init__(self, width, height):
        global tab_inventory, tab_equipment, tab_bench
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        self.image_showing_characteristics = None
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        tab_bench = ["None" for i in range(30)]
        temp = self.cursor.execute(f"""SELECT item FROM Items ORDER BY cost DESC""").fetchall()
        for i in range(len(temp)):
            tab_bench[i] = temp[i][0]
        self.left = 30
        self.top = 70
        self.cell_size_x = 92
        self.cell_size_y = 68
        self.color = [(0, 0, 0), (0, 255, 0)]

    def set_view(self, left, top, cell_size):
        self.left, self.top, self.cell_size = left, top, cell_size

    def render(self, screen):
        global gold
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 520, 900))
        text_bench = font.render('Лавка', True, (255, 255, 255))
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
        screen.blit(text_bench, (260 - text_bench.get_width() // 2, 20))
        self.items()
        if self.image_showing_characteristics != 'None':
            k = -1
            screen.blit(load_image(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            dexterity = self.cursor.execute(f"""SELECT dexterity FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            armor = self.cursor.execute(f"""SELECT armor FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            health = self.cursor.execute(f"""SELECT health FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            mane = self.cursor.execute(f"""SELECT mana FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            physical_damage = self.cursor.execute(f"""SELECT physical_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            magic_damage = self.cursor.execute(f"""SELECT magic_damage FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            speed = self.cursor.execute(f"""SELECT speed FROM Items WHERE item = '{self.image_showing_characteristics}'""").fetchone()
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_buy_price = font_smaller.render('Цена при покупке ' + str(selling_price[0]), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость +' + str(dexterity[0]), True, (255, 255, 255))
                screen.blit(text_dexterity, (1220, 150 + 20 * k))
            if armor[0] is not None:
                k += 1
                text_armor = font_smaller.render('Защита +' + str(armor[0]), True, (255, 255, 255))
                screen.blit(text_armor, (1220, 150 + 20 * k))
            if health[0] is not None:
                k += 1
                text_health = font_smaller.render('Здоровье +' + str(health[0]), True, (255, 255, 255))
                screen.blit(text_health, (1220, 150 + 20 * k))
            if mane[0] is not None:
                k += 1
                text_mane = font_smaller.render('Запас маны +' + str(mane[0]), True, (255, 255, 255))
                screen.blit(text_mane, (1220, 150 + 20 * k))
            if physical_damage[0] is not None:
                k += 1
                text_physical_damage = font_smaller.render('Физический урон +' + str(physical_damage[0]), True, (255, 255, 255))
                screen.blit(text_physical_damage, (1220, 150 + 20 * k))
            if magic_damage[0] is not None:
                k += 1
                text_magic_damage = font_smaller.render('Магический урон +' + str(magic_damage[0]), True, (255, 255, 255))
                screen.blit(text_magic_damage, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_buy_price, (1220, 150 + (20 * (k + 1))))


    def items(self):
        for i in range(0, len(tab_bench)):
            if tab_bench[i] != 'None':
                image = load_image(str(tab_bench[i]))
                screen.blit(image, (32 + ((i % 5) * 92), 72 + ((i // 5) * 68)))

    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 30) // 92
        y = (mouse_pos[1] - 70) // 68
        return (x, y, (mouse_pos[0]) % 92, (mouse_pos[1]) % 68)


    def get_click(self, event):
        global tab_bench, gold
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            self.position = (self.cell[0] + (5 * self.cell[1] + 1)) - 1
            if self.cell[0] >= 0 and self.cell[1] >= 0 and self.cell[0] <= 4 and self.cell[1] <= 5:
                self.click = True
                self.portable = tab_bench[self.position]
                if self.portable != 'None':
                    self.image_showing_characteristics = str(self.portable)
                if self.portable != 'None' and "None" in tab_inventory and gold >= int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.portable}'""").fetchone()[0]):
                    gold -= int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.portable}'""").fetchone()[0])
                    for i in range(len(tab_inventory)):
                        if tab_inventory[i] == "None":
                            sound_buy_sell.play()
                            tab_inventory[i] = self.portable[:-4]
                            break


    def showing_characteristics(self, event):
        cell = self.clicking_cell(event.pos)
        if cell[0] >= 0 and cell[1] >= 0 and cell[0] <= 4 and cell[1] <= 5:
            if tab_bench[(cell[0] + (5 * cell[1] + 1)) - 1] != 'None':
                self.image_showing_characteristics = str(tab_bench[(cell[0] + (5 * cell[1] + 1)) - 1])
            else:
                self.image_showing_characteristics = 'None'
        else:
            self.image_showing_characteristics = 'None'

    def completion(self):
        self.cursor.close()
        self.con.close()


board_inv = Inventory(5, 4)
board_equ = Equipment(5, 1)
board_ben = Bench(5, 6)
click = False
flag_B = False
flag_bench = True
cell = int()
run_invent = True
while run_invent:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_invent = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                flag_B = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_b:
                flag_B = False
        board_equ.get_click(event)
        board_inv.get_click(event)
        if flag_bench:
            board_ben.get_click(event)
        if event.type == pygame.MOUSEMOTION:
            x_motion = event.pos[0]
            y_motion = event.pos[1]
            board_inv.showing_characteristics(event)
            board_equ.showing_characteristics(event)
            if flag_bench:
                board_ben.showing_characteristics(event)
    screen.fill((255, 255, 255))
    board_inv.render(screen)
    board_equ.render(screen)
    if flag_bench:
        board_ben.render(screen)
    board_equ.get_motion(x_motion, y_motion)
    board_inv.get_motion(x_motion, y_motion)
    pygame.display.flip()
board_inv.completion()
board_equ.completion()
sqlite_connection = sqlite3.connect('forproject2.bd')
cursor = sqlite_connection.cursor()
sql_update_query = f"""Update Data set inventory = '{' '.join(tab_inventory)}',
equipment = '{' '.join(tab_equipment)}',
money = '{gold}'"""
cursor.execute(sql_update_query)
sqlite_connection.commit()
cursor.close()
pygame.quit()
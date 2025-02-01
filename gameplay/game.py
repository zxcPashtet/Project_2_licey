import pygame
import os
import sys
import random
import math
import sqlite3
import menu.main_menu


con = sqlite3.connect('forproject2.bd')
cursor = con.cursor()


def load_image(name, colorkey=None):  # Функция для загрузки картинок из data
    fullname = os.path.join('data', name)
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


def load_image_inventory(name, colorkey=None):  # Функция для загрузки картинок для инвентаря
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


def load_font(name):  # Функция загрузки шрифтов
    fullname = os.path.join('Fonts', name)
    if not os.path.isfile(fullname):
        print(f"Файл со шрифтом '{fullname}' не найден")
        sys.exit()
    font = fullname
    return font


def reading_characterestics(item):  # Функция, считывающая характеристики предмета из базы данных
    global dexterity, armor, health, mane, physical_damage, magic_damage, critical, speed
    dexterity = cursor.execute(f"""SELECT dexterity FROM Items WHERE item = '{item}'""").fetchone()
    armor = cursor.execute(f"""SELECT armor FROM Items WHERE item = '{item}'""").fetchone()
    health = cursor.execute(f"""SELECT health FROM Items WHERE item = '{item}'""").fetchone()
    mane = cursor.execute(f"""SELECT mana FROM Items WHERE item = '{item}'""").fetchone()
    physical_damage = cursor.execute(f"""SELECT physical_damage FROM Items WHERE item = '{item}'""").fetchone()
    magic_damage = cursor.execute(f"""SELECT magic_damage FROM Items WHERE item = '{item}'""").fetchone()
    critical = cursor.execute(f"""SELECT critical_damage FROM Items WHERE item = '{item}'""").fetchone()
    speed = cursor.execute(f"""SELECT speed FROM Items WHERE item = '{item}'""").fetchone()


def сhanging_characteristics_enemies():  # Функция, задающая характеристики врагов
    global MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE, SPEED_SKELETON, AWARD
    if cursor.execute("""SELECT complexity FROM Data""").fetchone()[0] == 'normal':
        MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE = 20 * (now_level ** 6) + 20, 10 * (now_level ** 5) + 15, now_level ** 5
        SPEED_SKELETON = 10 + now_level ** 2
        AWARD = 20 + (now_level * 15)
    else:
        MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE = 30 * (now_level ** 5) + 40, 10 * (now_level ** 6) + 15, now_level ** 6
        SPEED_SKELETON = 15 + now_level ** 3
        AWARD = 10 + (now_level * 10)


def clear_ini_group():  # Функция для обновления групп спрайтов при переходе на следующий уровень
    global player_sprites, mob_sprites, all_sprites, npc_sprites,\
        tiles_group, tiles_market, tiles_collide_group, tiles_collide_exit, tiles_collide_back, attacks_sprites
    player_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    npc_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    tiles_market = pygame.sprite.Group()
    tiles_collide_group = pygame.sprite.Group()
    tiles_collide_exit = pygame.sprite.Group()
    tiles_collide_back = pygame.sprite.Group()
    attacks_sprites = pygame.sprite.Group()


if menu.main_menu.flag_exit:
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    clear_ini_group()
    FPS = 24
    PLAYER_X, PLAYER_Y, PLAYER_POTIONS_HP, PLAYER_POTIONS_MANA, AWARD = 250, 250, 3, 5, 30
    now_level = int(cursor.execute("""SELECT last_level FROM Data""").fetchone()[0])
    сhanging_characteristics_enemies()
    rasa = cursor.execute("""SELECT rasa FROM Data""").fetchone()[0]

    MAX_HP_PLAYER = cursor.execute("""SELECT player_health FROM Data""").fetchone()[0]
    PLAYER_DAMAGE = cursor.execute("""SELECT player_damage FROM Data""").fetchone()[0]
    PLAYER_DEFENSE = cursor.execute("""SELECT player_protection FROM Data""").fetchone()[0]
    if rasa == 'knight':
        MAX_MANA_PLAYER = 'None'
    else:
        MAX_MANA_PLAYER = int(cursor.execute("""SELECT player_mana FROM Data""").fetchone()[0])
    if rasa == 'knight':
        KNIGHT_CRIT = int(cursor.execute("""SELECT player_critical FROM Data""").fetchone()[0])
    else:
        KNIGHT_CRIT = 'None'
    DEXTERITY = cursor.execute("""SELECT player_dexterity FROM Data""").fetchone()[0]
    SPEED_PLAYER = cursor.execute("""SELECT player_speed FROM Data""").fetchone()[0]

    tab_equipment = ["None" for i in range(5)]
    result = cursor.execute("""SELECT equipment FROM Data""").fetchone()[0].split()
    for i in range(len(result)):
        tab_equipment[i] = result[i]

    for p in tab_equipment:
        if p != 'None':
            reading_characterestics(p + '.png')
            if health[0] is not None:
                MAX_HP_PLAYER += health[0]
            if physical_damage[0] is not None:
                if rasa == 'knight':
                    PLAYER_DAMAGE += physical_damage[0]
            if magic_damage[0] is not None:
                if rasa == 'wizard':
                    PLAYER_DAMAGE += magic_damage[0]
            if armor[0] is not None:
                PLAYER_DEFENSE += armor[0]
            if mane[0] is not None:
                if rasa == 'wizard':
                    MAX_MANA_PLAYER += mane[0]
            if critical[0] is not None:
                if rasa == 'knight':
                    KNIGHT_CRIT += int(critical[0][:-1])
            if dexterity[0] is not None:
                DEXTERITY += int(dexterity[0][0])
            if speed[0] is not None:
                SPEED_PLAYER += speed[0]

    last_max_hp = MAX_HP_PLAYER

    # Загрузка музыки, звуков и тайлов
    volume_effects = float(cursor.execute("""SELECT sound_effects FROM Data""").fetchone()[0])
    sound_knight_attack = pygame.mixer.Sound('data/Knight/knight_attack.mp3')
    sound_knight_attack.set_volume(volume_effects)
    sound_knight_walk = pygame.mixer.Sound('data/Knight/knight_move.mp3')
    sound_knight_walk.set_volume(volume_effects)
    sound_charge1 = pygame.mixer.Sound('data/Mag/charge1.mp3')
    sound_charge1.set_volume(volume_effects)
    sound_charge2 = pygame.mixer.Sound('data/Mag/charge2.mp3')
    sound_charge2.set_volume(volume_effects)

    sound_warrior_attack = pygame.mixer.Sound('data/Skeleton_warrior/warrior_attack.mp3')
    sound_warrior_attack.set_volume(volume_effects)
    sound_skeleton_walk = pygame.mixer.Sound('data/Skeleton_warrior/warrior_walk.mp3')
    sound_skeleton_walk.set_volume(volume_effects)
    sound_skeleton_death = pygame.mixer.Sound('data/Skeleton_warrior/warrior_death.mp3')
    sound_skeleton_death.set_volume(volume_effects)
    sound_archero_attack = pygame.mixer.Sound('data/Skeleton_archero/archero_attack.mp3')
    sound_archero_attack.set_volume(volume_effects)
    sound_boss_attack1 = pygame.mixer.Sound('data/Boss/attack1.mp3')
    sound_boss_attack1.set_volume(volume_effects)
    sound_boss_attack2 = pygame.mixer.Sound('data/Boss/attack2.mp3')
    sound_boss_attack2.set_volume(volume_effects)

    playlist = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four'}
    current_song = 1

    music = pygame.mixer.music.load(f'music/{playlist[now_level]}.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(float(cursor.execute("""SELECT sound_music_game FROM Data""").fetchone()[0]))

    tile_images = {
        'wall': pygame.transform.scale(load_image('levels/cave_wall.png'), (150, 150)),
        'empty': pygame.transform.scale(load_image('levels/cave_pol.png'), (150, 150)),
        'exit': pygame.transform.scale(load_image('levels/cave.png'), (150, 150)),
        'back': pygame.transform.scale(load_image('levels/ladder.png'), (50, 150))
    }
    tile_width = tile_height = 150

    font_bigger = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 60)
    font_big = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 45)
    font = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 35)
    font_small = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 25)
    font_smaller = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 20)

    sound_buy_sell = pygame.mixer.Sound(os.path.join('sound', 'buy_1.mp3'))
    sound_buy_sell.set_volume(0.1)

    gold = 0


def load_level(filename):  # Загружает уровень и дополняет до максимальной длины
    with open('data/levels/' + filename, 'r') as levelfile:
        level_map = [line.strip() for line in levelfile.readlines()]
    max_len = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_len, '.'), level_map))


class Tile(pygame.sprite.Sprite):  # Класс для отрисовки земли
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_collide(pygame.sprite.Sprite):  # Класс для отрисовки стен
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_collide_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_exit(pygame.sprite.Sprite):  # Класс для отрисовки перехода на следующий уровень
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_collide_exit, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_back(pygame.sprite.Sprite):  # Класс для отрисовки лестницы, которая возвращает на предыдущий уровень
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_collide_back, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_market(pygame.sprite.Sprite):  # Класс для отрисовки кузнеца, который показывает зону лавки
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_market, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):  # Функция отрисовки уровня тайлами
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile_collide('wall', x, y)
            elif level[y][x] == '?':
                Tile_market('empty', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Tile_exit('exit', x, y)
            elif level[y][x] == '-':
                Tile('empty', x, y)
                Tile_back('back', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                if player_class == 0:
                    new_player = Knight(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_POTIONS_HP,
                                        KNIGHT_CRIT, DEXTERITY)
                else:
                    new_player = Mag(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_POTIONS_HP,
                                     PLAYER_POTIONS_MANA, MAX_MANA_PLAYER, DEXTERITY)
            elif level[y][x] == "$":
                Tile('empty', x, y)
                Warrior(x, y, MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Archero(x, y, MAX_HP_MOB // 2, MOB_DAMAGE, MOB_DEFENSE)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                Boss(x, y, MAX_HP_MOB * 3, MOB_DAMAGE * 4, MOB_DEFENSE * 2)
            elif level[y][x] == '+':
                Tile('empty', x, y)
                Blacksmith(x, y)
    return new_player, x, y


class Knight(pygame.sprite.Sprite):  # Класс рыцаря
    def __init__(self, x, y, max_hp, damage, defense, potions_hp, crit, dexterity):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/walk/walk{i}.png"),
                                                           (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/attack/attack{i}.png"),
                                                           (200, 130)) for i in range(1, 6)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/idle/idle{i}.png"),
                                                           (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/death/Dead{i}.png"),
                                                           (200, 130)) for i in range(1, 7)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag = False, False, False# Флаги для поворота, движения, смерти
        self.flag_attack = 0
        self.potions_hp = potions_hp
        self.damage, self.hp, self.defense, self.max_hp, self.crit, self.dexterity = (damage, max_hp,
                                                                                      defense, max_hp, crit, dexterity)
        self.move_sound_cooldown, self.move_cooldown = 10, 5
        self.temp_1 = 0

    def changing_characteristics(self):  # Функция, изменяющая характеристики персонажа
        self.damage, self.defense, self.max_hp, self.crit, self.dexterity = (PLAYER_DAMAGE, PLAYER_DEFENSE,
                                                                             MAX_HP_PLAYER, KNIGHT_CRIT, DEXTERITY)
        if last_max_hp < MAX_HP_PLAYER:
            self.hp = MAX_HP_PLAYER - (last_max_hp - self.hp)
        if last_max_hp > MAX_HP_PLAYER:
            self.hp = self.hp - (last_max_hp - MAX_HP_PLAYER)

    def attack(self, event):
        if event.key == pygame.K_f:
            self.attack_cur = 0
            self.flag_attack = 1

    def action_attack(self):  # Функция для отображения атаки и регистрации урона
        if not self.death_flag:
            attack_cooldown = 125
            if self.flag_attack == 1:
                self.image = self.animation_list[1][self.attack_cur]
                if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                        for i in mob_sprites:
                            if pygame.sprite.collide_mask(self, i):
                                if random.randrange(1, 400) <= self.crit * 4:
                                    i.hp = i.hp - ((self.damage + random.randrange(50, 200) / 100 * self.damage) - i.defense)
                                else:
                                    i.hp = i.hp - (self.damage - i.defense)
                                if i.hp <= 0:
                                    i.death_flag = True
                                    i.hp = 0
                    if self.attack_cur == 4:
                        sound_knight_attack.play()
                    self.attack_cur = (self.attack_cur + 1)
                if self.flag:
                    self.rotate()
                if not self.flag:
                    self.mask = pygame.mask.from_surface(self.image)
                if self.attack_cur == 5:
                    self.flag_attack = 0
                    self.attack_cur = 0
            elif not self.move_play:
                self.attack_cur = 0
                self.idle()

    def idle(self):  # Функция стоящего игрока
        idle_cooldown = 200
        self.image = self.animation_list[2][self.idle_cur]
        if pygame.time.get_ticks() - self.update_time > idle_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.idle_cur = (self.idle_cur + 1) % 4
        if self.flag:
            self.rotate()

    def move(self):
        if not self.death_flag:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.move_play = True
                self.m()
                self.flag = True
                self.rotate()
                self.sound_walk()
                self.rect.x -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.flag = False
                self.sound_walk()
                self.rect.x += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x -= SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.sound_walk()
                self.rect.y -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y += SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.sound_walk()
                self.rect.y += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y -= SPEED_PLAYER
            else:
                sound_knight_walk.stop()
                self.move_play = False

    def sound_walk(self):  # Функция для звука шагов
        if self.move_sound_cooldown == 0:
            sound_knight_walk.play()
        elif self.move_sound_cooldown < 0:
            self.move_sound_cooldown = 10

    def m(self):  # Функция для изменения спрайта при ходьбе
        self.image = self.animation_list[0][self.move_cur]
        if self.move_cooldown == 0:
            self.move_cur = (self.move_cur + 1) % 8
        elif self.move_cooldown < 0:
            self.move_cooldown = 2

    def rotate(self):  # Функция для поворота
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def use_health(self, event):  # Функция для использования зелий
        if event.key == pygame.K_z and self.potions_hp > 0 and not self.death_flag:
            self.potions_hp -= 1
            self.hp = self.hp + MAX_HP_PLAYER // 4
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def health(self):  # Функция для отображения здоровья
        if self.hp <= 0:
            self.death_flag = True
        pygame.draw.rect(screen, 'red', (10, 10, 200, 20))
        pygame.draw.rect(screen, 'green', (10, 10, int((self.hp / self.max_hp) * 200), 20))
        hp_bottle = pygame.transform.scale(load_image('levels/hp.png'), (50, 50))
        screen.blit(hp_bottle, (0, 60))
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.potions_hp}", True, (255, 255, 255))
        screen.blit(text, (30, 60))

    def dead(self):  # Функция для отображения смерти и окончания игры
        global flag_completion, text_exit, text_loss
        death_cooldown = 125
        self.temp_1 += 1
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > death_cooldown and self.death_cur != 5:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = self.death_cur + 1
            if self.death_cur == 5:
                self.death_cur = 5
            sql_update_data = f"""Update Data set last_level = '0'"""
            cursor.execute(sql_update_data)
            con.commit()
            if self.temp_1 == 50:
                text_loss = font_bigger.render('Вы проиграли', True, (255, 255, 255))
                text_exit = font.render('Выйти из игры', True, (255, 255, 255))
                flag_completion = True


class Blacksmith(pygame.sprite.Sprite):  # Класс кузнеца
    def __init__(self, x, y):
        super().__init__(npc_sprites, all_sprites)
        self.animation_list = [pygame.transform.scale(load_image(f"Blacksmith/{i}.png"),
                                                      (110, 160)) for i in range(1, 9)]
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect().move(13 + x * tile_width, y * tile_height - 10)
        self.update_time = pygame.time.get_ticks()
        self.idle_cur = 0

    def update(self):  # Функция для отображения кухнеца
        idle_cooldown = 200
        self.image = self.animation_list[self.idle_cur]
        if pygame.time.get_ticks() - self.update_time > idle_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.idle_cur = (self.idle_cur + 1) % 8


class Mag(pygame.sprite.Sprite):  # Класс мага
    def __init__(self, x, y, max_hp, damage, defense, potions_hp, potions_mana, max_mana, dexterity):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_walk/{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_attack1/{i}.png"),
                                                           (200, 130)) for i in range(1, 10)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_idle/{i}.png"),
                                                           (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_death/{i}.png"),
                                                           (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_attack2/{i}.png"),
                                                           (200, 130)) for i in range(1, 17)])
        self.bullets = []
        self.animation_bullet = []
        self.animation_bullet.append([load_image(f"Mag/charge/charge1/{i}.png") for i in range(1, 7)])
        self.animation_bullet.append([load_image(f"Mag/charge/charge2/{i}.png") for i in range(1, 10)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.potions_hp, self.potions_mana = potions_hp, potions_mana
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag, self.shot = False, False, False, False# Флаги поворота, движения, смерти, выстрела
        self.flag_attack = 0
        self.damage, self.hp, self.defense, self.max_hp, self.mana, self.max_mana, self.dexterity = (damage, max_hp, defense,
                                                                                                     max_hp, max_mana, max_mana, dexterity)
        self.shoot_cooldown = 0
        self.new_action = True
        self.defolt_attack = damage
        self.move_sound_cooldown, self.move_cooldown = 10, 5
        self.temp_1 = 0

    def changing_characteristics(self):  # Функция, изменяющая характеристики персонажа
        self.damage, self.defense, self.max_hp, self.crit, self.dexterity, self.max_mana = (PLAYER_DAMAGE, PLAYER_DEFENSE,
                                                                                            MAX_HP_PLAYER, KNIGHT_CRIT, DEXTERITY, MAX_MANA_PLAYER)
        self.mana = MAX_MANA_PLAYER
        if last_max_hp < MAX_HP_PLAYER:
            self.hp = MAX_HP_PLAYER - (last_max_hp - self.hp)
        if last_max_hp > MAX_HP_PLAYER:
            self.hp = self.hp - (last_max_hp - MAX_HP_PLAYER)

    def attack(self, event):  # Функция для обработки нажатия
        if event.key == pygame.K_f and self.new_action:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 30
                self.flag_attack = 1
                self.new_action = False
        elif event.key == pygame.K_r and self.mana - 10 >= 0 and self.new_action:
            if self.shoot_cooldown == 0:
                self.mana -= 10
                self.shoot_cooldown = 30
                self.flag_attack = 4
                self.new_action = False

    def action_attack(self):  # Функция для отображения атаки
        if not self.death_flag:
            if self.flag_attack == 1 or self.flag_attack == 4:
                attack_cooldown = 150
                self.image = self.animation_list[self.flag_attack][self.attack_cur]
                if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.attack_cur = (self.attack_cur + 1)
                    if self.attack_cur == 6 and self.flag_attack == 1:
                        bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag,
                                        self.defolt_attack, self.animation_bullet[0], 'player')
                        attacks_sprites.add(bullet)
                        all_sprites.add(bullet)
                        sound_charge1.play()
                    if self.attack_cur == 12 and self.flag_attack == 4:
                        bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag,
                                        self.defolt_attack * 2, self.animation_bullet[1], 'player')
                        attacks_sprites.add(bullet)
                        all_sprites.add(bullet)
                        sound_charge2.play()
                if self.flag:
                    self.rotate()
                if not self.flag:
                    self.mask = pygame.mask.from_surface(self.image)
                if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                    self.flag_attack = 0
                    self.attack_cur = 0
                    self.new_action = True
            elif not self.move_play:
                self.attack_cur = 0
                self.idle()

    def idle(self):  # Функция стоящего игрока
        idle_cooldown = 200
        self.image = self.animation_list[2][self.idle_cur]
        if pygame.time.get_ticks() - self.update_time > idle_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.idle_cur = (self.idle_cur + 1) % 4
        if self.flag:
            self.rotate()

    def move(self):
        if not self.death_flag:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.move_play = True
                self.m()
                self.sound_walk()
                self.flag = True
                self.rotate()
                self.rect.x -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.sound_walk()
                self.flag = False
                self.rect.x += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x -= SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                self.sound_walk()
                if self.flag:
                    self.rotate()
                self.rect.y -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y += SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                self.sound_walk()
                if self.flag:
                    self.rotate()
                self.rect.y += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y -= SPEED_PLAYER
            else:
                self.move_play = False

    def sound_walk(self):  # Функция звука шагов
        if self.move_sound_cooldown == 0:
            sound_knight_walk.play()
        elif self.move_sound_cooldown < 0:
            self.move_sound_cooldown = 10

    def m(self):  # Функция для изменения спрайта при ходьбе
        self.image = self.animation_list[0][self.move_cur]
        if self.move_cooldown == 0:
            self.move_cur = (self.move_cur + 1) % 7
        elif self.move_cooldown < 0:
            self.move_cooldown = 2

    def rotate(self):  # Функция поворота
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def use_health(self, event):  # Функция использования зелий здоровья и маны
        if event.key == pygame.K_z and self.potions_hp > 0 and not self.death_flag:
            self.potions_hp -= 1
            self.hp = self.hp + MAX_HP_PLAYER // 4
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        if event.key == pygame.K_x and self.potions_mana > 0 and not self.death_flag:
            self.potions_mana -= 1
            self.mana = self.mana + MAX_MANA_PLAYER // 4
            if self.mana > self.max_mana:
                self.mana = self.max_mana

    def health(self):  # Функция отображения здоровья
        if self.hp <= 0:
            self.death_flag = True
        pygame.draw.rect(screen, 'red', (10, 10, 200, 20))
        pygame.draw.rect(screen, 'green', (10, 10, int((self.hp / self.max_hp) * 200), 20))
        pygame.draw.rect(screen, 'red', (10, 30, 200, 20))
        pygame.draw.rect(screen, '#42aaff', (10, 30, int((self.mana / self.max_mana) * 200), 20))
        hp_bottle = pygame.transform.scale(load_image('levels/hp.png'), (50, 50))
        screen.blit(hp_bottle, (0, 60))
        mana_bottle = pygame.transform.scale(load_image('levels/mana.png'), (50, 50))
        screen.blit(mana_bottle, (0, 110))
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.potions_hp}", True, (255, 255, 255))
        screen.blit(text, (30, 60))
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.potions_mana}", True, (255, 255, 255))
        screen.blit(text, (30, 110))
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def dead(self):  # Функция смерти и конца игры
        global flag_completion, text_exit, text_loss
        death_cooldown = 125
        self.temp_1 += 1
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > death_cooldown and self.death_cur != 3:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = self.death_cur + 1
            if self.death_cur == 3:
                self.death_cur = 3
            sql_update_data = f"""Update Data set last_level = '0'"""
            cursor.execute(sql_update_data)
            con.commit()
            if self.temp_1 == 50:
                text_loss = font_bigger.render('Вы проиграли', True, (255, 255, 255))
                text_exit = font.render('Выйти из игры', True, (255, 255, 255))
                flag_completion = True


class Bullet(pygame.sprite.Sprite):  # Класс пули мага и лучника
    def __init__(self, x, y, direction, attack, image, attackers):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.attack_cur = 0
        if attackers == 'mob':
            self.image = image
        else:
            self.attack_animation = image
            self.image = self.attack_animation[self.attack_cur]
        self.rect = self.image.get_rect()
        if direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.center = (x + 50 * -1, y)
        else:
            self.rect.center = (x + 50, y)
        self.direction, self.attack = direction, attack
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        self.attackers = attackers

    def update(self):
        if self.attackers == 'player':
            if len(self.attack_animation) == 9:
                self.attack_cooldown = 120
            else:
                self.attack_cooldown = 250
        if pygame.time.get_ticks() - self.update_time > self.attack_cooldown and self.attackers == 'player':
            self.update_time = pygame.time.get_ticks()
            self.attack_cur = (self.attack_cur + 1) % (len(self.attack_animation) - 1)
        if self.direction:
            self.rect.x += (-1 * self.speed)
            if self.attackers == 'player':
                self.image = pygame.transform.flip(self.attack_animation[self.attack_cur % len(self.attack_animation)], True, False)
            else:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.x += self.speed
            if self.attackers == 'player':
                self.image = self.attack_animation[self.attack_cur % len(self.attack_animation)]
            else:
                self.image = self.image
        if self.attackers == 'mob':
            if self.rect.right < 200 or self.rect.left > height + 500:
                self.kill()
            if pygame.sprite.spritecollide(player, attacks_sprites, False):
                if not player.death_flag:
                    self.kill()
                    if not (random.randrange(1, 400) <= player.dexterity * 4):
                        player.hp -= 0 if self.attack <= player.defense else self.attack - player.defense
        else:
            if self.rect.right < 500 or self.rect.left > height + 200:
                self.kill()
            for i in mob_sprites:
                if pygame.sprite.spritecollide(i, attacks_sprites, False):
                    if not i.death_flag:
                        self.kill()
                        i.hp -= self.attack
                if i.hp <= 0:
                    i.death_flag = True


class Warrior(pygame.sprite.Sprite):  # Класс скелета
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_walk/skeleton_walk{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_idle/skeleton_idle{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_attack/skeleton_attack{i}.png"),
                                                           (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_death/skeleton_dead{i}.png"),
                                                           (200, 130)) for i in range(1, 5)])
        self.frame_index, self.cur = 1, 0
        self.move_cur, self.death_cur, self.attack_cur, self.idle_cur = 0, 0, 0, 0
        self.max_hp, self.hp, self.defense, self.damage = max_hp, max_hp, defense, damage
        self.x, self.y = x, y
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index][self.cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.mask = pygame.mask.from_surface(self.animation_list[2][3])
        self.death_flag, self.attack_flag, self.move_play, self.idle_flag = False, 0, False, True
        self.move_sound_cooldown, self.move_cooldown = 20, 5

    def idle(self):
        if self.idle_flag:
            idle_cooldown = 200
            self.image = self.animation_list[1][self.idle_cur]
            if pygame.time.get_ticks() - self.update_time > idle_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.idle_cur = (self.idle_cur + 1) % 6
        if not self.idle_flag:
            self.idle_cur = 0

    def attack(self):
        if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 80:
            self.action_attack()
            self.idle_flag = False
        else:
            self.move_play = True
            self.attack_cur = 0

    def action_attack(self):
        self.move_play = False
        attack_cooldown = 150
        if not self.death_flag:
            self.image = self.animation_list[2][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                if self.attack_cur == len(self.animation_list[2]) - 1:
                    if pygame.sprite.collide_mask(self, player):
                        if not (random.randrange(1, 400) <= player.dexterity * 4):
                            player.hp -= 0 if self.damage <= player.defense else self.damage - player.defense
                        if player.hp <= 0:
                            player.death_flag = True
                            player.hp = 0
                self.attack_cur = (self.attack_cur + 1) % 4
                if self.attack_cur == 2:
                    sound_warrior_attack.play()
            if self.animation_list[2][3] and player.rect[0] < self.rect[0]:
                self.rotate()
                self.mask = pygame.mask.from_surface(self.image)
            if self.animation_list[2][3] and player.rect[0] > self.rect[0]:
                self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if not self.death_flag and self.move_play:
            if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 360:
                self.idle_flag = False
                if player.rect[0] > self.rect[0]:
                    self.m()
                    self.sound_walk()
                    self.rect.x += SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.x -= SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.m()
                    self.sound_walk()
                    self.rect.x -= SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.x += SPEED_SKELETON
                if player.rect[1] > self.rect[1]:
                    self.m()
                    self.sound_walk()
                    self.rect.y += SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y -= SPEED_SKELETON
                if player.rect[1] < self.rect[1]:
                    self.m()
                    self.sound_walk()
                    self.rect.y -= SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y += SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.rotate()
            else:
                self.idle_flag = True

    def sound_walk(self):
        if self.move_sound_cooldown == 0:
            sound_skeleton_walk.play()
        elif self.move_sound_cooldown < 0:
            self.move_sound_cooldown = 20

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        if self.move_cooldown == 0:
            self.move_cur = (self.move_cur + 1) % 7
        elif self.move_cooldown < 0:
            self.move_cooldown = 2

    def dead(self):
        global gold
        self.idle_flag = False
        attack_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown and self.death_cur != 3:
                self.update_time = pygame.time.get_ticks()
                if self.death_cur == 0:
                    gold += AWARD
                    sql_update_query = f"""Update Data set money = '{gold}'"""
                    cursor.execute(sql_update_query)
                    con.commit()
                    sound_skeleton_death.play()
                self.death_cur = (self.death_cur + 1)
            if self.death_cur == 3:
                self.death_cur = 3

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))


class Archero(pygame.sprite.Sprite):  # Класс лучника
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_walk/{i}.png"),
                                                           (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_idle/{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_attack/{i}.png"),
                                                           (200, 130)) for i in range(1, 16)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_death/{i}.png"),
                                                           (200, 130)) for i in range(1, 6)])
        self.arrow = pygame.transform.scale(load_image('Skeleton_archero/Arrow.png'), (48, 26))
        self.frame_index, self.cur = 1, 0
        self.move_cur, self.death_cur, self.attack_cur, self.idle_cur = 0, 0, 0, 0
        self.max_hp, self.hp, self.defense, self.damage = max_hp, max_hp, defense, damage
        self.x, self.y = x, y
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index][self.cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.mask = pygame.mask.from_surface(self.image)
        self.death_flag, self.attack_flag, self.move_play, self.idle_flag, self.flag = False, 0, False, True, False
        self.defolt_attack = damage
        self.move_sound_cooldown, self.move_cooldown = 20, 5

    def idle(self):
        if self.idle_flag:
            idle_cooldown = 200
            self.image = self.animation_list[1][self.idle_cur]
            if pygame.time.get_ticks() - self.update_time > idle_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.idle_cur = (self.idle_cur + 1) % 6
        if not self.idle_flag:
            self.idle_cur = 0

    def attack(self):
        if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                player.rect.center[1] - self.rect.center[1]) ** 2) < 700:
            self.action_attack()
            self.idle_flag = False
        else:
            self.move_play = True

    def action_attack(self):
        self.move_play = False
        attack_cooldown = 100
        if not self.death_flag:
            self.image = self.animation_list[2][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                if self.attack_cur == 12:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag, self.defolt_attack, self.arrow, 'mob')
                    attacks_sprites.add(bullet)
                    all_sprites.add(bullet)
                    sound_archero_attack.play()
                self.attack_cur = (self.attack_cur + 1) % 15
            if player.rect[0] > self.rect[0]:
                self.flag = False
            elif player.rect[0] < self.rect[0]:
                self.flag = True
                self.rotate()

    def move(self):
        if not self.death_flag and self.move_play:
            if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 800:
                self.idle_flag = False
                if player.rect[1] > self.rect[1]:
                    self.m()
                    self.sound_walk()
                    self.rect.y += SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y -= SPEED_SKELETON
                if player.rect[1] < self.rect[1]:
                    self.m()
                    self.sound_walk()
                    self.rect.y -= SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y += SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.rotate()
                    self.flag = True
                if player.rect[0] > self.rect[0]:
                    self.flag = True
                if self.rect[1] == player.rect[1]:
                    self.idle_flag = True

    def sound_walk(self):
        if self.move_sound_cooldown == 0:
            sound_skeleton_walk.play()
        elif self.move_sound_cooldown < 0:
            self.move_sound_cooldown = 20

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        if self.move_cooldown == 0:
            self.move_cur = (self.move_cur + 1) % 7
        elif self.move_cooldown < 0:
            self.move_cooldown = 2

    def dead(self):
        global gold
        self.idle_flag = False
        attack_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown and self.death_cur != 4:
                self.update_time = pygame.time.get_ticks()
                if self.death_cur == 0:
                    gold += AWARD
                    sql_update_query = f"""Update Data set money = '{gold}'"""
                    cursor.execute(sql_update_query)
                    con.commit()
                    sound_skeleton_death.play()
                self.death_cur = (self.death_cur + 1)
            if self.death_cur == 4:
                self.death_cur = 4

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))


class Boss(pygame.sprite.Sprite):  # Класс босса
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Boss/walk/{i}.png"),
                                                           (200, 130)) for i in range(1, 14)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Boss/idle/{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Boss/attack1/{i}.png"),
                                                           (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Boss/attack2/{i}.png"),
                                                           (200, 130)) for i in range(1, 11)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Boss/dead/{i}.png"),
                                                           (200, 130)) for i in range(1, 4)])
        self.frame_index, self.cur = 1, 0
        self.move_cur, self.death_cur, self.attack_cur, self.idle_cur = 0, 0, 0, 0
        self.max_hp, self.hp, self.defense, self.damage = max_hp, max_hp, defense, damage
        self.x, self.y = x, y
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index][self.cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.mask = pygame.mask.from_surface(self.image)
        self.death_flag, self.attack_flag, self.move_play, self.idle_flag, self.flag = False, 0, False, True, False
        self.defolt_attack = damage
        self.move_cooldown = 5
        self.flag_attack = None
        self.new_motion = True
        self.temp_1 = 0

    def idle(self):
        if self.idle_flag:
            idle_cooldown = 200
            self.image = self.animation_list[1][self.idle_cur]
            if pygame.time.get_ticks() - self.update_time > idle_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.idle_cur = (self.idle_cur + 1) % 6
        if not self.idle_flag:
            self.idle_cur = 0

    def attack(self):
        if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 80:
            if self.new_motion:
                if random.randrange(1, 400) >= 0 and random.randrange(1, 400) <= 200:
                    self.flag_attack = 2
                    self.proverka = 4
                    self.new_motion = False
                else:
                    self.flag_attack = 3
                    self.proverka = 8
                    self.new_motion = False
            self.action_attack()
            self.idle_flag = False
        else:
            self.move_play = True
            self.attack_cur = 0

    def action_attack(self):
        self.move_play = False
        if self.flag_attack == 2:
            attack_cooldown = 150
        else:
            attack_cooldown = 100
        if not self.death_flag:
            self.image = self.animation_list[self.flag_attack][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                if self.attack_cur == self.proverka:
                    if pygame.sprite.collide_mask(self, player):
                        if not (random.randrange(1, 400) <= player.dexterity * 4):
                            player.hp -= 0 if self.damage * 2 <= player.defense else self.damage * 2 - player.defense
                        else:
                            player.hp -= 0 if self.damage <= player.defense else self.damage - player.defense
                        if player.hp <= 0:
                            player.death_flag = True
                            player.hp = 0
                self.attack_cur = (self.attack_cur + 1) % len(self.animation_list[self.flag_attack])
            if self.flag_attack == 2:
                if self.attack_cur == 5:
                    sound_boss_attack1.play()
                if self.attack_cur == 6:
                    sound_boss_attack1.stop()
                if self.animation_list[2][4] and player.rect[0] < self.rect[0]:
                    self.rotate()
                    self.mask = pygame.mask.from_surface(self.image)
                if self.animation_list[2][4] and player.rect[0] > self.rect[0]:
                    self.mask = pygame.mask.from_surface(self.image)
            else:
                if self.attack_cur == 7:
                    sound_boss_attack2.play()
                if self.attack_cur == 8:
                    sound_boss_attack2.stop()
                if self.animation_list[3][8] and player.rect[0] < self.rect[0]:
                    self.rotate()
                    self.mask = pygame.mask.from_surface(self.image)
                if self.animation_list[3][8] and player.rect[0] > self.rect[0]:
                    self.mask = pygame.mask.from_surface(self.image)
            if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                self.attack_cur = 0
                self.new_motion = True

    def move(self):
        if not self.death_flag and self.move_play:
            if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 1000:
                self.idle_flag = False
                if player.rect[0] > self.rect[0]:
                    self.m()
                    self.rect.x += SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.x -= SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.m()
                    self.rect.x -= SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.x += SPEED_SKELETON
                if player.rect[1] > self.rect[1]:
                    self.m()
                    self.rect.y += SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y -= SPEED_SKELETON
                if player.rect[1] < self.rect[1]:
                    self.m()
                    self.rect.y -= SPEED_SKELETON
                    if len(pygame.sprite.groupcollide(mob_sprites, tiles_collide_group, False, False)) != 0:
                        self.rect.y += SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.rotate()
            else:
                self.idle_flag = True

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        if self.move_cooldown == 0:
            self.move_cur = (self.move_cur + 1) % 13
        elif self.move_cooldown < 0:
            self.move_cooldown = 2

    def dead(self):
        global text_exit, text_win, flag_completion, flag_win
        self.temp_1 += 1
        self.idle_flag = False
        attack_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[4][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown and self.death_cur != 2:
                self.update_time = pygame.time.get_ticks()
                if self.death_cur == 0:
                    sound_skeleton_death.play()
                self.death_cur = (self.death_cur + 1)
            if self.death_cur == 2:
                self.death_cur = 2
            sql_update_data = f"""Update Data set last_level = '1'"""
            cursor.execute(sql_update_data)
            con.commit()
            if self.temp_1 == 50:
                text_win = font_bigger.render('Вы победили', True, (255, 255, 255))
                text_exit = font.render('Выйти из игры', True, (255, 255, 255))
                flag_win = True

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))


class Camera:  # Класс камеры
    def init(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        object.rect.x += self.dx
        object.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Inventory:  # Класс, для отображения инвентаря и обработки нажатий на предметы(артефакты)
    def __init__(self, width, height):
        global tab_inventory, gold, cursor, con, money
        self.con = con
        self.cursor = cursor
        tab_inventory = ["None" for i in range(20)]
        result = self.cursor.execute("""SELECT inventory FROM Data""").fetchone()[0].split()
        for i in range(len(result)):
            tab_inventory[i] = result[i]
        gold += int(self.cursor.execute("""SELECT money FROM Data""").fetchone()[0])
        self.click = False
        self.image_showing_characteristics = 'None'
        self.portable = 'None'
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 1110
        self.top = 590
        self.cell_size_x = 92
        self.cell_size_y = 68
        self.color = [(0, 0, 0), (0, 255, 0)]

    def render(self, screen):  # Функция, отображающая поле инвентаря
        global gold
        pygame.draw.rect(screen, (0, 0, 0), (1080, 0, 520, 900))
        text_inventory = font.render('Инвентарь', True, (255, 255, 255))
        text_equipment = font_small.render('Ваше снаряжение', True, (255, 255, 255))
        image_gold = pygame.transform.scale(load_image_inventory('gold.png'), (25, 25))
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
            screen.blit(load_image_inventory(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item
             = '{self.image_showing_characteristics}'""").fetchone()
            reading_characterestics(self.image_showing_characteristics)
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_selling_price = font_smaller.render('Цена при продаже ' + str(selling_price[0] // 2), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость(Уклонение) +' + str(dexterity[0]), True, (255, 255, 255))
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
            if critical[0] is not None:
                k += 1
                text_critical = font_smaller.render('Критический урон +' + str(critical[0]), True, (255, 255, 255))
                screen.blit(text_critical, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_selling_price, (1220, 150 + (20 * (k + 1))))

    def items(self):  # Функция, отображающая предметы(артефакты) в поле инвентаря
        for i in range(0, len(tab_inventory)):
            if tab_inventory[i] != 'None':
                image = load_image_inventory(str(tab_inventory[i]) + '.png')
                screen.blit(image, (1112 + ((i % 5) * 92), 592 + ((i // 5) * 68)))

    def clicking_cell(self, mouse_pos):  # Функция, считывающая координаты мыши
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 590) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 590) % 68)

    def get_click(self, event):  # Функция, обрабатывающая нажатие мыши
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
                        gold += int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item
                         = '{str(self.portable) + '.png'}'""").fetchone()[0]) // 2
                        self.portable = 'None'
                        self.image_showing_characteristics = 'None'
                        self.click = False
                        sound_buy_sell.play()
        if event.type == pygame.MOUSEBUTTONUP and self.click and self.portable != 'None':
            self.cell = self.clicking_cell(event.pos)
            self.click = False
            if (event.pos[0] < 1110 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400):
                if (event.pos[0] >= 1110 and event.pos[0] <= 1560) and (event.pos[1] >= 590 and event.pos[1] <= 862):
                    if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] == 'None':
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    else:
                        temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                        tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                        tab_inventory[self.position] = temp
                else:
                    tab_inventory[self.position] = self.portable
            if (event.pos[0] >= 1110 and event.pos[0] <= 1560) and (event.pos[1] >= 400 and event.pos[1] <= 468):
                self.cell = board_equ.clicking_cell(event.pos)
                if tab_equipment[self.cell[0]] == 'None':
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_inventory[self.position] = temp
            self.portable = 'None'

    def get_motion(self, x, y):  # Функция, отображающая предмет при его перемещении
        if self.click and self.portable != 'None':
            image = load_image_inventory(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))

    def showing_characteristics(self, event):  # Функция, отображающая характеристики предмета при наведении на него
        cell = self.clicking_cell(event.pos)
        if self.click is False:
            if cell[0] >= 0 and cell[1] >= 0 and cell[0] <= 4 and cell[1] <= 3:
                if tab_inventory[(cell[0] + (5 * cell[1] + 1)) - 1] != 'None':
                    self.image_showing_characteristics = str(tab_inventory[(cell[0] + (5 * cell[1] + 1)) - 1]) + '.png'
                else:
                    self.image_showing_characteristics = 'None'
            else:
                self.image_showing_characteristics = 'None'


class Equipment:  # Класс, для отображения экипировки и обработки нажатий на предметы(артефакты)
    def __init__(self, width, height):
        global tab_inventory, tab_equipment
        self.con = sqlite3.connect('forproject2.bd')
        self.cursor = self.con.cursor()
        self.click = False
        self.image_showing_characteristics = 'None'
        self.portable = 'None'
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 1110
        self.top = 400
        self.cell_size_x = 92
        self.cell_size_y = 68
        self.color = [(0, 0, 0), (0, 255, 0)]

    def render(self, screen):  # Функция, отображающая поле экипировки
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
            screen.blit(load_image_inventory(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item
             = '{self.image_showing_characteristics}'""").fetchone()
            reading_characterestics(self.image_showing_characteristics)
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_selling_price = font_smaller.render('Цена при продаже ' + str(selling_price[0] // 2), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость(Уклонение) +' + str(dexterity[0]), True, (255, 255, 255))
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
            if critical[0] is not None:
                k += 1
                text_critical = font_smaller.render('Критический урон +' + str(critical[0]), True, (255, 255, 255))
                screen.blit(text_critical, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_selling_price, (1220, 150 + (20 * (k + 1))))

    def items(self):  # Функция, отображающая предметы(артефакты) в поле экипировки
        for i in range(0, len(tab_equipment)):
            if tab_equipment[i] != 'None':
                image = load_image_inventory(str(tab_equipment[i]) + '.png')
                screen.blit(image, (1112 + ((i % 5) * 92), 402))

    def clicking_cell(self, mouse_pos):
        x = (mouse_pos[0] - 1110) // 92
        y = (mouse_pos[1] - 400) // 68
        return (x, y, (mouse_pos[0] - 1110) % 92, (mouse_pos[1] - 400) % 68)

    def get_click(self, event):  # Функция, обрабатывающая нажатие мыши
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
                        gold += int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item 
                        = '{str(self.portable) + '.png'}'""").fetchone()[0]) // 2
                        self.portable = 'None'
                        self.image_showing_characteristics = 'None'
                        self.click = False
                        sound_buy_sell.play()
        if event.type == pygame.MOUSEBUTTONUP and self.click and self.portable != 'None':
            self.click = False
            self.cell = self.clicking_cell(event.pos)
            if ((event.pos[0] < 1110 or event.pos[0] > 1560) or (event.pos[1] > 468 or event.pos[1] < 400)
                    and (event.pos[1] > 862 or event.pos[1] < 590)):
                tab_equipment[self.position] = self.portable
            if (event.pos[0] >= 1110 and event.pos[0] <= 1560) and (event.pos[1] >= 400 and event.pos[1] <= 468):
                if tab_equipment[self.cell[0]] == 'None':
                    tab_equipment[self.cell[0]] = self.portable
                else:
                    temp = tab_equipment[self.cell[0]]
                    tab_equipment[self.cell[0]] = self.portable
                    tab_equipment[self.position] = temp
            if (event.pos[0] >= 1110 and event.pos[0] <= 1560) and (event.pos[1] >= 590 and event.pos[1] <= 862):
                self.cell = board_inv.clicking_cell(event.pos)
                if tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] == 'None':
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                else:
                    temp = tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1]
                    tab_inventory[(self.cell[0] + (5 * self.cell[1] + 1)) - 1] = self.portable
                    tab_equipment[self.position] = temp
            self.portable = 'None'

    def get_motion(self, x, y):  # Функция, отображающая предмет при его перемещении
        if self.click and self.portable != 'None':
            image = load_image_inventory(self.portable + '.png')
            screen.blit(image, (x - self.cell[2], y - self.cell[3]))

    def showing_characteristics(self, event):  # Функция, отображающая характеристики предмета при наведении на него
        cell = self.clicking_cell(event.pos)
        if self.click is False:
            if cell[1] == 0 and cell[0] <= 4 and cell[0] >= 0:
                if tab_equipment[cell[0]] != 'None':
                    self.image_showing_characteristics = str(tab_equipment[cell[0]]) + '.png'
                else:
                    self.image_showing_characteristics = 'None'
            else:
                self.image_showing_characteristics = 'None'


class Bench:  # Класс, для отображения лавки торговца и обработки нажатий на предметы(артефакты)
    def __init__(self, width, height):
        global tab_inventory, tab_equipment, tab_bench, cursor, con
        self.con = con
        self.cursor = cursor
        self.image_showing_characteristics = 'None'
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

    def render(self, screen):  # Функция, отображающая поле лавки торговца
        global gold
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 520, 900))
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
            screen.blit(load_image_inventory(self.image_showing_characteristics), (1110, 150))
            selling_price = self.cursor.execute(f"""SELECT cost FROM Items WHERE item
             = '{self.image_showing_characteristics}'""").fetchone()
            reading_characterestics(self.image_showing_characteristics)
            name = ' '.join(self.image_showing_characteristics[:-9].split('_'))
            text_name = font_small.render(name, True, (255, 255, 255))
            text_buy_price = font_smaller.render('Цена при покупке ' + str(selling_price[0]), True, (255, 255, 0))
            screen.blit(text_name, (1110, 110))
            if dexterity[0] is not None:
                k += 1
                text_dexterity = font_smaller.render('Ловкость(Уклонение) +' + str(dexterity[0]), True, (255, 255, 255))
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
            if critical[0] is not None:
                k += 1
                text_critical = font_smaller.render('Критический урон +' + str(critical[0]), True, (255, 255, 255))
                screen.blit(text_critical, (1220, 150 + 20 * k))
            if speed[0] is not None:
                k += 1
                text_speed = font_smaller.render('Скорость +' + str(speed[0]), True, (255, 255, 255))
                screen.blit(text_speed, (1220, 150 + 20 * k))
            screen.blit(text_buy_price, (1220, 150 + (20 * (k + 1))))

    def items(self):  # Функция, отображающая предметы(артефакты) в поле лавки торговца
        for i in range(0, len(tab_bench)):
            if tab_bench[i] != 'None':
                image = load_image_inventory(str(tab_bench[i]))
                screen.blit(image, (32 + ((i % 5) * 92), 72 + ((i // 5) * 68)))

    def clicking_cell(self, mouse_pos):  # Функция, считывающая координаты мыши
        x = (mouse_pos[0] - 30) // 92
        y = (mouse_pos[1] - 70) // 68
        return (x, y, (mouse_pos[0]) % 92, (mouse_pos[1]) % 68)

    def get_click(self, event):  # Функция, обрабатывающая нажатие мыши
        global tab_bench, gold
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cell = self.clicking_cell(event.pos)
            self.position = (self.cell[0] + (5 * self.cell[1] + 1)) - 1
            if self.cell[0] >= 0 and self.cell[1] >= 0 and self.cell[0] <= 4 and self.cell[1] <= 5:
                self.click = True
                self.portable = tab_bench[self.position]
                if self.portable != 'None':
                    self.image_showing_characteristics = str(self.portable)
                if self.portable != 'None' and "None" in tab_inventory and gold >= int(self.cursor.execute(
                        f"""SELECT cost FROM Items WHERE item = '{self.portable}'""").fetchone()[0]):
                    gold -= int(self.cursor.execute(f"""SELECT cost FROM Items WHERE item = '{self.portable}'""").fetchone()[0])
                    for i in range(len(tab_inventory)):
                        if tab_inventory[i] == "None":
                            sound_buy_sell.play()
                            tab_inventory[i] = self.portable[:-4]
                            break

    def showing_characteristics(self, event):  # Функция, отображающая характеристики предмета при наведении на него
        cell = self.clicking_cell(event.pos)
        if cell[0] >= 0 and cell[1] >= 0 and cell[0] <= 4 and cell[1] <= 5:
            if tab_bench[(cell[0] + (5 * cell[1] + 1)) - 1] != 'None':
                self.image_showing_characteristics = str(tab_bench[(cell[0] + (5 * cell[1] + 1)) - 1])
            else:
                self.image_showing_characteristics = 'None'
        else:
            self.image_showing_characteristics = 'None'


def motion_cursor(x, y):  # Функция, заменяющая курсор мыши
    if pygame.mouse.get_focused():
        if flag_choice_cursor == 'defoult_cursor':
            pass
        if flag_choice_cursor == 'sword':
            pygame.mouse.set_visible(False)
            image = pygame.transform.scale(load_image_inventory(flag_choice_cursor + '.gif'), (34, 34))
            screen.blit(image, (x, y))
        if flag_choice_cursor == 'stick':
            pygame.mouse.set_visible(False)
            image = pygame.transform.scale(load_image_inventory(flag_choice_cursor + '.png'), (34, 42))
            screen.blit(image, (x, y))


if menu.main_menu.flag_exit:
    player_class = 0 if cursor.execute("""SELECT rasa FROM Data""").fetchone()[0] == 'knight' else 1
    camera = Camera()
    player, x, y = generate_level(load_level(f'level{(cursor.execute("""SELECT last_level FROM Data""").fetchone()[0])}.txt'))
    run_game = True
    run_invent = False
    clock = pygame.time.Clock()

    board_inv = Inventory(5, 4)
    board_equ = Equipment(5, 1)
    board_ben = Bench(5, 6)
    click = False
    flag_B = False
    flag_bench = True
    flag_completion = False
    flag_win = False
    cell = int()
    x_cursor = -1000
    y_cursor = -1000
    flag_choice_cursor = menu.main_menu.flag_choice_cursor

    while run_game:
        if flag_completion is False and flag_win is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                if event.type == pygame.MOUSEMOTION:
                    x_cursor = event.pos[0]
                    y_cursor = event.pos[1]
                if event.type == pygame.KEYDOWN:
                    player.attack(event)
                    player.use_health(event)
                    if event.key == pygame.K_TAB:
                        if run_invent:
                            run_invent = False
                            if board_equ.portable != 'None':
                                tab_equipment[board_equ.position] = board_equ.portable
                                board_equ.portable = 'None'
                            if board_inv.portable != 'None':
                                tab_inventory[board_inv.position] = board_inv.portable
                                board_inv.portable = 'None'
                        else:
                            run_invent = True
                            x_motion = -1000
                            y_motion = -1000
                    if run_invent and event.key == pygame.K_b:
                        if event.type == pygame.KEYDOWN:
                            flag_B = True
                        if event.type == pygame.KEYUP:
                            flag_B = False
                if event.type == pygame.KEYUP:
                    if run_invent and event.key == pygame.K_b:
                        flag_B = False

                if run_invent:
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

                    sql_update_query = f"""Update Data set inventory = '{' '.join(tab_inventory)}',
                    equipment = '{' '.join(tab_equipment)}',
                    money = '{gold}'"""
                    cursor.execute(sql_update_query)
                    con.commit()

                    MAX_HP_PLAYER = cursor.execute("""SELECT player_health FROM Data""").fetchone()[0]
                    PLAYER_DAMAGE = cursor.execute("""SELECT player_damage FROM Data""").fetchone()[0]
                    PLAYER_DEFENSE = cursor.execute("""SELECT player_protection FROM Data""").fetchone()[0]
                    if rasa == 'knight':
                        MAX_MANA_PLAYER = 'None'
                    else:
                        MAX_MANA_PLAYER = int(cursor.execute("""SELECT player_mana FROM Data""").fetchone()[0])
                    if rasa == 'knight':
                        KNIGHT_CRIT = int(cursor.execute("""SELECT player_critical FROM Data""").fetchone()[0])
                    else:
                        KNIGHT_CRIT = 'None'
                    DEXTERITY = cursor.execute("""SELECT player_dexterity FROM Data""").fetchone()[0]
                    SPEED_PLAYER = cursor.execute("""SELECT player_speed FROM Data""").fetchone()[0]

                    for p in tab_equipment:
                        if p != 'None':
                            reading_characterestics(p + '.png')
                            if health[0] is not None:
                                MAX_HP_PLAYER += health[0]
                            if physical_damage[0] is not None:
                                if rasa == 'knight':
                                    PLAYER_DAMAGE += physical_damage[0]
                            if magic_damage[0] is not None:
                                if rasa == 'wizard':
                                    PLAYER_DAMAGE += magic_damage[0]
                            if armor[0] is not None:
                                PLAYER_DEFENSE += armor[0]
                            if mane[0] is not None:
                                if rasa == 'wizard':
                                    MAX_MANA_PLAYER += mane[0]
                            if critical[0] is not None:
                                if rasa == 'knight':
                                    KNIGHT_CRIT += int(critical[0][:-1])
                            if dexterity[0] is not None:
                                DEXTERITY += int(dexterity[0][:-1])
                            if speed[0] is not None:
                                SPEED_PLAYER += speed[0]
                    player.changing_characteristics()
                    last_max_hp = MAX_HP_PLAYER

            screen.fill((0, 0, 0))
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            all_sprites.draw(screen)
            mob_sprites.draw(screen)
            npc_sprites.draw(screen)
            npc_sprites.update()
            for i in mob_sprites:
                if not i.attack_flag:
                    i.move()
                    i.move_cooldown -= 1
                    i.move_sound_cooldown -= 1
                i.health()
                i.idle()
                i.attack()
                if i.death_flag:
                    i.dead()

            player_sprites.draw(screen)
            player.move()
            player.move_sound_cooldown -= 1
            player.move_cooldown -= 1
            player.action_attack()
            player.health()
            if player.death_flag:
                player.dead()

            if pygame.sprite.spritecollideany(player, tiles_collide_exit):
                clear_ini_group()
                sql_update_data = f"""Update Data set last_level = '{str(now_level + 1)}'"""
                cursor.execute(sql_update_data)
                con.commit()
                now_level = int(cursor.execute("""SELECT last_level FROM Data""").fetchone()[0])
                сhanging_characteristics_enemies()
                player, x, y = generate_level(load_level(f'level{str(now_level)}.txt'))
                music = pygame.mixer.music.load(f'music/{playlist[now_level]}.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(
                    float(cursor.execute("""SELECT sound_music_game FROM Data""").fetchone()[0]))

            if pygame.sprite.spritecollideany(player, tiles_collide_back):
                clear_ini_group()
                sql_update_data = f"""Update Data set last_level = '{str(now_level - 1)}'"""
                cursor.execute(sql_update_data)
                con.commit()
                now_level = int(cursor.execute("""SELECT last_level FROM Data""").fetchone()[0])
                сhanging_characteristics_enemies()
                player, x, y = generate_level(load_level(f'level{str(now_level)}.txt'))
                music = pygame.mixer.music.load(f'music/{playlist[now_level]}.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(
                    float(cursor.execute("""SELECT sound_music_game FROM Data""").fetchone()[0]))

            if pygame.sprite.spritecollideany(player, tiles_market):
                player.potions_hp = PLAYER_POTIONS_HP
                player.potions_mana = PLAYER_POTIONS_MANA
                player.hp = MAX_HP_PLAYER
                player.mana = MAX_MANA_PLAYER
                flag_bench = True
            else:
                flag_bench = False

            attacks_sprites.update()

            if run_invent:
                board_inv.render(screen)
                board_equ.render(screen)
                if flag_bench:
                    board_ben.render(screen)
                board_equ.get_motion(x_motion, y_motion)
                board_inv.get_motion(x_motion, y_motion)
                pygame.display.flip()

            motion_cursor(x_cursor, y_cursor)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                if event.type == pygame.MOUSEMOTION:
                    x_cursor = event.pos[0]
                    y_cursor = event.pos[1]
                    if (event.pos[0] >= width // 2 - text_exit.get_width() // 2 and
                            event.pos[0] <= width // 2 - text_exit.get_width() // 2 + text_exit.get_width() and
                            event.pos[1] >= 400 and event.pos[1] <= 400 + text_exit.get_height()):
                        text_exit = font_big.render('Выйти из игры', True, (255, 255, 255))
                    else:
                        text_exit = font.render('Выйти из игры', True, (255, 255, 255))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.pos[0] >= width // 2 - text_exit.get_width() // 2 and
                            event.pos[0] <= width // 2 - text_exit.get_width() // 2 + text_exit.get_width() and
                            event.pos[1] >= 400 and event.pos[1] <= 400 + text_exit.get_height()):
                        run_game = False
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1600, 900))
            if flag_completion:
                screen.blit(text_loss, (width // 2 - text_loss.get_width() // 2, 300))
            if flag_win:
                screen.blit(text_win, (width // 2 - text_win.get_width() // 2, 300))
            screen.blit(text_exit, (width // 2 - text_exit.get_width() // 2, 400))
            motion_cursor(x_cursor, y_cursor)

        clock.tick(FPS)
        pygame.display.flip()

cursor.close()
con.close()

pygame.quit()
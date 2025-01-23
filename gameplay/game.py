import pygame
import os
import sys
import random
import math
import sqlite3
import menu.main_menu


def load_image(name, colorkey=None):
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


if menu.main_menu.flag_exit:
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)
    player_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    tiles_market = pygame.sprite.Group()
    tiles_collide_group = pygame.sprite.Group()
    tiles_collide_exit = pygame.sprite.Group()
    attacks_sprites = pygame.sprite.Group()
    SPEED_SKELETON = 10
    SPEED_PLAYER = 50
    FPS = 15
    PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_POTIONS_HP, PLAYER_POTIONS_MANA, MAX_MANA_PLAYER = 250, 250, 100, 50, 5, 3, 5, 200
    MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE = 100, 20, 0
    sound1 = pygame.mixer.Sound('data/Knight/knight_attack.mp3')
    sound2 = pygame.mixer.Sound('data/Knight/knight_move.mp3')

    con = sqlite3.connect('forproject2.bd')
    cursor = con.cursor()

    tile_images = {
        'wall': pygame.transform.scale(load_image('levels/cave_wall.png'), (150, 150)),
        'empty': pygame.transform.scale(load_image('levels/cave_pol.png'), (150, 150)),
        'exit': pygame.transform.scale(load_image('levels/cave.png'), (150, 150))
    }
    tile_width = tile_height = 150


def load_level(filename):
    with open('data/levels/' + filename, 'r') as levelfile:
        level_map = [line.strip() for line in levelfile.readlines()]
    max_len = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_len, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_collide(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_collide_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_exit(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_collide_exit, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile_market(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_market, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
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
            elif level[y][x] == "@":
                Tile('empty', x, y)
                if player_class == 0:
                    new_player = Knight(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_POTIONS_HP)
                else:
                    new_player = Mag(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_POTIONS_HP, PLAYER_POTIONS_MANA, MAX_MANA_PLAYER)
            elif level[y][x] == "$":
                Tile('empty', x, y)
                Warrior(x, y, MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Archero(x, y, MAX_HP_MOB // 2, MOB_DAMAGE, MOB_DEFENSE)
    return new_player, x, y


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense, potions_hp):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/walk/walk{i}.png"), (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/attack/attack{i}.png"), (200, 130)) for i in range(1, 6)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/idle/idle{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Knight/death/Dead{i}.png"), (200, 130)) for i in range(1, 7)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag = False, False, False
        self.flag_attack = 0
        self.potions_hp = potions_hp
        self.damage, self.hp, self.defense, self.max_hp, self.crit = damage, max_hp, defense, max_hp, 5

    def attack(self, event):
        if event.key == pygame.K_f:
            self.attack_cur = 0
            self.flag_attack = 1

    def action_attack(self):
        if not self.death_flag:
            attack_cooldown = 125
            if self.flag_attack == 1:
                self.image = self.animation_list[1][self.attack_cur]
                if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                        for i in mob_sprites:
                            if pygame.sprite.collide_mask(self, i):
                                if random.randrange(1, 400) / 4 <= self.crit:
                                    i.hp = i.hp - ((self.damage + (self.damage // 100) * self.crit) - i.defense)
                                else:
                                    i.hp = i.hp - (self.damage - i.defense)
                                if i.hp <= 0:
                                    i.death_flag = True
                                    i.hp = 0
                    self.attack_cur = (self.attack_cur + 1)
                    if self.attack_cur == 4:
                        sound1.play()
                if self.flag:
                    self.rotate()
                if not self.flag:
                    self.mask = pygame.mask.from_surface(self.image)
                if self.attack_cur == 5:
                    self.flag_attack = 0
                    self.attack_cur = 0
                    sound1.stop()
            elif not self.move_play:
                self.attack_cur = 0
                self.idle()

    def idle(self):
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
                self.rect.x -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.flag = False
                self.rect.x += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x -= SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y += SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y -= SPEED_PLAYER
            else:
                self.move_play = False

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 8

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def use_health(self, event):
        if event.key == pygame.K_z and self.potions_hp > 0 and not self.death_flag:
            self.potions_hp -= 1
            self.hp = self.hp + 30
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        pygame.draw.rect(screen, 'red', (10, 10, 200, 20))
        pygame.draw.rect(screen, 'green', (10, 10, int((self.hp / self.max_hp) * 200), 20))
        hp_bottle = pygame.transform.scale(load_image('levels/hp.png'), (50, 50))
        screen.blit(hp_bottle, (0, 60))
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.potions_hp}", True, (255, 255, 255))
        screen.blit(text, (30, 60))

    def dead(self):
        death_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > death_cooldown and self.death_cur != 5:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = self.death_cur + 1
            if self.death_cur == 5:
                self.death_cur = 5


class Mag(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense, potions_hp, potions_mana, max_mana):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_walk/{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_attack1/{i}.png"), (200, 130)) for i in range(1, 10)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_idle/{i}.png"), (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_death/{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Mag/mag_attack2/{i}.png"), (200, 130)) for i in range(1, 17)])
        self.bullets = []
        self.animation_bullet = []
        self.animation_bullet.append([load_image(f"Mag/charge/charge1/{i}.png") for i in range(1, 7)])
        self.animation_bullet.append([load_image(f"Mag/charge/charge2/{i}.png") for i in range(1, 10)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.potions_hp, self.potions_mana = potions_hp, potions_mana
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag, self.shot = False, False, False, False
        self.flag_attack = 0
        self.damage, self.hp, self.defense, self.max_hp, self.mana, self.max_mana = damage, max_hp, defense, max_hp, max_mana, max_mana
        self.shoot_cooldown = 0
        self.new_action = True
        self.defolt_attack, self.super_attack = 10, 30

    def attack(self, event):
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

    def action_attack(self):
        if not self.death_flag:
            if self.flag_attack == 1 or self.flag_attack == 4:
                attack_cooldown = 150
                self.image = self.animation_list[self.flag_attack][self.attack_cur]
                if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.attack_cur = (self.attack_cur + 1)
                    if self.attack_cur == 6 and self.flag_attack == 1:
                        bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag, self.defolt_attack, self.animation_bullet[0], 'player')
                        attacks_sprites.add(bullet)
                        all_sprites.add(bullet)
                    if self.attack_cur == 12 and self.flag_attack == 4:
                        bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag, self.super_attack, self.animation_bullet[1], 'player')
                        attacks_sprites.add(bullet)
                        all_sprites.add(bullet)
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

    def idle(self):
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
                self.rect.x -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.flag = False
                self.rect.x += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.x -= SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y -= SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y += SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y += SPEED_PLAYER
                if len(pygame.sprite.groupcollide(player_sprites, tiles_collide_group, False, False)) != 0:
                    self.rect.y -= SPEED_PLAYER
            else:
                self.move_play = False

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 7

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def use_health(self, event):
        if event.key == pygame.K_z and self.potions_hp > 0 and not self.death_flag:
            self.potions_hp -= 1
            self.hp = self.hp + 30
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        if event.key == pygame.K_x and self.potions_mana > 0 and not self.death_flag:
            self.potions_mana -= 1
            self.mana = self.mana + 30
            if self.mana > self.max_mana:
                self.mana = self.max_mana

    def health(self):
        if self.hp == 0:
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

    def dead(self):
        death_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > death_cooldown and self.death_cur != 3:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = self.death_cur + 1
            if self.death_cur == 3:
                self.death_cur = 3


class Bullet(pygame.sprite.Sprite):
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
        if self.rect.right < 500 or self.rect.left > height + 200:
            self.kill()
        if self.attackers == 'mob':
            if pygame.sprite.spritecollide(player, attacks_sprites, False):
                if not player.death_flag:
                    self.kill()
                    player.hp -= self.attack
        else:
            for i in mob_sprites:
                if pygame.sprite.spritecollide(i, attacks_sprites, False):
                    if not i.death_flag:
                        self.kill()
                        i.hp -= self.attack
                if i.hp <= 0:
                    i.death_flag = True


class Warrior(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_walk/skeleton_walk{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_idle/skeleton_idle{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_attack/skeleton_attack{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_warrior/skeleton_death/skeleton_dead{i}.png"), (200, 130)) for i in range(1, 5)])
        self.frame_index, self.cur = 1, 0
        self.move_cur, self.death_cur, self.attack_cur, self.idle_cur = 0, 0, 0, 0
        self.max_hp, self.hp, self.defense, self.damage = max_hp, max_hp, defense, damage
        self.x, self.y = x, y
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index][self.cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.mask = pygame.mask.from_surface(self.animation_list[2][3])
        self.death_flag, self.attack_flag, self.move_play, self.idle_flag = False, 0, False, True

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
        attack_cooldown = 125
        if not self.death_flag:
            self.image = self.animation_list[2][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                if self.attack_cur == len(self.animation_list[2]) - 1:
                    if pygame.sprite.collide_mask(self, player):
                        player.hp = player.hp - (self.damage - player.defense)
                        if player.hp <= 0:
                            player.death_flag = True
                            player.hp = 0
                self.attack_cur = (self.attack_cur + 1) % 4
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

    def dead(self):
        self.idle_flag = False
        attack_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown and self.death_cur != 3:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = (self.death_cur + 1)
            if self.death_cur == 3:
                self.death_cur = 3

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 7

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))


class Archero(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_walk/{i}.png"), (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_idle/{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_attack/{i}.png"), (200, 130)) for i in range(1, 16)])
        self.animation_list.append([pygame.transform.scale(load_image(f"Skeleton_archero/skeleton_death/{i}.png"), (200, 130)) for i in range(1, 6)])
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
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 360:
            self.action_attack()
            self.idle_flag = False
        else:
            self.move_play = True

    def action_attack(self):
        self.move_play = False
        attack_cooldown = 125
        if not self.death_flag:
            self.image = self.animation_list[2][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                if self.attack_cur == 12:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, self.flag, self.defolt_attack, self.arrow, 'mob')
                    attacks_sprites.add(bullet)
                    all_sprites.add(bullet)
                self.attack_cur = (self.attack_cur + 1) % 15
            if player.rect[0] > self.rect[0]:
                self.flag = False
            elif player.rect[0] < self.rect[0]:
                self.flag = True
                self.rotate()

    def move(self):
        if not self.death_flag and self.move_play:
            if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 600:
                self.idle_flag = False
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
                    self.flag = True
                if player.rect[0] > self.rect[0]:
                    self.flag = True
                if player.rect[1] == self.rect[1]:
                    self.idle_flag = True

    def dead(self):
        self.idle_flag = False
        attack_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown and self.death_cur != 4:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = (self.death_cur + 1)
            if self.death_cur == 4:
                self.death_cur = 4

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 7

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))


class Camera:
    def init(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        object.rect.x += self.dx
        object.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if menu.main_menu.flag_exit:
    player_class = 0 if cursor.execute("""SELECT rasa FROM Data""").fetchone()[0] == 'knight' else 1
    camera = Camera()
    player, x, y = generate_level(load_level('level1.txt'))
    run_game = True
    clock = pygame.time.Clock()
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                player.attack(event)
                player.use_health(event)
        screen.fill((0, 0, 0))
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)
        mob_sprites.draw(screen)
        for i in mob_sprites:
            if not i.attack_flag:
                i.move()
            i.health()
            i.idle()
            i.attack()
            if i.death_flag:
                i.dead()

        player_sprites.draw(screen)
        player.move()
        player.action_attack()
        player.health()
        if player.death_flag:
            player.dead()

        if pygame.sprite.spritecollideany(player, tiles_collide_exit):
            run_game = False

        if pygame.sprite.spritecollideany(player, tiles_market):
            player.potions_hp = PLAYER_POTIONS_HP
            player.potions_mana = PLAYER_POTIONS_MANA
            player.hp = MAX_HP_PLAYER
            player.mana = MAX_MANA_PLAYER

        attacks_sprites.update()

        clock.tick(FPS)
        pygame.display.flip()

pygame.quit()
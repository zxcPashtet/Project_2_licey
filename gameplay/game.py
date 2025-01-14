import pygame
import os
import sys
import random
import math


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
player_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
SPEED_SKELETON = 10
SPEED_PLAYER = 50
FPS = 10
PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN = 250, 250, 100, 15, 5, 3
MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE = 100, 20, 3


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


tile_images = {
    'wall': pygame.transform.scale(load_image('box.jpg'), (150, 150)),
    'empty': pygame.transform.scale(load_image('grass.png'), (150, 150))
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                if player_class == 0:
                    new_player = Knight(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN)
                else:
                    new_player = Mag(x, y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, 200)
            elif level[y][x] == "$":
                Tile('empty', x, y)
                mob = Mob(x, y, MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE)
    return new_player, x, y


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense, potions):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"walk/walk{i}.png"), (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"attack/attack{i}.png"), (200, 130)) for i in range(1, 6)])
        self.animation_list.append([pygame.transform.scale(load_image(f"idle/idle{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"death/Dead{i}.png"), (200, 130)) for i in range(1, 7)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag = False, False, False
        self.flag_attack = 0
        self.damage, self.hp, self.defense, self.max_hp = damage, max_hp, defense, max_hp

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
                    for i in mob_sprites:
                        if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                            if pygame.sprite.collide_mask(self, i):
                                i.hp = i.hp - (self.damage - i.defense)
                                if i.hp <= 0:
                                    i.death_flag = True
                                    i.hp = 0
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
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.flag = False
                self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y -= SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y += SPEED_PLAYER
            else:
                self.move_play = False

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 8

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (10, 10, 200, 20))
            pygame.draw.rect(screen, 'green', (10, 10, int((self.hp / self.max_hp) * 200), 20))

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
    def __init__(self, x, y, max_hp, damage, defense, max_mana):
        super().__init__(player_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"mag_walk/{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"mag_attack1/{i}.png"), (200, 130)) for i in range(1, 10)])
        self.animation_list.append([pygame.transform.scale(load_image(f"mag_idle/{i}.png"), (200, 130)) for i in range(1, 9)])
        self.animation_list.append([pygame.transform.scale(load_image(f"mag_death/{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"mag_attack2/{i}.png"), (200, 130)) for i in range(1, 17)])
        self.bullets = []
        self.animation_bullet = []
        self.animation_bullet.append([load_image(f"charge1/{i}.png") for i in range(1, 7)])
        self.animation_bullet.append([load_image(f"charge2/{i}.png") for i in range(1, 10)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect().move(13 + x * tile_width, 5 + y * tile_height)
        self.flag, self.move_play, self.death_flag, self.shot = False, False, False, False
        self.flag_attack = 0
        self.damage, self.hp, self.defense, self.max_hp, self.mana, self.max_mana = damage, max_hp, defense, max_hp, max_mana, max_mana

    def attack(self, event):
        if event.key == pygame.K_f:
            self.attack_cur = 0
            self.flag_attack = 1
        elif event.key == pygame.K_r and self.mana - 10 >= 0:
            self.mana -= 10
            self.attack_cur = 0
            self.flag_attack = 4

    def action_bullet(self):
        pass

    def action_attack(self):
        if not self.death_flag:
            if self.flag_attack == 1 or self.flag_attack == 4:
                attack_cooldown = 150
                self.image = self.animation_list[self.flag_attack][self.attack_cur]
                if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    for i in mob_sprites:
                        if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                            if pygame.sprite.collide_mask(self, i):
                                i.hp = i.hp - (self.damage - i.defense)
                                if i.hp <= 0:
                                    i.death_flag = True
                                    i.hp = 0
                    self.attack_cur = (self.attack_cur + 1)
                    if self.attack_cur == 5 and self.flag_attack == 1:
                        pass
                    if self.attack_cur == 12 and self.flag_attack == 4:
                        pass
                if self.flag:
                    self.rotate()
                    self.animation_list[0][2] = pygame.transform.flip(self.animation_bullet[0][2], True, False)
                if not self.flag:
                    self.mask = pygame.mask.from_surface(self.image)
                if self.attack_cur == len(self.animation_list[self.flag_attack]) - 1:
                    self.flag_attack = 0
                    self.attack_cur = 0
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
            elif keys[pygame.K_d]:
                self.move_play = True
                self.m()
                self.flag = False
                self.rect.x += SPEED_PLAYER
            elif keys[pygame.K_w]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y -= SPEED_PLAYER
            elif keys[pygame.K_s]:
                self.move_play = True
                self.m()
                if self.flag:
                    self.rotate()
                self.rect.y += SPEED_PLAYER
            else:
                self.move_play = False

    def m(self):
        self.image = self.animation_list[0][self.move_cur]
        self.move_cur = (self.move_cur + 1) % 7

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (10, 10, 200, 20))
            pygame.draw.rect(screen, 'green', (10, 10, int((self.hp / self.max_hp) * 200), 20))
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (30, 30, 200, 20))
            pygame.draw.rect(screen, '#42aaff', (30, 30, int((self.mana / self.max_mana) * 200), 20))

    def dead(self):
        death_cooldown = 125
        if self.death_flag:
            self.image = self.animation_list[3][self.death_cur]
            if pygame.time.get_ticks() - self.update_time > death_cooldown and self.death_cur != 3:
                self.update_time = pygame.time.get_ticks()
                self.death_cur = self.death_cur + 1
            if self.death_cur == 3:
                self.death_cur = 3


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense):
        super().__init__(mob_sprites, all_sprites)
        self.animation_list = []
        self.animation_list.append([pygame.transform.scale(load_image(f"skeleton_walk/skeleton_walk{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"skeleton_idle/skeleton_idle{i}.png"), (200, 130)) for i in range(1, 8)])
        self.animation_list.append([pygame.transform.scale(load_image(f"skeleton_attack/skeleton_attack{i}.png"), (200, 130)) for i in range(1, 5)])
        self.animation_list.append([pygame.transform.scale(load_image(f"skeleton_death/skeleton_dead{i}.png"), (200, 130)) for i in range(1, 5)])
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

    def action_attack(self):
        self.move_play = False
        attack_cooldown = 125
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
        elif player.rect[0] < self.rect[0]:
            self.rotate()

    def move(self):
        if not self.death_flag and self.move_play:
            if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 360:
                self.idle_flag = False
                if player.rect[0] > self.rect[0]:
                    self.m()
                    self.rect.x += SPEED_SKELETON
                if player.rect[0] < self.rect[0]:
                    self.m()
                    self.rect.x -= SPEED_SKELETON
                if player.rect[1] > self.rect[1]:
                    self.m()
                    self.rect.y += SPEED_SKELETON
                if player.rect[1] < self.rect[1]:
                    self.m()
                    self.rect.y -= SPEED_SKELETON
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


player_class = 1
camera = Camera()
player, x, y = generate_level(load_level('level1.txt'))
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.attack(event)
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
    if player_class == 1:
        player.action_bullet()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
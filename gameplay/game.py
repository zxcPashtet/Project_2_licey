import pygame
import os
import sys
import random
import math


SPEED_SKELETON = 1
SPEED_PLAYER = 5
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


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense, regen):
        pygame.sprite.Sprite.__init__(self, player_sprites)
        self.animation_list = []
        self.animation_list.append([load_image(f"walk/walk{i}.png") for i in range(1, 9)])
        self.animation_list.append([load_image(f"attack/attack{i}.png") for i in range(1, 6)])
        self.animation_list.append([load_image(f"idle/idle{i}.png") for i in range(1, 5)])
        self.animation_list.append([load_image(f"death/Dead{i}.png") for i in range(1, 7)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
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
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))

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
    def __init__(self, x, y, max_hp, damage, defense, regen):
        pygame.sprite.Sprite.__init__(self, player_sprites)
        self.animation_list = []
        self.animation_list.append([load_image(f"mag_walk/mag_walk{i}.png") for i in range(1, 8)])
        self.animation_list.append([load_image(f"mag_attack1/mag_attack1{i}.png") for i in range(1, 8)])
        self.animation_list.append([load_image(f"mag_idle/mag_idle{i}.png") for i in range(1, 9)])
        self.animation_list.append([load_image(f"mag_death/mag_dead{i}.png") for i in range(1, 5)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur, self.death_cur = 2, 0, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
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
        self.move_cur = (self.move_cur + 1) % 7

    def rotate(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def health(self):
        if self.hp == 0:
            self.death_flag = True
        if not self.death_flag:
            pygame.draw.rect(screen, 'red', (self.rect.x + 50, self.rect.y, 20, 3))
            pygame.draw.rect(screen, 'green', (self.rect.x + 50, self.rect.y, int((self.hp / self.max_hp) * 20), 3))

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
        pygame.sprite.Sprite.__init__(self, mob_sprites)
        self.animation_list = []
        self.animation_list.append([load_image(f"skeleton_walk/skeleton_walk{i}.png") for i in range(1, 8)])
        self.animation_list.append([load_image(f"skeleton_idle/skeleton_idle{i}.png") for i in range(1, 8)])
        self.animation_list.append([load_image(f"skeleton_attack/skeleton_attack{i}.png") for i in range(1, 5)])
        self.animation_list.append([load_image(f"skeleton_death/skeleton_dead{i}.png") for i in range(1, 5)])
        self.frame_index, self.cur = 1, 0
        self.move_cur, self.death_cur, self.attack_cur = 0, 0, 0
        self.max_hp, self.hp, self.defense, self.damage = max_hp, max_hp, defense, damage
        self.x, self.y = x, y
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index][self.cur]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.animation_list[2][3])
        self.rect.center = x, y
        self.death_flag, self.attack_flag, self.move_play = False, 0, False

    def update(self):
        if not self.death_flag:
            attack_cooldown = 125
            self.image = self.animation_list[1][self.cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.cur = (self.cur + 1) % 6

    def idle(self):
        if not self.death_flag:
            self.frame_index, self.cur, self.update_time = 3, 0, pygame.time.get_ticks()

    def attack(self):
        if math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 40:
            self.action_attack()
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
                    player.rect.center[1] - self.rect.center[1]) ** 2) <= 240:
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

    def dead(self):
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


player_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
player_class = int(input())
pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
if player_class == 0:
    player = Knight(PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN)
else:
    player = Mag(PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN)
for _ in range(1):
    mob = Mob(random.randrange(1, 500), random.randrange(1, 500), MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE)
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.attack(event)
    for i in mob_sprites:
        if not i.attack_flag:
            i.move()
        i.health()
        i.attack()
        if i.death_flag:
            i.dead()

    player_sprites.draw(screen)
    player.move()
    player.action_attack()
    player.health()
    if player.death_flag:
        player.dead()

    mob_sprites.draw(screen)
    mob_sprites.update()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
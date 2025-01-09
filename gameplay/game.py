import pygame
import os
import sys
import random


SPEED_SKELETON = 0.5
SPEED_PLAYER = 5
FPS = 10
PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN = 250, 250, 100, 15, 30, 3
MAX_HP_MOB, MOB_DAMAGE, MOB_DEFENSE = 100, 4, 3


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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, defense, regen):
        pygame.sprite.Sprite.__init__(self, player_sprites)
        self.animation_list = []
        self.animation_list.append([load_image(f"walk/walk{i}.png") for i in range(1, 9)])
        self.animation_list.append([load_image(f"attack/attack{i}.png") for i in range(1, 6)])
        self.animation_list.append([load_image(f"idle/idle{i}.png") for i in range(1, 5)])
        self.frame_index, self.attack_cur, self.move_cur, self.idle_cur = 2, 0, 0, 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[2][self.attack_cur]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.flag, self.move_play = False, False
        self.flag_attack = 0
        self.damage = damage

    def attack(self, event):
        if event.key == pygame.K_f:
            self.attack_cur = 0
            self.flag_attack = 1

    def action_attack(self):
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
        self.death_flag, self.attack_flag = False, False

    def update(self):
        if not self.death_flag:
            attack_cooldown = 125
            self.image = self.animation_list[self.frame_index][self.cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.cur += 1

            if self.cur >= len(self.animation_list[self.frame_index]):
                self.idle()

    def idle(self):
        if not self.death_flag:
            self.frame_index, self.cur, self.update_time = 3, 0, pygame.time.get_ticks()

    def attack(self, sprite):
        if self.rect.x + 20 > sprite.rect.x or self.rect.x - 20 < sprite.rect.x:
            self.attack_flag = True
        else:
            self.attack_flag = False

    def action_attack(self):
        attack_cooldown = 125
        if self.attack_flag:
            self.image = self.animation_list[2][self.attack_cur]
            if pygame.time.get_ticks() - self.update_time > attack_cooldown:
                self.update_time = pygame.time.get_ticks()
                for i in player_sprites:
                    if self.attack_cur == len(self.animation_list[2]) - 1:
                        if pygame.sprite.collide_mask(self, i):
                            i.hp = i.hp - (self.damage - i.defense)
                            if i.hp <= 0:
                                i.death_flag = True
                                i.hp = 0
                self.attack_cur = (self.attack_cur + 1)
            if player.rect[0] < self.rect[0] and (player.rect[1] <= self.rect[1] or player.rect[1] >= self.rect[1]):
                self.rotate()
            if not player.rect[0] < self.rect[0] and not (player.rect[1] <= self.rect[1] or player.rect[1] >= self.rect[1]):
                self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if not self.death_flag:
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
            if player.rect[0] < self.rect[0] and (player.rect[1] <= self.rect[1] or player.rect[1] >= self.rect[1]):
                self.rotate()

    def dead(self):
        attack_cooldown = 125
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


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
player_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
player = Player(PLAYER_X, PLAYER_Y, MAX_HP_PLAYER, PLAYER_DAMAGE, PLAYER_DEFENSE, PLAYER_REGEN)
for _ in range(5):
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
        i.move()
        i.health()
        i.attack(player)
        if i.death_flag:
            i.dead()
    player_sprites.draw(screen)
    player.move()
    player.action_attack()

    mob_sprites.draw(screen)
    mob_sprites.update()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
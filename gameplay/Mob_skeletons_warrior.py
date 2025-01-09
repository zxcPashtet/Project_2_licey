import pygame


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
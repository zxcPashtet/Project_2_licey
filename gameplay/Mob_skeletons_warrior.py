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
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 50:
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
        if player.rect[0] < self.rect[0]:
            self.rotate()
        if not math.sqrt((player.rect.center[0] - self.rect.center[0]) ** 2 + (
                player.rect.center[1] - self.rect.center[1]) ** 2) <= 60:
            self.mask = pygame.mask.from_surface(self.image)

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
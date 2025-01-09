import pygame


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
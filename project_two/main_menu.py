import pygame
import pygame_gui
import os
import sys
import sqlite3
import cv2


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


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Main_menu')

all_sprites = pygame.sprite.Group()

manager = pygame_gui.UIManager((1600, 900))

image = pygame.transform.scale(load_image('main_menu.jpg'), (1600, 900))
screen.blit(image, (0, 0))

pygame.mixer.music.load('music\main_menu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

font = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 35)
font_enlarged = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 45)
font_smaller = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 20)
font_small = pygame.font.Font(load_font('Courier WGL4 Italic.otf'), 25)

con = sqlite3.connect('forproject2.bd')
cursor = con.cursor()
result = cursor.execute("""SELECT COUNT(*) FROM Data""").fetchone()
if result[0] == 0:
    new_game = font.render('Начать новую игру', True, (255, 255, 255))
    screen.blit(new_game, (((width // 2) - (new_game.get_width() // 2)), 550))
    how_to_play = font.render('Как играть', True, (255, 255, 255))
    screen.blit(how_to_play, (width // 2 - how_to_play.get_width() // 2, 610))
    settings = font.render('Настройки', True, (255, 255, 255))
    screen.blit(settings, (((width // 2) - (settings.get_width() // 2)), 670))
    exit = font.render('Выйти из игры', True, (255, 255, 255))
    screen.blit(exit, (((width // 2) - (exit.get_width() // 2)), 730))
else:
    new_game = font.render('Начать новую игру', True, (255, 255, 255))
    screen.blit(new_game, (((width // 2) - (new_game.get_width() // 2)), 550))
    resume = font.render('Продолжить', True, (255, 255, 255))
    screen.blit(new_game, (((width // 2) - (resume.get_width() // 2)), 610))
    how_to_play = font.render('Как играть', True, (255, 255, 255))
    screen.blit(how_to_play, (width // 2 - how_to_play.get_width() // 2, 670))
    settings = font.render('Настройки', True, (255, 255, 255))
    screen.blit(settings, (((width // 2) - (settings.get_width() // 2)), 730))
    exit = font.render('Выйти из игры', True, (255, 255, 255))
    screen.blit(exit, (((width // 2) - (exit.get_width() // 2)), 780))

def blit_main(result):
    global new_game, settings, exit, resume
    if result == 0:
        screen.blit(new_game, (((width // 2) - (new_game.get_width() // 2)), 550))
        screen.blit(how_to_play, (width // 2 - how_to_play.get_width() // 2, 610))
        screen.blit(settings, (((width // 2) - (settings.get_width() // 2)), 670))
        screen.blit(exit, (((width // 2) - (exit.get_width() // 2)), 730))
    else:
        screen.blit(new_game, (((width // 2) - (new_game.get_width() // 2)), 550))
        screen.blit(resume, (((width // 2) - (resume.get_width() // 2)), 610))
        screen.blit(how_to_play, (width // 2 - how_to_play.get_width() // 2, 670))
        screen.blit(settings, (((width // 2) - (settings.get_width() // 2)), 730))
        screen.blit(exit, (((width // 2) - (exit.get_width() // 2)), 780))


def motion_main(result):
    global new_game, settings, exit, resume, how_to_play
    if result == 0:
        if ((event.pos[0] >= ((width // 2) - (new_game.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (new_game.get_width() // 2)) + new_game.get_width()) and
                (event.pos[1] >= 550 and event.pos[1] <= 550 + new_game.get_height())):
            new_game = font_enlarged.render('Начать новую игру', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (how_to_play.get_width() // 2)) and
             event.pos[0] <= ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) and
                (event.pos[1] >= 610 and event.pos[1] <= 610 + how_to_play.get_height())):
            how_to_play = font_enlarged.render('Как играть', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (settings.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) and
                (event.pos[1] >= 670 and event.pos[1] <= 670 + settings.get_height())):
            settings = font_enlarged.render('Настройки', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (exit.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) and
                (event.pos[1] >= 730 and event.pos[1] <= 730 + exit.get_height())):
            exit = font_enlarged.render('Выйти из игры', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (new_game.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (new_game.get_width() // 2)) + new_game.get_width()) or
                (event.pos[1] < 550 or event.pos[1] > 550 + new_game.get_height())):
            new_game = font.render('Начать новую игру', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (how_to_play.get_width() // 2)) or
             event.pos[0] > ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) or
                (event.pos[1] < 610 or event.pos[1] > 610 + how_to_play.get_height())):
            how_to_play = font.render('Как играть', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (settings.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) or
                (event.pos[1] < 670 or event.pos[1] > 670 + settings.get_height())):
            settings = font.render('Настройки', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (exit.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) or
                (event.pos[1] < 730 or event.pos[1] > 730 + exit.get_height())):
            exit = font.render('Выйти из игры', True, (255, 255, 255))
    else:
        if ((event.pos[0] >= ((width // 2) - (new_game.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (new_game.get_width() // 2)) + new_game.get_width()) and
                (event.pos[1] >= 550 and event.pos[1] <= 550 + new_game.get_height())):
            new_game = font_enlarged.render('Начать новую игру', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (resume.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (resume.get_width() // 2)) + resume.get_width()) and
                (event.pos[1] >= 610 and event.pos[1] <= 610 + resume.get_height())):
            resume = font_enlarged.render('Продолжить', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (how_to_play.get_width() // 2)) and
             event.pos[0] <= ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) and
                (event.pos[1] >= 670 and event.pos[1] <= 670 + how_to_play.get_height())):
            how_to_play = font_enlarged.render('Как играть', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (settings.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) and
                (event.pos[1] >= 730 and event.pos[1] <= 730 + settings.get_height())):
            settings = font_enlarged.render('Настройки', True, (255, 255, 255))
        if ((event.pos[0] >= ((width // 2) - (exit.get_width() // 2)) and
            event.pos[0] <= ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) and
                (event.pos[1] >= 780 and event.pos[1] <= 780 + exit.get_height())):
            exit = font_enlarged.render('Выйти из игры', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (new_game.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (new_game.get_width() // 2)) + new_game.get_width()) or
                (event.pos[1] < 550 or event.pos[1] > 550 + new_game.get_height())):
            new_game = font.render('Начать новую игру', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (resume.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (resume.get_width() // 2)) + resume.get_width()) or
                (event.pos[1] < 610 or event.pos[1] > 610 + resume.get_height())):
            resume = font.render('Продолжить', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (how_to_play.get_width() // 2)) or
             event.pos[0] > ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) or
                (event.pos[1] < 670 or event.pos[1] > 670 + how_to_play.get_height())):
            how_to_play = font.render('Как играть', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (settings.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) or
                (event.pos[1] < 730 or event.pos[1] > 730 + settings.get_height())):
            settings = font.render('Настройки', True, (255, 255, 255))
        if ((event.pos[0] < ((width // 2) - (exit.get_width() // 2)) or
            event.pos[0] > ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) or
                (event.pos[1] < 780 or event.pos[1] > 780 + exit.get_height())):
            exit = font.render('Выйти из игры', True, (255, 255, 255))


def motion_new_game(event):
    global flag_rect1, flag_rect2, flag_text_complexity_normal, flag_text_complexity_hard
    if (event.pos[0] >= 456 and event.pos[0] <= 716) and (event.pos[1] >= 190 and event.pos[1] <= 450):
        flag_rect1 = True
    if (event.pos[0] >= 884 and event.pos[0] <= 1144) and (event.pos[1] >= 190 and event.pos[1] <= 450):
        flag_rect2 = True
    if (event.pos[0] < 451 or event.pos[0] > 721) or (event.pos[1] < 185 or event.pos[1] > 460):
        flag_rect1 = False
    if (event.pos[0] < 884 or event.pos[0] > 1154) or (event.pos[1] < 185 or event.pos[1] > 460):
        flag_rect2 = False

    if ((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_normal.get_width())
            and (event.pos[1] >= 673 and event.pos[1] <= 661 + text_complexity_normal.get_height())):
        flag_text_complexity_normal = True
    if ((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_hard.get_width())
            and (event.pos[1] >= 720 and event.pos[1] <= 705 + text_complexity_hard.get_height())):
        flag_text_complexity_hard = True
    if ((event.pos[0] < 456 or event.pos[0] > 456 + text_complexity_normal.get_width())
            or (event.pos[1] < 673 or event.pos[1] > 661 + text_complexity_normal.get_height())):
        flag_text_complexity_normal = False
    if ((event.pos[0] < 456 or event.pos[0] > 456 + text_complexity_hard.get_width())
            or (event.pos[1] < 720 or event.pos[1] > 705 + text_complexity_hard.get_height())):
        flag_text_complexity_hard = False


def blit_new_game(flag_rect1, flag_rect2, screen):
    global text_complexity_normal, text_complexity_hard
    if ((flag_text_complexity_normal or flag_change_text_complexity_normal) and
            flag_change_text_complexity_hard is False):
        text_complexity_normal = font_enlarged.render('Нормальная', True, (255, 255, 0))
    else:
        text_complexity_normal = font.render('Нормальная', True, (255, 255, 255))
    if (flag_text_complexity_hard or flag_change_text_complexity_hard) and flag_change_text_complexity_normal is False:
        text_complexity_hard = font_enlarged.render('Сложная', True, (255, 255, 0))
    else:
        text_complexity_hard = font.render('Сложная', True, (255, 255, 255))
    screen.blit(text_choice_name, (((width // 2) - (text_choice_name.get_width() // 2)), 20))
    screen.blit(text_class_hero, (((width // 2) - (text_class_hero.get_width() // 2)),
                                  90 + text_choice_name.get_height()))
    screen.blit(text_complexity_game, (((width // 2) - (text_complexity_game.get_width() // 2)), 620))
    screen.blit(text_knight, (456, 460))
    screen.blit(text_wizard, (880, 460))
    screen.blit(text_health, (456, 500))
    screen.blit(text_damage, (456, 520))
    screen.blit(text_protection, (456, 540))
    screen.blit(text_dexterity, (456, 560))
    screen.blit(text_health, (880, 500))
    screen.blit(text_damage, (880, 520))
    screen.blit(text_protection, (880, 540))
    screen.blit(text_dexterity, (880, 560))
    screen.blit(text_complexity_normal, (456, 670))
    screen.blit(text_complexity_hard, (456, 720))
    screen.blit(text_error, (0, 900 - text_error.get_height()))
    screen.blit(enter, (1343, 5))
    screen.blit(esc, (220, 5))
    screen.blit(text_next, (1430, 75 // 2 - text_next.get_height() // 2 + 5))
    screen.blit(text_back, (0, 75 // 2 - text_back.get_height() // 2 + 5))
    if (flag_rect1 or flag_change_rect1) and flag_change_rect2 is False:
        rect_1 = pygame.draw.rect(screen, (255, 255, 0), (451, 185, 270, 270), 5)
    else:
        rect_1 = pygame.draw.rect(screen, (255, 255, 255), (456, 190, 260, 260), 5)
    if (flag_rect2 or flag_change_rect2) and flag_change_rect1 is False:
        rect_2 = pygame.draw.rect(screen, (255, 255, 0), (879, 185, 270, 270), 5)
    else:
        rect_2 = pygame.draw.rect(screen, (255, 255, 255), (884, 190, 260, 260), 5)


def down_new_game(event):
    global flag_change_rect2, flag_change_rect1, rasa, flag_change_text_complexity_normal,\
        flag_change_text_complexity_hard, complexity
    if ((event.pos[0] >= 456 and event.pos[0] <= 716) and (event.pos[1] >= 190 and event.pos[1] <= 450) and
            flag_change_rect1 is False):
        flag_change_rect1 = True
        flag_change_rect2 = False
        rasa = 'knight'
    elif ((event.pos[0] >= 451 and event.pos[0] <= 721) and (event.pos[1] >= 185 and event.pos[1] <= 460) and
          flag_change_rect1 is True):
        flag_change_rect1 = False
        rasa = None
    if ((event.pos[0] >= 884 and event.pos[0] <= 1144) and (event.pos[1] >= 190 and event.pos[1] <= 450) and
            flag_change_rect2 is False):
        flag_change_rect2 = True
        flag_change_rect1 = False
        rasa = 'wizard'
    elif ((event.pos[0] >= 884 and event.pos[0] <= 1154) and (event.pos[1] >= 185 and event.pos[1] <= 460) and
          flag_change_rect2 is True):
        flag_change_rect2 = False
        rasa = None

    if (((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_normal.get_width())
            and (event.pos[1] >= 673 and event.pos[1] <= 661 + text_complexity_normal.get_height())) and
            flag_change_text_complexity_normal is False):
        flag_change_text_complexity_normal = True
        flag_change_text_complexity_hard = False
        complexity = 'normal'
    elif (((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_normal.get_width())
            and (event.pos[1] >= 673 and event.pos[1] <= 661 + text_complexity_normal.get_height())) and
          flag_change_text_complexity_normal is True):
        flag_change_text_complexity_normal = False
        complexity = None
    if (((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_hard.get_width())
            and (event.pos[1] >= 720 and event.pos[1] <= 705 + text_complexity_hard.get_height())) and
            flag_change_text_complexity_hard is False):
        flag_change_text_complexity_hard = True
        flag_change_text_complexity_normal = False
        complexity = 'hard'
    elif (((event.pos[0] >= 456 and event.pos[0] <= 456 + text_complexity_hard.get_width())
            and (event.pos[1] >= 720 and event.pos[1] <= 705 + text_complexity_hard.get_height())) and
          flag_change_text_complexity_hard is True):
        flag_change_text_complexity_hard = False
        complexity = None


def blit_settings():
    screen.blit(text_back, (0, 75 // 2 - text_back.get_height() // 2 + 5))
    screen.blit(esc, (220, 5))
    screen.blit(text_sounds, (width // 2 - text_sounds.get_width() // 2, 20))
    line_sounds_main_menu = pygame.draw.line(screen, (255, 255, 255), (width // 2 - 200, 120),
                                             (width // 2 + 200, 120), 5)
    line_sounds_in_game = pygame.draw.line(screen, (255, 255, 255), (width // 2 - 200, 200),
                                           (width // 2 + 200, 200), 5)
    line_sounds_effects = pygame.draw.line(screen, (255, 255, 255), (width // 2 - 200, 280),
                                           (width // 2 + 200, 280), 5)
    screen.blit(text_sounds_main_menu, (1020, 107))
    screen.blit(text_sounds_in_game, (1020, 187))
    screen.blit(text_sounds_effects, (1020, 267))
    if flag_change_sound_main_menu is False and flag_rect_main_menu is False:
        rect_sounds_main_menu = pygame.draw.rect(screen, (255, 255, 255),
                                                 (400 // 100 * meaning_main * 100 + 600, 105, 10, 30))
    else:
        rect_sounds_main_menu = pygame.draw.rect(screen, (255, 255, 0),
                                                 (400 // 100 * meaning_main * 100 + 600, 105, 10, 30))
    if flag_change_sound_in_game is False and flag_rect_in_game is False:
        rect_sounds_in_game = pygame.draw.rect(screen, (255, 255, 255),
                                               (400 // 100 * meaning_in_game * 100 + 600, 185, 10, 30))
    else:
        rect_sounds_in_game = pygame.draw.rect(screen, (255, 255, 0),
                                               (400 // 100 * meaning_in_game * 100 + 600, 185, 10, 30))
    if flag_change_sound_effects is False and flag_rect_effects is False:
        rect_sounds_effects = pygame.draw.rect(screen, (255, 255, 255),
                                               (400 // 100 * meaning_effects * 100 + 600, 265, 10, 30))
    else:
        rect_sounds_effects = pygame.draw.rect(screen, (255, 255, 0),
                                               (400 // 100 * meaning_effects * 100 + 600, 265, 10, 30))
    screen.blit(text_meaning_sounds_main_menu, (505, 107))
    screen.blit(text_meaning_sounds_in_game, (505, 187))
    screen.blit(text_meaning_sounds_effects, (505, 267))
    screen.blit(text_choice_cursor, (width // 2 - text_choice_cursor.get_width() // 2, 340))
    if flag_choice_cursor != 'defoult_cursor.png':
        rect_cursor_defoult = pygame.draw.rect(screen, (255, 255, 255),
                                               (width // 2 - 50, 415, 100, 100), 5)
    elif flag_choice_cursor == 'defoult_cursor.png':
        rect_cursor_defoult = pygame.draw.rect(screen, (255, 255, 0),
                                               (width // 2 - 50, 415, 100, 100), 5)
    if flag_choice_cursor != 'sword.gif':
        rect_cursor_sword = pygame.draw.rect(screen, (255, 255, 255),
                                             (width // 2 - 200, 415, 100, 100), 5)
    elif flag_choice_cursor == 'sword.gif':
        rect_cursor_sword = pygame.draw.rect(screen, (255, 255, 0),
                                             (width // 2 - 200, 415, 100, 100), 5)
    if flag_choice_cursor != 'stick.png':
        rect_cursor_stick = pygame.draw.rect(screen, (255, 255, 255),
                                             (width // 2 + 100, 415, 100, 100), 5)
    elif flag_choice_cursor == 'stick.png':
        rect_cursor_stick = pygame.draw.rect(screen, (255, 255, 0),
                                             (width // 2 + 100, 415, 100, 100), 5)
    screen.blit(img_cursor_defoult, (width // 2 - 25, 440))
    screen.blit(img_cursor_sword, (width // 2 - 180, 435))
    screen.blit(img_cursor_stick, (width // 2 + 125, 435))


def down_settings(event):
    global flag_change_sound_in_game, flag_change_sound_effects, flag_change_sound_main_menu, \
        meaning_main, meaning_in_game, meaning_effects, text_meaning_sounds_effects, text_meaning_sounds_in_game, \
        text_meaning_sounds_main_menu, flag_choice_cursor
    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 105 and event.pos[1] <= 135) and
            pygame.mouse.get_pressed()[0] is True):
        flag_change_sound_main_menu = True
        meaning_main = (event.pos[0] - 5 - 600) / 400
    else:
        flag_change_sound_main_menu = False
    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 185 and event.pos[1] <= 215) and
            pygame.mouse.get_pressed()[0] is True):
        flag_change_sound_in_game = True
        meaning_in_game = (event.pos[0] - 5 - 600) / 400
    else:
        flag_change_sound_in_game = False
    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 265 and event.pos[1] <= 295) and
            pygame.mouse.get_pressed()[0] is True):
        flag_change_sound_effects = True
        meaning_effects = (event.pos[0] - 5 - 600) / 400
    else:
        flag_change_sound_effects = False
    text_meaning_sounds_main_menu = font_small.render(str(abs(round(meaning_main, 1))) + ' -', True,
                                                      (255, 255, 255))
    text_meaning_sounds_in_game = font_small.render(str(abs(round(meaning_in_game, 1))) + ' -', True,
                                                    (255, 255, 255))
    text_meaning_sounds_effects = font_small.render(str(abs(round(meaning_effects, 1))) + ' -', True,
                                                    (255, 255, 255))
    if ((event.pos[0] >= 750 and event.pos[0] <= 850) and (event.pos[1] >= 415 and event.pos[1] <= 515)):
        flag_choice_cursor = 'defoult_cursor.png'
        pygame.mouse.set_visible(True)
    if ((event.pos[0] >= 600 and event.pos[0] <= 700) and (event.pos[1] >= 415 and event.pos[1] <= 515)):
        flag_choice_cursor = 'sword.gif'
    if ((event.pos[0] >= 900 and event.pos[0] <= 1000) and (event.pos[1] >= 415 and event.pos[1] <= 515)):
        flag_choice_cursor = 'stick.png'


def motion_settings(event):
    global meaning_main, meaning_in_game, meaning_effects, text_meaning_sounds_effects, text_meaning_sounds_in_game, \
        text_meaning_sounds_main_menu, flag_rect_main_menu, flag_rect_effects, flag_rect_in_game
    if flag_change_sound_main_menu:
        if (event.pos[0] >= 604 and event.pos[0] <= 996):
            meaning_main = (event.pos[0] - 5 - 600) / 400
        else:
            if event.pos[0] < 604:
                meaning_main = 0.0
            if event.pos[0] > 996:
                meaning_main = 1.0
        text_meaning_sounds_main_menu = font_small.render(str(abs(round(meaning_main, 1))) + ' -', True,
                                                          (255, 255, 255))
    if flag_change_sound_in_game:
        if (event.pos[0] >= 604 and event.pos[0] <= 996):
            meaning_in_game = (event.pos[0] - 5 - 600) / 400
        else:
            if event.pos[0] < 604:
                meaning_in_game = 0.0
            if event.pos[0] > 996:
                meaning_in_game = 1.0
        text_meaning_sounds_in_game = font_small.render(str(abs(round(meaning_in_game, 1))) + ' -', True,
                                                        (255, 255, 255))
    if flag_change_sound_effects:
        if (event.pos[0] >= 604 and event.pos[0] <= 996):
            meaning_effects = (event.pos[0] - 5 - 600) / 400
        else:
            if event.pos[0] < 604:
                meaning_effects = 0.0
            if event.pos[0] > 996:
                meaning_effects = 1.0
        text_meaning_sounds_effects = font_small.render(str(abs(round(meaning_effects, 1))) + ' -', True,
                                                        (255, 255, 255))

    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 105 and event.pos[1] <= 135)):
        flag_rect_main_menu = True
    else:
        flag_rect_main_menu = False
    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 185 and event.pos[1] <= 215)):
        flag_rect_in_game = True
    else:
        flag_rect_in_game = False
    if ((event.pos[0] >= 604 and event.pos[0] <= 996) and (event.pos[1] >= 265 and event.pos[1] <= 295)):
        flag_rect_effects = True
    else:
        flag_rect_effects = False


def blit_how_to_play():
    screen.blit(text_back, (0, 75 // 2 - text_back.get_height() // 2 + 5))
    screen.blit(esc, (220, 5))
    screen.blit(text_management, (width // 2 - text_management.get_width() // 2, 20))
    screen.blit(text_wasd, (width // 2 - text_movement.get_width() // 2 - text_wasd.get_width() // 2, 80))
    screen.blit(text_movement, (width // 2 - text_movement.get_width() // 2 + text_wasd.get_width() // 2 + 20, 85))
    screen.blit(text_f, (width // 2 - text_movement.get_width() // 2 - text_wasd.get_width() // 2, 130))
    screen.blit(text_hit, (width // 2 - text_movement.get_width() // 2 -
                                text_wasd.get_width() // 2 + text_f.get_width() + 10, 135))


class Knight(pygame.sprite.Sprite):
    def __init__(self):
        global rect_1, rect_2
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.frames = []
        for i in range(1, 5):
            self.frames.append(pygame.transform.scale(load_image('knight_idle\idle' + str(i) + '.png'),
                                                      (43 * 3, 64 * 3)))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = 456 + 260 // 2 - self.image.get_width() // 2, 190 + 260 // 2 - self.image.height // 2


    def update(self):
        global cout_knight
        if cout_knight == 8:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (43 * 3, 64 * 3))
            cout_knight = 0
        else:
            cout_knight += 1


class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        global rect_1, rect_2
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.frames = []
        for i in range(1, 9):
            self.frames.append(pygame.transform.scale(load_image('wizard_idle\idle' + str(i) + '.png'),
                                                      (43 * 3, 64 * 3)))
        self.cur_frame = 0
        self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
        self.rect = 884 + 260 // 2 - self.image.get_width() // 2, 190 + 260 // 2 - self.image.height // 2


    def update(self):
        global cout_wizard
        if cout_wizard == 8:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.flip(pygame.transform.scale(self.frames[self.cur_frame],
                                                                      (43 * 3, 64 * 3)), True, False)
            cout_wizard = 0
        else:
            cout_wizard += 1


def motion_cursor(x, y):
    if pygame.mouse.get_focused():
        if flag_choice_cursor == 'defoult_cursor':
            pass
        if flag_choice_cursor == 'sword.gif':
            pygame.mouse.set_visible(False)
            image = pygame.transform.scale(load_image(flag_choice_cursor), (34, 34))
            screen.blit(image, (x, y))
        if flag_choice_cursor == 'stick.png':
            pygame.mouse.set_visible(False)
            image = pygame.transform.scale(load_image(flag_choice_cursor), (34, 42))
            screen.blit(image, (x, y))


clock = pygame.time.Clock()
cout_knight = 0
cout_wizard = 0
name_hero = ''
meaning_main = 0.2
meaning_in_game = 0.5
meaning_effects = 0.5
last_x_sound_main_menu = 0
last_x_sound_in_game = 0
last_x_sound_effects = 0
rasa = None
complexity = None
running = True
flag_new_game = False
flag_play = False
flag_settings = False
flag_main = True
flag_how_to_play = False
flag_rect1 = False
flag_rect2 = False
flag_change_rect1 = False
flag_change_rect2 = False
flag_text_complexity_normal = False
flag_text_complexity_hard = False
flag_change_text_complexity_normal = False
flag_change_text_complexity_hard = False
flag_change_sound_main_menu = False
flag_change_sound_in_game = False
flag_change_sound_effects = False
flag_rect_main_menu = False
flag_rect_in_game = False
flag_rect_effects = False
flag_choice_cursor = 'defoult_cursor.png'
cap = cv2.VideoCapture('menu_video.mp4')
success, img = cap.read()
shape = (1600, 900)
while running:
    pygame.mixer.music.set_volume(meaning_main)
    success, img = cap.read()
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if flag_main:
            if event.type == pygame.MOUSEMOTION:
                motion_main(result[0])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (((event.pos[0] >= ((width // 2) - (exit.get_width() // 2)) and
                        event.pos[0] <= ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) and
                        (event.pos[1] >= 730 and event.pos[1] <= 730 + exit.get_height()) and result[0] == 0) or
                        ((event.pos[0] >= ((width // 2) - (exit.get_width() // 2)) and
                          event.pos[0] <= ((width // 2) - (exit.get_width() // 2)) + exit.get_width()) and
                         (event.pos[1] >= 780 and event.pos[1] <= 780 + exit.get_height()) and result[0] != 0)):
                    running = False
                if ((event.pos[0] >= ((width // 2) - (new_game.get_width() // 2)) and
                    event.pos[0] <= ((width // 2) - (new_game.get_width() // 2)) + new_game.get_width()) and
                        (event.pos[1] >= 550 and event.pos[1] <= 550 + new_game.get_height())):
                    flag_main = False
                    flag_new_game = True
                    text_choice_name = font.render('Введите имя для своего персонажа', True,
                                                   (255, 255, 255))
                    text_class_hero = font.render('Выберите класс своего героя', True,
                                                  (255, 255, 255))
                    text_complexity_game = font.render('Выберите сложность игры', True,
                                                       (255, 255, 255))
                    text_knight = font.render('Рыцарь', True, (255, 255, 255))
                    text_wizard = font.render('Волшебник', True, (255, 255, 255))
                    text_health = font_smaller.render('Здоровье', True, (255, 255, 255))
                    text_damage = font_smaller.render('Урон', True, (255, 255, 255))
                    text_protection = font_smaller.render('Защита', True, (255, 255, 255))
                    text_dexterity = font_smaller.render('Ловкость', True, (255, 255, 255))
                    text_complexity_normal = font.render('Нормальная', True, (255, 255, 255))
                    text_complexity_hard = font.render('Сложная', True, (255, 255, 255))
                    text_back = font_smaller.render('Вернуться назад -', True, (255, 255, 255))
                    text_next = font_smaller.render('- Начать игру', True, (255, 255, 255))
                    text_error = font_smaller.render('', True, (255, 0, 0))
                    enter = pygame.transform.scale(load_image('enter_white.png'), (75, 75))
                    esc = pygame.transform.scale(load_image('esc_white.png'), (75, 75))
                    entry = pygame_gui.elements.UITextEntryLine(
                        relative_rect=pygame.Rect((width // 2 - text_choice_name.get_width() // 2, 60),
                                                  (text_choice_name.get_size())),
                        manager=manager)
                    entry.set_text(name_hero)
                    knight = Knight()
                    wizard = Wizard()

                if (((event.pos[0] >= ((width // 2) - (settings.get_width() // 2))) and
                     (event.pos[0] <= ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) and
                      (event.pos[1] >= 670 and event.pos[1] <= 670 + settings.get_height()) and result[0] == 0) or
                        ((event.pos[0] >= ((width // 2) - (settings.get_width() // 2))) and
                         (event.pos[0] <= ((width // 2) - (settings.get_width() // 2)) + settings.get_width()) and
                          (event.pos[1] >= 730 and event.pos[1] <= 730 + settings.get_height()) and result[0] != 0)):
                    flag_main = False
                    flag_settings = True
                    esc = pygame.transform.scale(load_image('esc_white.png'), (75, 75))
                    text_back = font_smaller.render('Вернуться назад -', True, (255, 255, 255))
                    text_sounds = font.render('Звуки', True, (255, 255, 255))
                    line_sounds_main_menu = pygame.draw.line(
                        screen, (255, 255, 255), (width // 2 - 200, 120),
                        (width // 2 + 200, 120), 5)
                    line_sounds_in_game = pygame.draw.line(
                        screen, (255, 255, 255), (width // 2 - 200, 180),
                        (width // 2 + 200, 180), 5)
                    line_sounds_effects = pygame.draw.line(
                        screen, (255, 255, 255), (width // 2 - 200, 260),
                        (width // 2 + 200, 260), 5)
                    text_sounds_main_menu = font_small.render('- Громкость музыки в главном меню',
                                                              True, (255, 255, 255))
                    text_sounds_in_game = font_small.render('- Громкость музыки в игре',
                                                            True, (255, 255, 255))
                    text_sounds_effects = font_small.render('- Громкость эффектов',
                                                            True, (255, 255, 255))
                    rect_sounds_main_menu = pygame.draw.rect(screen, (255, 255, 255),
                                                             (int(400 // 100 * meaning_main * 100) + 600,
                                                              105, 10, 30))
                    rect_sounds_in_game = pygame.draw.rect(screen, (255, 255, 255),
                                                           (int(400 // 100 * meaning_in_game * 100) + 600,
                                                            185, 10, 30))
                    rect_sounds_effects = pygame.draw.rect(screen, (255, 255, 255),
                                                           (int(400 // 100 * meaning_effects * 100) + 600,
                                                            265, 10, 30))
                    last_x_sound_main_menu = rect_sounds_main_menu.x
                    last_x_sound_in_game = rect_sounds_in_game.x
                    last_x_sound_effects = rect_sounds_effects.x
                    text_meaning_sounds_main_menu = font_small.render(
                        str(abs(round(meaning_main, 1))) + ' -', True,
                        (255, 255, 255))
                    text_meaning_sounds_in_game = font_small.render(
                        str(abs(round(meaning_in_game, 1))) + ' -', True,
                        (255, 255, 255))
                    text_meaning_sounds_effects = font_small.render(
                        str(abs(round(meaning_effects, 1))) + ' -', True,
                        (255, 255, 255))
                    text_choice_cursor = font.render('Выберите курсор мыши', True, (255, 255, 255))
                    img_cursor_defoult = pygame.transform.scale(load_image('defoult_cursor.png'), (50, 50))
                    img_cursor_sword = pygame.transform.scale(load_image('sword.gif'), (60, 60))
                    img_cursor_stick = pygame.transform.scale(load_image('stick.png'), (49, 60))

                if (((event.pos[0] >= ((width // 2) - (how_to_play.get_width() // 2))) and
                     (event.pos[0] <= ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) and
                        (event.pos[1] >= 610 and event.pos[1] <= 610 + how_to_play.get_height()) and result[0] == 0) or
                        ((event.pos[0] >= ((width // 2) - (how_to_play.get_width() // 2))) and
                         (event.pos[0] <= ((width // 2) - (how_to_play.get_width() // 2)) + how_to_play.get_width()) and
                         (event.pos[1] >= 670 and event.pos[1] <= 670 + how_to_play.get_height()) and result[0] != 0)):
                    flag_main = False
                    flag_how_to_play = True
                    esc = pygame.transform.scale(load_image('esc_white.png'), (75, 75))
                    text_back = font_smaller.render('Вернуться назад -', True, (255, 255, 255))
                    text_management = font.render('Управление', True, (255, 255, 255))
                    text_movement = font_small.render('- Передвижение персонажа', True, (255, 255, 255))
                    text_hit = font_small.render('- Обычная атака', True, (255, 255, 255))
                    text_wasd = font.render('W, A, S, D', True, (255, 255, 255))
                    text_f = font.render('F', True, (255, 255, 255))

        if flag_new_game:
            if event.type == pygame.MOUSEMOTION:
                motion_new_game(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                down_new_game(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag_main = True
                    flag_new_game = False
                    entry.hide()
                    all_sprites.empty()
                if event.key == pygame.K_RETURN:
                    if rasa is not None and complexity is not None and name_hero.split() != []:
                        text_error = font_smaller.render('', True, (255, 0, 0))
                    else:
                        if complexity is None:
                            text_error = font_smaller.render('Выберите сложность игры', True,
                                                             (255, 0, 0))
                        if rasa is None:
                            text_error = font_smaller.render('Выберите расу своего героя', True,
                                                             (255, 0, 0))
                        if name_hero.split() == []:
                            text_error = font_smaller.render('Введите имя вашего героя', True,
                                                             (255, 0, 0))

        if flag_settings:
            if event.type == pygame.MOUSEMOTION:
                motion_settings(event)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                down_settings(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag_main = True
                    flag_settings = False

        if flag_how_to_play:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag_main = True
                    flag_how_to_play = False

        if event.type == pygame.MOUSEMOTION:
            x_cursor = event.pos[0]
            y_cursor = event.pos[1]

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                name_hero = event.text
        manager.process_events(event)
    manager.update(time_delta)
    try:
        screen.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
        #screen.blit(image, (0, 0))
    except AttributeError:
        cap = cv2.VideoCapture('menu_video.mp4')
    all_sprites.draw(screen)
    all_sprites.update()

    if flag_main:
        blit_main(result[0])

    if flag_new_game:
        blit_new_game(flag_rect1, flag_rect2, screen)

    if flag_how_to_play:
        blit_how_to_play()

    if flag_settings:
        blit_settings()

    motion_cursor(x_cursor, y_cursor)

    manager.draw_ui(screen)
    pygame.display.update()
    clock.tick(120)
con.close()
pygame.quit()
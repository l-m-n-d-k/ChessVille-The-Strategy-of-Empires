import pygame
import os
import sys
from constants import *


def load_image(name, directory='Фото персонажей', colorkey=None):
    fullname = os.path.join(directory, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


images = {
    7: pygame.transform.scale(load_image('Холм.png'), (100, 100)),
    8: pygame.transform.scale(load_image('Поле с речкой.png'), (100, 100)),
    9: pygame.transform.scale(load_image('Поле.png'), (100, 100)),
    10: pygame.transform.scale(load_image('Гора.png'), (100, 100)),
    11: load_image('Туман войны.jpg'),
    12: load_image('Разбойник 1.jpg', colorkey=-1),
    13: load_image('Разбойник 2.jpg', colorkey=-1),
    'курсор': load_image("arrow.png"),
    'иконка 1': load_image('Иконка 1.jpg'),
    'иконка 2': load_image('Иконка 2.jpg', colorkey=-1),
    'иконка 3': load_image('Иконка 2.jpg', colorkey=-1),
    'миникарта': load_image('Миникарта.png', 'data', -1),
    'кнопка характеристик': load_image('Кнопка характеристик.png', 'data', -1),
    'кнопка ожидания': load_image('Кнопка ожидания.png', 'data', -1),
    'кнопка юнит ждёт': load_image('Ожидание приказа.png', 'data', -1),
    'кнопка ок': load_image('Кнопка ок.png', 'data', -1),
    'кнопка удалить': load_image('Кнопка удалить.png', 'data', -1),
    'следующий ход': load_image('Следующий ход.png', 'data', -1),
    'зажатая кнопка ожидания': load_image('Зажатая кнопка ожидания.png', 'data', -1),
    'зажатая кнопка характеристик': load_image('Зажатая кнопка характеристик.png', 'data', -1),
    'зажатое ожидание приказа': load_image('Зажатое ожидание приказа.png', 'data', -1),
    'зажатый следующий ход': load_image('Зажатый следующий ход.png', 'data', -1),
    'табличка характеристик': load_image('Табличка характеристик.png', 'data').subsurface((0, 0, 328, 148)),
    'таймер анимашка': pygame.transform.scale(load_image('Анимация таймера.png', 'data', -1), (400, 100)),
    'пауза': pygame.transform.scale(load_image('settings.png', 'data'), (75, 75)),
    'окошко кратких характеристик': pygame.transform.scale(load_image('Окошко кратких характеристик.PNG', 'data'), (280, 334)).subsurface(4, 4, 274, 326),
    'король белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 0, 64 * 1, 64, 64)),
    'ферзь белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 1, 64 * 1, 64, 64)),
    'ладья белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 2, 64 * 1, 64, 64)),
    'конь белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 3, 64 * 1, 64, 64)),
    'слон белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 4, 64 * 1, 64, 64)),
    'пешка белые': load_image('Шахматные фигуры 2д.png').subsurface((64 * 5, 64 * 1, 64, 64)),
    'король чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 0, 64 * 0, 64, 64)),
    'ферзь чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 1, 64 * 0, 64, 64)),
    'ладья чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 2, 64 * 0, 64, 64)),
    'конь чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 3, 64 * 0, 64, 64)),
    'слон чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 4, 64 * 0, 64, 64)),
    'пешка чёрные': load_image('Шахматные фигуры 2д.png').subsurface((64 * 5, 64 * 0, 64, 64)),
    'окошко поражения': pygame.transform.scale(load_image('Окошко поражения.png', 'data'), (750, 470)),
    'окошко победы': load_image('Окошко победы.png', 'data'),
    'красный крест': load_image('Красный крест.jpg', 'data', -1),
    'Герой 1': load_image("Герой 1.png"),
    'Герой 2': load_image("Герой 2.png"),
    'Герой 3': load_image("Герой 3.png"),
    'Герой 1 иконка': load_image("Герой 1 иконка.png"),
    'Герой 2 иконка': load_image("Герой 2 иконка.png"),
    'Герой 3 иконка': load_image("Герой 3 иконка.png"),
    'Герой 4': load_image("Герой 4.png"),
    'Герой 5': load_image("Герой 5.png"),
    'Герой 6': load_image("Герой 6.png"),
    'Герой 4 иконка': load_image("Герой 4 иконка.png"),
    'Герой 5 иконка': load_image("Герой 5 иконка.png"),
    'Герой 6 иконка': load_image("Герой 6 иконка.png"),
    'Нейтральный юнит 12': load_image("Нейтральный юнит 12.png"),
    'Нейтральный юнит 13': load_image("Нейтральный юнит 13.png"),
    'Место для таймера': pygame.transform.smoothscale(load_image("Место под таймер.png", directory='data'), (100, 60)),
}

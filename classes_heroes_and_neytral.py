import pygame
from copy import deepcopy
from groups_sprites import players_group1, players_group2, neytral_group, all_sprites
from sprites_images import images
from constants import *


class Players1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(players_group1, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()
        self.tip = tile_type
        self.army = {'Король': 1,
                     'Ферзь': 0,
                     'Ладья': 0,
                     'Слон': 0,
                     'Конь': 0,
                     'Пешка': 0}
        if self.tip == 1:
            self.army['Конь'] = 2
            self.army['Пешка'] = 4
        elif self.tip == 2:
            self.army['Ладья'] = 2
            self.army['Пешка'] = 5
        elif self.tip == 3:
            self.army['Слон'] = 2
            self.army['Пешка'] = 4
        self.steps = 0
        self.board = [[None for _1 in range(map_width)] for _2 in range(map_height)]

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y, mapa):
        self.pos = pos_x, pos_y
        self._define_rect()
        self.update_board(mapa)

    def update_steps(self):
        if self.tip in (2, 5):
            self.steps = 6
        elif self.tip in (1, 3, 4, 6):
            self.steps = 4

    def update_board(self, mapa):
        board = [[[None, '', '', '']] * map_width for _ in range(map_height)]
        for y in range(map_height):
            for x in range(map_width):
                if mapa.fon[y][x] == 9:
                    board[y][x] = [None, "Поле"]
                elif mapa.fon[y][x] == 10:
                    board[y][x] = [None, "Гора"]
                elif mapa.fon[y][x] == 7:
                    board[y][x] = [None, "Холм"]
                elif mapa.fon[y][x] == 8:
                    board[y][x] = [None, "Река"]

                if mapa.neytral[y][x] in (12, 13):
                    board[y][x].append('Нейтрал')
                elif mapa.players[y][x] in (4, 5, 6):
                    board[y][x].append('Вражеский герой')
                elif mapa.players[y][x] in (1, 2, 3):
                    board[y][x].append('Союзный герой')
                elif mapa.players[y][x] == 0:
                    board[y][x].append('Пусто')

                if mapa.tyman1[y][x] == 11:
                    board[y][x].append('Туман')
                elif mapa.tyman1[y][x] == 0:
                    board[y][x].append('Тумана нет')

        board[self.pos[1]][self.pos[0]] = [0, 'Моя позция', 'Я', 'Тумана нет']

        steps = {'Поле': 1,
                 'Холм': 2,
                 'Река': 2,
                 'Моя позция': 0,
                 'Нейтрал': 2,
                 'Вражеский герой': 2,
                 'Пусто': 0,
                 'Я': 0}

        if self.tip in (1, 4):
            steps['Холм'] = 1
        elif self.tip in (3, 6):
            steps['Река'] = 1

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if abs(self.pos[1] - y) <= 8 and abs(self.pos[0] - x) <= 8 and ceil1[0] is None and ceil1[
                        1] != 'Гора' and ceil1[2] not in ('Я', 'Союзный герой') and ceil1[3] != 'Туман':
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            board_copy[y][x] = [optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]], *ceil1[1:]]
                            c += 1
                        else:
                            pass
            board = deepcopy(board_copy)

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if ceil1[0]:
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            numb = optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]]
                            if numb != ceil1[0]:
                                board_copy[y][x] = [numb, *ceil1[1:]]
                                c += 1
                        else:
                            pass
            board = deepcopy(board_copy)

        self.board = deepcopy(board)


class Players2(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(players_group2, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()
        self.tip = tile_type
        self.army = {'Король': 1,
                     'Ферзь': 0,
                     'Ладья': 0,
                     'Слон': 0,
                     'Конь': 0,
                     'Пешка': 0}
        if self.tip == 4:
            self.army['Конь'] = 2
            self.army['Пешка'] = 4
        elif self.tip == 5:
            self.army['Ладья'] = 2
            self.army['Пешка'] = 5
        elif self.tip == 6:
            self.army['Слон'] = 2
            self.army['Пешка'] = 4
        self.steps = 0
        self.board = [[None for _1 in range(map_width)] for _2 in range(map_height)]

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y, mapa):
        self.pos = pos_x, pos_y
        self._define_rect()
        self.update_board(mapa)

    def update_steps(self):
        if self.tip in (2, 5):
            self.steps = 6
        elif self.tip in (1, 3, 4, 6):
            self.steps = 4

    def update_board(self, mapa):
        board = [[[None, '', '', '', '']] * map_width for _ in range(map_height)]
        for y in range(map_height):
            for x in range(map_width):
                if mapa.fon[y][x] == 9:
                    board[y][x] = [None, "Поле"]
                elif mapa.fon[y][x] == 10:
                    board[y][x] = [None, "Гора"]
                elif mapa.fon[y][x] == 7:
                    board[y][x] = [None, "Холм"]
                elif mapa.fon[y][x] == 8:
                    board[y][x] = [None, "Река"]

                if mapa.neytral[y][x] in (12, 13):
                    board[y][x].append('Нейтрал')
                elif mapa.players[y][x] in (1, 2, 3):
                    board[y][x].append('Вражеский герой')
                elif mapa.players[y][x] in (4, 5, 6):
                    board[y][x].append('Союзный герой')
                elif mapa.players[y][x] == 0:
                    board[y][x].append('Пусто')

                if mapa.tyman2[y][x] == 11:
                    board[y][x].append('Туман')
                elif mapa.tyman2[y][x] == 0:
                    board[y][x].append('Тумана нет')

        board[self.pos[1]][self.pos[0]] = [0, 'Моя позция', 'Я', 'Тумана нет']

        steps = {'Поле': 1,
                 'Холм': 2,
                 'Река': 2,
                 'Моя позция': 0,
                 'Нейтрал': 2,
                 'Вражеский герой': 2,
                 'Пусто': 0,
                 'Я': 0}

        if self.tip in (1, 4):
            steps['Холм'] = 1
        elif self.tip in (3, 6):
            steps['Река'] = 1

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if abs(self.pos[1] - y) <= 8 and abs(self.pos[0] - x) <= 8 and ceil1[0] is None and ceil1[
                        1] != 'Гора' and ceil1[2] not in ('Я', 'Союзный герой') and ceil1[3] != 'Туман':
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            board_copy[y][x] = [optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]], *ceil1[1:]]
                            c += 1
                        else:
                            pass
            board = deepcopy(board_copy)
        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if ceil1[0]:
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            numb = optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]]
                            if numb < ceil1[0]:
                                board_copy[y][x] = [numb, *ceil1[1:]]
                                c += 1
                        else:
                            pass
            board = deepcopy(board_copy)
        self.board = deepcopy(board)


class Neytral(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(neytral_group, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y):
        self.pos = pos_x, pos_y
        self._define_rect()

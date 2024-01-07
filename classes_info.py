import pygame
from copy import deepcopy
from groups_sprites import info_group, button_group, all_sprites, players_group1, players_group2
from sprites_images import images
from classes_map import Map
from constants import *


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, mapa):
        super().__init__(info_group, all_sprites)
        self.image = images['миникарта']
        self.rect = self.image.get_rect()
        self.rect.bottomright = (width + 10, height + 10)

        self.button_stats = ButtonStats(self)
        self.button_wait = ButtonWait(self)
        self.button_unit_wait = ButtonUnitWait(self)

        self.size = 308, 308
        self.otstyp = 80, 8
        self.side = self.size[0] // map_width
        self.fon = deepcopy(mapa.fon)
        self.neytral = deepcopy(mapa.neytral)
        self.tyman1 = deepcopy(mapa.tyman1)
        self.tyman2 = deepcopy(mapa.tyman2)
        self.players = deepcopy(mapa.players)

    def update(self, HOD, *args):
        for el in args:
            if isinstance(el, Map):
                mapa = el
                self.fon = deepcopy(mapa.fon)
                self.neytral = deepcopy(mapa.neytral)
                self.tyman1 = deepcopy(mapa.tyman1)
                self.tyman2 = deepcopy(mapa.tyman2)
                self.players = deepcopy(mapa.players)
        self.image = images['миникарта']
        self.rect = self.image.get_rect()
        self.rect.bottomright = (width + 8, height + 10)
        for y in range(map_height):
            for x in range(map_width):
                if HOD == 'first':
                    if self.fon[y][x] == 7:
                        pygame.draw.rect(self.image, (10, 69, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 153, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (0, 103, 126), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (100, 107, 99), (x * self.side + 80, y * self.side + 8, self.side, self.side))

                    if self.tyman1[y][x] != 0:
                        pygame.draw.rect(self.image, (200, 200, 200), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.circle(self.image, (83, 55, 122), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.circle(self.image, (175, 43, 30), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.circle(self.image, (236, 124, 38), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue

                elif HOD == 'second':
                    if self.fon[y][x] == 7:
                        pygame.draw.rect(self.image, (10, 69, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 153, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (0, 103, 126), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (100, 107, 99), (x * self.side + 80, y * self.side + 8, self.side, self.side))

                    if self.tyman2[y][x] != 0:
                        pygame.draw.rect(self.image, (200, 200, 200), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.circle(self.image, (83, 55, 122), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.circle(self.image, (175, 43, 30), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.circle(self.image, (236, 124, 38),(x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue


class ButtonStats(pygame.sprite.Sprite):
    def __init__(self, mimimapa):
        super().__init__(button_group, all_sprites)
        self.image = images['кнопка характеристик']
        self.rect = self.image.get_rect()
        self.rect.topleft = (mimimapa.rect.x + 3, mimimapa.rect.y + 202)


class ButtonWait(pygame.sprite.Sprite):
    def __init__(self, mimimapa):
        super().__init__(button_group, all_sprites)
        self.image = images['кнопка ожидания']
        self.rect = self.image.get_rect()
        self.rect.topleft = (mimimapa.rect.x + 3, mimimapa.rect.y + 260)

    def click(self, hod, icon):
        numb = icon + 1 + (3 if hod == 'second' else 0)
        for sprite in players_group1:
            if sprite.tip == numb:
                sprite.steps = 0
        for sprite in players_group2:
            if sprite.tip == numb:
                sprite.steps = 0


class ButtonUnitWait(pygame.sprite.Sprite):
    def __init__(self, mimimapa):
        super().__init__(button_group, all_sprites)
        self.image = images['кнопка юнит ждёт']
        self.rect = self.image.get_rect()
        self.rect.bottomright = (mimimapa.rect.topright[0] - 13, mimimapa.rect.topright[1])
        self.sost = 'wait'

    def upgrade(self, hod, click=False):
        if hod == 'first':
            if self.sost == 'wait':
                for sprite in sorted(players_group1, key=lambda spr: spr.tip):
                    if sprite.steps:
                        icon = sprite.tip - 1
                        hero = sprite
                        sost = 'юнит ждёт приказа'
                        break
                else:
                    icon = None
                    hero = None
                    sost = 'следующий ход'
                    self.image = images['следующий ход']
                    self.sost = 'new hod'
                return sost, hero, icon
            elif self.sost == 'new hod':
                if click:
                    self.image = images['кнопка юнит ждёт']
                    self.sost = 'wait'
                    return 'следующий ход', None, None

        elif hod == 'second':
            if self.sost == 'wait':
                for sprite in sorted(players_group2, key=lambda spr: spr.tip):
                    if sprite.steps:
                        icon = sprite.tip - 4
                        hero = sprite
                        sost = 'юнит ждёт приказа'
                        break
                else:
                    icon = None
                    hero = None
                    sost = 'следующий ход'
                    self.image = images['следующий ход']
                    self.sost = 'new hod'
                return sost, hero, icon
            elif self.sost == 'new hod':
                if click:
                    self.image = images['кнопка юнит ждёт']
                    self.sost = 'wait'
                    return 'следующий ход', None, None

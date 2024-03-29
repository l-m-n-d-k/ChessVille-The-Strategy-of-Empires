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
                        pygame.draw.rect(self.image, (0, 148, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 110, 52), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (93, 118, 203), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (71, 69, 60), (x * self.side + 80, y * self.side + 8, self.side, self.side))

                    if self.tyman1[y][x] != 0:
                        pygame.draw.rect(self.image, (180, 180, 180), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.circle(self.image, (244, 200, 0), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.circle(self.image, (195, 43, 30), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.circle(self.image, (32, 33, 79), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue

                elif HOD == 'second':
                    if self.fon[y][x] == 7:
                        pygame.draw.rect(self.image, (0, 148, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 110, 52), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (93, 118, 203), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (71, 69, 60), (x * self.side + 80, y * self.side + 8, self.side, self.side))

                    if self.tyman2[y][x] != 0:
                        pygame.draw.rect(self.image, (180, 180, 180), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.circle(self.image, (244, 200, 0), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.circle(self.image, (195, 43, 30), (x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.circle(self.image, (32, 33, 79),(x * self.side + 80 + self.side // 2, y * self.side + 8 + self.side // 2), self.side // 2)
                        continue

    def update_select(self, event):
        if self.button_wait.rect.collidepoint(event.pos):
            self.button_wait.image = images['зажатая кнопка ожидания']
        else:
            self.button_wait.image = images['кнопка ожидания']
        if self.button_stats.rect.collidepoint(event.pos):
            self.button_stats.image = images['зажатая кнопка характеристик']
        else:
            self.button_stats.image = images['кнопка характеристик']
        if self.button_unit_wait.rect.collidepoint(event.pos):
            if self.button_unit_wait.sost == 'new hod':
                self.button_unit_wait.image = images['зажатый следующий ход']
            else:
                self.button_unit_wait.image = images['зажатое ожидание приказа']
        else:
            if self.button_unit_wait.sost == 'new hod':
                self.button_unit_wait.image = images['следующий ход']
            else:
                self.button_unit_wait.image = images['кнопка юнит ждёт']


class ButtonStats(pygame.sprite.Sprite):
    def __init__(self, mimimapa):
        super().__init__(info_group, all_sprites)
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
        super().__init__(info_group, all_sprites)
        self.image = images['кнопка юнит ждёт']
        self.rect = self.image.get_rect()
        self.rect.bottomright = (mimimapa.rect.topright[0] - 13, mimimapa.rect.topright[1])
        self.sost = 'wait'

    def upgrade(self, hod, click=False):
        if hod == 'first':
            if self.sost == 'wait':
                for sprite in sorted(players_group1, key=lambda spr: spr.tip):
                    if sprite.steps and sprite.live:
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
                    if sprite.steps and sprite.live:
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


class TableSteps(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(info_group, all_sprites)
        self.image = images['табличка характеристик']
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 0, height

    def update_stats(self, hod, icon):
        self.image = images['табличка характеристик'].copy()
        numb = icon + 1 + (3 if hod == 'second' else 0)
        my_hero = None
        for sprite in players_group1:
            if sprite.tip == numb:
                my_hero = sprite
        for sprite in players_group2:
            if sprite.tip == numb:
                my_hero = sprite

        steps = str(my_hero.steps)
        max_steps = str(6 if numb in (2, 5) else 4)
        strong = str(sum(my_hero.army[key] * ceil[key] for key in my_hero.army))
        image = my_hero.icon

        font = pygame.font.Font(None, 30)
        text1 = font.render(steps, True, (250, 250, 250))
        text2 = font.render(max_steps, True, (250, 250, 250))
        text3 = font.render(strong, True, (250, 250, 250))

        self.image.blit(pygame.transform.scale(image, (80, 100)), (10, 35))
        self.image.blit(text1, (250, 72))
        self.image.blit(text2, (270, 72))
        self.image.blit(text3, (255, 97))

import pygame
from copy import deepcopy
from groups_sprites import info_group, all_sprites
from sprites_images import images
from classes_map import Map
from constants import *


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, mapa):
        super().__init__(info_group, all_sprites)
        self.image = images['миникарта']
        self.rect = self.image.get_rect()
        self.rect.bottomright = (width, height)
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
        self.rect.bottomright = (width, height)
        for y in range(map_height):
            for x in range(map_width):
                if HOD == 'first':
                    if self.tyman1[y][x] != 0:
                        pygame.draw.rect(self.image, (200, 200, 200), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.rect(self.image, (83, 55, 122), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.rect(self.image, (175, 43, 30), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.rect(self.image, (236, 124, 38), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue

                    if self.fon[y][x] == 7:
                        pygame.draw.rect(self.image, (10, 69, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 153, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (0, 103, 126), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (100, 107, 99), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                elif HOD == 'second':
                    if self.tyman2[y][x] != 0:
                        pygame.draw.rect(self.image, (200, 200, 200), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (4, 5, 6):
                        pygame.draw.rect(self.image, (83, 55, 122), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.players[y][x] in (1, 2, 3):
                        pygame.draw.rect(self.image, (175, 43, 30), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue
                    if self.neytral[y][x]:
                        pygame.draw.rect(self.image, (236, 124, 38), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                        continue

                    if self.fon[y][x] == 7:
                        pygame.draw.rect(self.image, (10, 69, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 9:
                        pygame.draw.rect(self.image, (0, 153, 0), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 8:
                        pygame.draw.rect(self.image, (0, 103, 126), (x * self.side + 80, y * self.side + 8, self.side, self.side))
                    elif self.fon[y][x] == 10:
                        pygame.draw.rect(self.image, (100, 107, 99), (x * self.side + 80, y * self.side + 8, self.side, self.side))


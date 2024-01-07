import pygame
import csv
from classes_fon_and_tyman import Tile, Tyman1, Tyman2
from classes_heroes_and_neytral import Players1, Players2, Neytral
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group, info_group, button_group
from constants import *


class Map:
    def __init__(self):
        self.ox = 30
        self.oy = 30
        with (open('many_map/Фон 1.csv') as fon, open('many_map/Нейтральные юниты 1.csv') as neytral, open(
                'many_map/Туман войны 1.csv') as tyman1, open('many_map/Игроки 1.csv') as players,
              open('many_map/Туман войны 2.csv') as tyman2):
            self.fon = [[int(elem) for elem in lst] for lst in csv.reader(fon, delimiter=',')]
            self.neytral = [[int(elem) for elem in lst] for lst in csv.reader(neytral, delimiter=',')]
            self.tyman1 = [[int(elem) for elem in lst] for lst in csv.reader(tyman1, delimiter=',')]
            self.tyman2 = [[int(elem) for elem in lst] for lst in csv.reader(tyman2, delimiter=',')]
            self.players = [[int(elem) for elem in lst] for lst in csv.reader(players, delimiter=',')]
        for y in range(self.oy):
            for x in range(self.ox):
                sprite = self.fon[y][x]
                if sprite:
                    Tile(sprite, x, y)
                sprite = self.neytral[y][x]
                if sprite:
                    Neytral(sprite, x, y)
                sprite = self.tyman1[y][x]
                if sprite:
                    Tyman1(sprite, x, y)
                sprite = self.tyman2[y][x]
                if sprite:
                    Tyman2(sprite, x, y)
                sprite = self.players[y][x]
                if sprite in (1, 2, 3):
                    Players1(sprite, x, y)
                elif sprite in (4, 5, 6):
                    Players2(sprite, x, y)

    def draw_map(self, screen, HOD):
        if HOD == 'first':
            tiles_group.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            neytral_group.draw(screen)
            tyman_group1.draw(screen)
            info_group.draw(screen)
            button_group.draw(screen)
            system_group.draw(screen)
        elif HOD == 'second':
            tiles_group.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            neytral_group.draw(screen)
            tyman_group2.draw(screen)
            info_group.draw(screen)
            button_group.draw(screen)
            system_group.draw(screen)

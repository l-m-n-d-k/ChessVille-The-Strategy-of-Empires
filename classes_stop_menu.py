import sys
import pygame
from groups_sprites import stop_menu_group
from constants import *


class Pause_fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(stop_menu_group)
        self.image =  pygame.image.load('menu/menu_in_game.png')
        self.image = pygame.transform.scale(self.image, (150*3, 225*3))
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2 - 50)

class Exit_button_pause(pygame.sprite.Sprite):
    def __init__(self, event, game_running):
        super().__init__(stop_menu_group)
        self.event = event
        self.game_running = game_running
        self.image =  pygame.image.load('menu/to_main_menu.png')
        self.image = pygame.transform.scale(self.image, (150*3, 51*3))
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2 + 100)

    def to_main_menu(self):
        if self.rect.collidepoint(self.event.pos):
            print('выход')
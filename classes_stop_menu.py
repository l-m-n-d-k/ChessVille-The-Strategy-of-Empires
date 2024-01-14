import pygame
from groups_sprites import stop_menu_group
from constants import *


class Pause_fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(stop_menu_group, window_group)
        self.image_fon =  pygame.image.load('menu/menu_in_game.png')
        self.rect = self.image_fon.get_rect()
        self.rect.center = (width / 2, height / 2 - 50)
        stop_menu_group.draw(screen)
import pygame
from groups_sprites import system_group, all_sprites
from sprites_images import images
from constants import *


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, position, player_number):
        super().__init__(system_group, all_sprites)
        image = {0: images['иконка 1'], 1: images['иконка 2'], 2: images['иконка 3']}
        self.image = image[player_number]
        self.rect = self.image.get_rect(topleft=position)
        self.numb = player_number

    def draw(self, select_icon):
        if self.numb == select_icon:
            rect = self.rect[0] - 10, self.rect[1] - 10, self.rect[2] + 20, self.rect[3] + 20
            pygame.draw.rect(screen, 'red', rect, 10)

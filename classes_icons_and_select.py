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

    def draw_base_rama(self, select_icon):
        rect = self.rect[0] - 7, self.rect[1] - 7, self.rect[2] + 14, self.rect[3] + 14
        pygame.draw.rect(screen, (78, 87, 84), rect, 7)

    def draw_select_rama(self, select_icon):
        if self.numb == select_icon:
            rect = self.rect[0] - 7, self.rect[1] - 7, self.rect[2] + 14, self.rect[3] + 14
            pygame.draw.rect(screen, 'red', rect, 9)

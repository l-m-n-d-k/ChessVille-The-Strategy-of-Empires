import pygame
from groups_sprites import system_group, all_sprites
from sprites_images import images
from groups_sprites import players_group1, players_group2
from constants import *


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, position, player_number):
        super().__init__(system_group, all_sprites)
        image = {0: images['иконка 1'].copy(), 1: images['иконка 2'].copy(), 2: images['иконка 3'].copy()}
        self.image = image[player_number].copy()
        self.rect = self.image.get_rect(topleft=position)
        self.numb = player_number
        self.tip = 'без креста'

    def draw_base_rama(self, hod, select_icon):
        rect = self.rect[0] - 7, self.rect[1] - 7, self.rect[2] + 14, self.rect[3] + 14
        pygame.draw.rect(screen, (78, 87, 84), rect, 7)
        if hod == 'first':
            for sprite in players_group1:
                if sprite.tip == self.numb + 1 and sprite.live is False and self.tip == 'без креста':
                    image = pygame.transform.scale(images['красный крест'].copy(), (90, 90))
                    self.image.blit(image, (5, 5))
                    self.tip = 'с крестом'
                    break
                elif sprite.tip == self.numb + 1 and sprite.live is True and self.tip == 'с крестом':
                    self.image = images[f'иконка {self.numb + 1}'].copy()
                    self.tip = 'без креста'
        elif hod == 'second':
            for sprite in players_group2:
                if sprite.tip == self.numb + 4 and sprite.live is False and self.tip == 'без креста':
                    image = pygame.transform.scale(images['красный крест'].copy(), (90, 90))
                    self.image.blit(image, (5, 5))
                    self.tip = 'с крестом'
                    break
                elif sprite.tip == self.numb + 4 and sprite.live is True and self.tip == 'с крестом':
                    self.image = images[f'иконка {self.numb + 1}'].copy()
                    self.tip = 'без креста'

    def draw_select_rama(self, select_icon):
        if self.numb == select_icon:
            rect = self.rect[0] - 7, self.rect[1] - 7, self.rect[2] + 14, self.rect[3] + 14
            pygame.draw.rect(screen, 'red', rect, 9)

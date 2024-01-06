import pygame
from groups_sprites import tiles_group, tyman_group1, tyman_group2, all_sprites
from sprites_images import images
from constants import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        surface.set_alpha(10)
        pygame.draw.rect(surface, (110, 110, 110), [0, 0, 100, 100], 1)  # Рисование прямоугольника
        self.image.blit(surface, (0, 0))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tyman1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tyman_group1, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tyman2(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tyman_group2, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

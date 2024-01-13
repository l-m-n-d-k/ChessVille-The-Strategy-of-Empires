import pygame
from groups_sprites import window_group, button_group, all_sprites
from sprites_images import images
from constants import *
import time


class SmallWindow(pygame.sprite.Sprite):
    next_counter = 0

    def __init__(self, target, pos_x, pos_y):
        super().__init__(window_group, all_sprites)
        self.last = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        self.cord = (pos_x, pos_y)
        self.image = images['окошко кратких характеристик']
        self.rect = self.image.get_rect(bottomleft=pos)
        self.target = target
        if SmallWindow.next_counter > 0 or not self.target.rect.collidepoint(pos):
            self.kill()
        else:
            SmallWindow.next_counter += 1

    def update(self, camera, *args):
        for elem in args:
            if isinstance(elem, pygame.event.Event) and elem.type == pygame.MOUSEMOTION:
                if not self.target.rect.collidepoint(elem.pos):
                    SmallWindow.next_counter -= 1
                    self.kill()

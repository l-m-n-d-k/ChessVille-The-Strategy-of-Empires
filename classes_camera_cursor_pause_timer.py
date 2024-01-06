import pygame
from sprites_images import images
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group
from constants import *


class MyCursor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(system_group, all_sprites, *group)
        self.image = images['курсор']
        self.image.set_alpha(80)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        for ev in args:
            if isinstance(ev, pygame.event.Event) and ev.type == pygame.MOUSEMOTION:
                self.rect.topleft = ev.pos
                pygame.draw.rect(self.image, 'red', [0, 0, 50, 47], 2)


class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.camera_x = self.camera_y = 0
        self.target_x = self.target_y = screen_width // 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

    def update_camera(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Ограничиваем положение target_x и target_y, чтобы не выходили за границы карты
        self.target_x = max(self.screen_width // 2, min(self.map_width - self.screen_width // 2, mouse_x))
        self.target_y = max(self.screen_height // 2, min(self.map_height - self.screen_height // 2, mouse_y))

        # Проверка, достигла ли мышь границ экрана для перемещения карты
        if mouse_x < self.screen_width * 0.05 and self.camera_x > 0:
            self.camera_x -= 10
        elif mouse_x > self.screen_width * 0.95 and self.camera_x < self.map_width - self.screen_width:
            self.camera_x += 10
        if mouse_y < self.screen_height * 0.05 and self.camera_y > 0:
            self.camera_y -= 10
        elif mouse_y > self.screen_height * 0.95 and self.camera_y < self.map_height - self.screen_height:
            self.camera_y += 10

    def update_targets(self):
        for sprite in tiles_group:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group1:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group2:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in neytral_group:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in tyman_group1:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in tyman_group2:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)

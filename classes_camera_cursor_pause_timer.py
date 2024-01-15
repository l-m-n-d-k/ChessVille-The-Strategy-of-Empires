import pygame
from sprites_images import images
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group, window_group, button_group, info_group
from constants import *


class MyCursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(system_group, all_sprites)
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
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

    def update_camera(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Проверка, достигла ли мышь границ экрана для перемещения карты
        if mouse_x < self.screen_width * 0.005 and self.camera_x > 0:
            self.camera_x -= 10
        elif mouse_x > self.screen_width * 0.99 and self.camera_x < self.map_width - self.screen_width:
            self.camera_x += 10
        if mouse_y < self.screen_height * 0.005 and self.camera_y > 0:
            self.camera_y -= 10
        elif mouse_y > self.screen_height * 0.99 and self.camera_y < self.map_height - self.screen_height:
            self.camera_y += 10

    def focus_target(self, target):
        target_x = max(0, min(self.map_width - self.screen_width,
                              target.pos[0] * tile_width - self.screen_width // 2 + tile_width // 2))
        target_y = max(0, min(self.map_height - self.screen_height,
                              target.pos[1] * tile_height - self.screen_height // 2 + tile_height // 2))
        self.camera_x = target_x
        self.camera_y = target_y

    def update_targets(self):
        for sprite in tiles_group:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group1:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] + 6 - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group2:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] + 6 - self.camera_x,
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


class TimerAnim(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, sheet=images['таймер анимашка']):
        super().__init__(info_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update_value(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


"""class Timer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(button_group, all_sprites)
        self.image = images['кнопка характеристик']
        self.rect = self.image.get_rect()
        self.rect.topleft = (mimimapa.rect.x + 3, mimimapa.rect.y + 202)"""


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(button_group, all_sprites)
        self.image = images['пауза']
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

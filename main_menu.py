import sys
import pygame
import os
from classes_map import Map
from classes_camera_cursor_pause_timer import MyCursor, Camera
from classes_icons_and_select import PlayerIcon
from classes_info import MiniMap
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group
from constants import *
from main import *


def main_menu(screen, fps, clock):
    background_image = pygame.image.load('menu/fon.png')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    menu_running = True
    MyCursor()
    pygame.mouse.set_visible(False)

    # Загрузка изображений для кнопок
    start_image = pygame.image.load('menu/start.png')  # Путь к изображению для кнопки "Начать игру"
    exit_image = pygame.image.load('menu/exit.png')    # Путь к изображению для кнопки "Выход"

    while menu_running:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)

        # Координаты кнопок
        start_button = start_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        exit_button = exit_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))

        screen.blit(start_image, start_button)
        screen.blit(exit_image, exit_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    main()  # Завершение меню и начало игры
                    system_group.empty()
                    MyCursor()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()  # Выход из игры
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                system_group.update(event)

        system_group.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    sys.exit(main_menu(screen, fps, clock))

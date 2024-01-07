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

    while menu_running:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)

        # Создание текстовых объектов для кнопок
        start_text = font.render('Начать игру', True, (255, 255, 255))
        exit_text = font.render('Выход', True, (255, 255, 255))

        # Координаты кнопок
        start_button = start_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        exit_button = exit_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))

        screen.blit(start_text, start_button)
        screen.blit(exit_text, exit_button)

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

import sys
import pygame
from classes_camera_cursor_pause_timer import MyCursor
from groups_sprites import system_group
from constants import *
from main import *
from classes_music import Music


def main_menu(screen, fps, clock):
    Music().in_menu()
    background_image = pygame.image.load('menu/fon.png')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    menu_running = True
    MyCursor()
    pygame.mouse.set_visible(False)

    # Загрузка изображений для кнопок
    start_image = pygame.image.load('menu/new_game.png').subsurface((0, 650, 1500, 200))  # Путь к изображению для кнопки "Начать игру"
    start_image = pygame.transform.scale(start_image, (500, 80))
    exit_image = pygame.image.load('menu/exit.png').subsurface((0, 600, 1500, 500))    # Путь к изображению для кнопки "Выход"
    exit_image = pygame.transform.scale(exit_image, (500, 165))
    
    while menu_running:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)

        # Координаты кнопок
        start_button = start_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        exit_button = exit_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))

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

import pygame

pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()

tile_width = tile_height = 100
map_width = map_height = 30
ceil = {'Король': 0,
        'Ферзь': 9,
        'Ладья': 5,
        'Слон': 3,
        'Конь': 3,
        'Пешка': 1}
names = {1: 'Имя 1',
         2: 'Имя 2',
         3: 'Имя 3',
         4: 'Имя 4',
         5: 'Имя 5',
         6: 'Имя 6',
         12: 'Имя нейтрал 1',
         13: 'Имя нейтрал 2'}

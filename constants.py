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
names = {1: 'Рудеус',
         2: 'Лорд Гриффит',
         3: 'Аэрос',
         4: 'Командир Гатс',
         5: 'Колчак',
         6: 'Олдеренс',
         12: 'Голем',
         13: 'Минотавр'}

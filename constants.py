import pygame

pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()

tile_width = tile_height = 100
map_width = map_height = 30

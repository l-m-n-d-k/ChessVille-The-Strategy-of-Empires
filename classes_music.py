import pygame

def Music():
    pygame.mixer.init()
    pygame.mixer.music.load('music/Pirate Ship (Acoustic).mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
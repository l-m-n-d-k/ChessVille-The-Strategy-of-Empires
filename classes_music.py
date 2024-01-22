import pygame

class Music():
    def __init__(self):
         pygame.mixer.init()

    def in_game(self):
        pygame.mixer.music.load('music/Pirate Ship (Acoustic).mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def in_menu(self):
        pygame.mixer.music.load('music/Pirate Bay.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    def in_credits(self):
        ...
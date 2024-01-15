import pygame

all_sprites = pygame.sprite.Group()  # группа всех спрайтов
tiles_group = pygame.sprite.Group()  # поле, холм, река, гора
players_group1 = pygame.sprite.Group()  # герои первого игрока
players_group2 = pygame.sprite.Group()  # герои второго игрока
neytral_group = pygame.sprite.Group()  # нейтральные юниты
tyman_group1 = pygame.sprite.Group()  # туман войны от лица первого игрока
tyman_group2 = pygame.sprite.Group()  # туман войны от лица второго игрока
info_group = pygame.sprite.Group()  # миникарта, табличка с очками передвижения и боевой мощью,
button_group = pygame.sprite.Group()  # 2 круглых кнопки на миникарте, кнопка следующего хода
window_group = pygame.sprite.Group()  # для всплывающих окошек (таких пока не было)
system_group = pygame.sprite.Group()  # иконки и курсор
menu_group = pygame.sprite.Group() # всплывающее меню

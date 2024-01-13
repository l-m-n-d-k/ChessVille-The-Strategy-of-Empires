import pygame
from groups_sprites import window_group, button_group, all_sprites, players_group1, players_group2, neytral_group
from sprites_images import images
from constants import *
import time


class SmallWindow(pygame.sprite.Sprite):
    next_counter = 0

    def __init__(self, target, pos_x, pos_y, hod, position):
        pos = pygame.mouse.get_pos()
        if SmallWindow.next_counter > 0 or not pos == position:
            del self
        else:
            SmallWindow.next_counter += 1
        super().__init__(window_group, all_sprites)
        self.cord = (pos_x, pos_y)
        self.image = images['окошко кратких характеристик'].copy()
        self.rect = self.image.get_rect(bottomleft=pos)
        self.rect = (min(width - self.image.get_width(), max(0, self.rect[0])),
                     min(height - self.image.get_height(), max(0, self.rect[1])))
        self.target = target

        numb = target.tip
        my_hero = target
        name = my_hero.name
        tip = ('Созный герой' if my_hero in players_group1.sprites() else 'Вражеский герой' if my_hero in players_group2\
            else 'Нейтральный юнит') if hod == 'first' else ('Созный герой' if my_hero in players_group2.sprites() else\
            'Вражеский герой' if my_hero in players_group1 else 'Нейтральный юнит')
        color = ((0, 128, 0) if my_hero in players_group1.sprites() else (255, 0, 0) if my_hero in players_group2 \
            else (0, 0, 230)) if hod == 'first' else ((0, 128, 0) if my_hero in players_group2.sprites() else \
            (255, 0, 0) if my_hero in players_group1 else (0, 0, 230))
        steps = f"Перемещение: {str(my_hero.steps)} / {str(6 if numb in (2, 5) else 4 if numb in (1, 3, 4, 6) else 0)}"
        strong = f"Боевая мощь: {str(sum(my_hero.army[key] * ceil[key] for key in my_hero.army))}"

        if hod == 'first' and target in players_group1.sprites():
            pawn = pygame.transform.scale(images['пешка белые'].copy(), (43, 45))
            knight = pygame.transform.scale(images['конь белые'].copy(), (43, 45))
            bishop = pygame.transform.scale(images['слон белые'].copy(), (43, 45))
            rook = pygame.transform.scale(images['ладья белые'].copy(), (43, 45))
            queen = pygame.transform.scale(images['ферзь белые'].copy(), (43, 45))
            king = pygame.transform.scale(images['король белые'].copy(), (43, 45))

        elif hod == 'second' and target in players_group2.sprites():
            pawn = pygame.transform.scale(images['пешка белые'].copy(), (43, 45))
            knight = pygame.transform.scale(images['конь белые'].copy(), (43, 45))
            bishop = pygame.transform.scale(images['слон белые'].copy(), (43, 45))
            rook = pygame.transform.scale(images['ладья белые'].copy(), (43, 45))
            queen = pygame.transform.scale(images['ферзь белые'].copy(), (43, 45))
            king = pygame.transform.scale(images['король белые'].copy(), (43, 45))
        else:
            pawn = pygame.transform.scale(images['пешка чёрные'].copy(), (43, 45))
            knight = pygame.transform.scale(images['конь чёрные'].copy(), (43, 45))
            bishop = pygame.transform.scale(images['слон чёрные'].copy(), (43, 45))
            rook = pygame.transform.scale(images['ладья чёрные'].copy(), (43, 45))
            queen = pygame.transform.scale(images['ферзь чёрные'].copy(), (43, 45))
            king = pygame.transform.scale(images['король чёрные'].copy(), (43, 45))

        font1 = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 25)

        text_name = font1.render(name, True, color)
        text_tip = font2.render(tip, True, color)
        text_steps = font2.render(steps, True, (200, 200, 200))
        text_strong = font2.render(strong, True, (200, 200, 200))

        text_pawn = font2.render(str(my_hero.army['Пешка']), True, (200, 200, 200))
        text_knight = font2.render(str(my_hero.army['Конь']), True, (200, 200, 200))
        text_bishop = font2.render(str(my_hero.army['Слон']), True, (200, 200, 200))
        text_rook = font2.render(str(my_hero.army['Ладья']), True, (200, 200, 200))
        text_queen = font2.render(str(my_hero.army['Ферзь']), True, (200, 200, 200))
        text_king = font2.render(str(my_hero.army['Король']), True, (200, 200, 200))

        pawn.blit(text_pawn, (pawn.get_width() - text_pawn.get_width(), pawn.get_height() - text_pawn.get_height()))
        knight.blit(text_knight,
                    (knight.get_width() - text_knight.get_width(), knight.get_height() - text_knight.get_height()))
        bishop.blit(text_bishop,
                  (bishop.get_width() - text_bishop.get_width(), bishop.get_height() - text_bishop.get_height()))
        rook.blit(text_rook, (rook.get_width() - text_rook.get_width(), rook.get_height() - text_rook.get_height()))
        queen.blit(text_queen,
                  (queen.get_width() - text_queen.get_width(), queen.get_height() - text_queen.get_height()))
        king.blit(text_king, (king.get_width() - text_king.get_width(), king.get_height() - text_king.get_height()))

        self.image.blit(pawn, (41, 186))
        self.image.blit(knight, (110, 186))
        self.image.blit(bishop, (186, 186))
        self.image.blit(rook, (41, 257))
        self.image.blit(queen, (110, 257))
        self.image.blit(king, (186, 257))

        self.image.blit(text_name, (138 - text_name.get_width() // 2, 10))
        self.image.blit(text_tip, (138 - text_tip.get_width() // 2, 40))
        self.image.blit(text_steps, (35, 100))
        self.image.blit(text_strong, (35, 120))

    def update(self, camera, *args):
        for elem in args:
            if isinstance(elem, pygame.event.Event) and elem.type == pygame.MOUSEMOTION:
                if not self.target.rect.collidepoint(elem.pos):
                    SmallWindow.next_counter -= 1
                    self.kill()

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
            return
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


class LoseWindow(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__(window_group, all_sprites)
        self.image = images['окошко поражения'].copy()
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        self.target = target

        pawn = pygame.transform.scale(images['пешка белые'].copy(), (60, 60))
        knight = pygame.transform.scale(images['конь белые'].copy(), (60, 60))
        bishop = pygame.transform.scale(images['слон белые'].copy(), (60, 60))
        rook = pygame.transform.scale(images['ладья белые'].copy(), (60, 60))
        queen = pygame.transform.scale(images['ферзь белые'].copy(), (60, 60))
        king = pygame.transform.scale(images['король белые'].copy(), (60, 60))
        icon = pygame.transform.scale(images[f'иконка {target.tip - (3 if target.tip >= 4 else 0)}'].copy(), (60, 60))
        self.button_ok = ButtuonOk(self, dx=575, dy=385, x=125, y=37)

        font2 = pygame.font.Font(None, 25)

        text_pawn = font2.render(str(target.army['Пешка']), True, (200, 200, 200))
        text_knight = font2.render(str(target.army['Конь']), True, (200, 200, 200))
        text_bishop = font2.render(str(target.army['Слон']), True, (200, 200, 200))
        text_rook = font2.render(str(target.army['Ладья']), True, (200, 200, 200))
        text_queen = font2.render(str(target.army['Ферзь']), True, (200, 200, 200))
        text_king = font2.render(str(target.army['Король']), True, (200, 200, 200))

        pawn.blit(text_pawn, (pawn.get_width() - text_pawn.get_width(), pawn.get_height() - text_pawn.get_height()))
        knight.blit(text_knight,
                    (knight.get_width() - text_knight.get_width(), knight.get_height() - text_knight.get_height()))
        bishop.blit(text_bishop,
                  (bishop.get_width() - text_bishop.get_width(), bishop.get_height() - text_bishop.get_height()))
        rook.blit(text_rook, (rook.get_width() - text_rook.get_width(), rook.get_height() - text_rook.get_height()))
        queen.blit(text_queen,
                  (queen.get_width() - text_queen.get_width(), queen.get_height() - text_queen.get_height()))
        king.blit(text_king, (king.get_width() - text_king.get_width(), king.get_height() - text_king.get_height()))

        self.image.blit(icon, (80, 292))
        self.image.blit(king, (167, 292))
        self.image.blit(queen, (256, 292))
        self.image.blit(rook, (344, 292))
        self.image.blit(bishop, (434, 292))
        self.image.blit(knight, (523, 292))
        self.image.blit(pawn, (612, 292))


class WinWindow(pygame.sprite.Sprite):
    def __init__(self, my_hero, target):
        super().__init__(window_group, all_sprites)
        self.image = images['окошко победы'].copy()
        self.rect = self.image.get_rect(center=(width // 2, height // 2))

        icon_white = pygame.transform.scale(my_hero.icon.copy(), (50, 50))
        self.image.blit(icon_white, (70, 243))
        icon_black = pygame.transform.scale(target.icon.copy(), (50, 50))
        self.image.blit(icon_black, (70, 348))

        self.pawn_white = IconChessFigure(self.rect, 'пешка белые', my_hero.army['Пешка'], 508, 243)
        self.knight_white = IconChessFigure(self.rect, 'конь белые', my_hero.army['Конь'], 434, 243)
        self.bishop_white = IconChessFigure(self.rect, 'слон белые', my_hero.army['Слон'], 361, 243)
        self.rook_white = IconChessFigure(self.rect, 'ладья белые', my_hero.army['Ладья'], 285, 243)
        self.queen_white = IconChessFigure(self.rect, 'ферзь белые', my_hero.army['Ферзь'], 212, 243)
        self.king_white = IconChessFigure(self.rect, 'король белые', my_hero.army['Король'], 142, 243)
        self.icons_white = [self.pawn_white, self.knight_white, self.bishop_white, self.rook_white, self.queen_white,
                            self.king_white]

        self.pawn_black = IconChessFigure(self.rect, 'пешка чёрные', target.army['Пешка'], 508, 348)
        self.knight_black = IconChessFigure(self.rect, 'конь чёрные', target.army['Конь'], 434, 348)
        self.bishop_black = IconChessFigure(self.rect, 'слон чёрные', target.army['Слон'], 361, 348)
        self.rook_black = IconChessFigure(self.rect, 'ладья чёрные', target.army['Ладья'], 285, 348)
        self.queen_black = IconChessFigure(self.rect, 'ферзь чёрные', target.army['Ферзь'], 212, 348)
        self.king_black = IconChessFigure(self.rect, 'король чёрные', target.army['Король'], 142, 348)
        self.icons_black = [self.pawn_black, self.knight_black, self.bishop_black, self.rook_black, self.queen_black,
                            self.king_black]

        self.button_ok = ButtuonOk(self, dx=470, dy=430, x=100, y=30)
        #self.button_del = ButtonDelete(self, dx=55, dy=425, x=140, y=38)


class ButtuonOk(pygame.sprite.Sprite):
    def __init__(self, window, dx, dy, x, y):
        super().__init__(window_group, all_sprites)
        self.image = pygame.transform.scale(images['кнопка ок'].copy(), (x, y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (window.rect.x + dx, window.rect.y + dy)


class ButtonDelete(pygame.sprite.Sprite):
    def __init__(self, window, dx, dy, x, y):
        super().__init__(window_group, all_sprites)
        self.image = pygame.transform.scale(images['кнопка удалить'].copy(), (x, y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (window.rect.x + dx, window.rect.y + dy)


class IconChessFigure(pygame.sprite.Sprite):
    def __init__(self, parent_rect, name_image, count_unit, dx, dy):
        super().__init__(window_group, all_sprites)
        self.reserve = pygame.transform.scale(images[name_image].copy(), (50, 50))
        self.image = self.reserve.copy()
        font = pygame.font.Font(None, 25)
        if count_unit is None:
            self.can_moving = False
        else:
            text_figure = font.render(str(count_unit), True, (200, 200, 200))
            self.image.blit(text_figure, (self.image.get_width() - text_figure.get_width(), self.image.get_height() - text_figure.get_height()))
        self.rect = self.image.get_rect(topleft=(parent_rect[0] + dx, parent_rect[1] + dy))
        self.moving = False
        self.start_coords = self.rect.copy()
        self.start_coords_mouse = 0, 0

    def update_move(self, *args):
        for elem in args:
            if isinstance(elem, pygame.event.Event) and elem.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(elem.pos):
                    self.moving = True
                    self.start_coords_mouse = elem.pos
            elif isinstance(elem, pygame.event.Event) and elem.type == pygame.MOUSEBUTTONUP:
                self.moving = False

        if self.moving:
            mouse = pygame.mouse.get_pos()
            self.rect = self.image.get_rect().move(self.start_coords[0] + mouse[0] - self.start_coords_mouse[0],
                                 self.start_coords[1] + mouse[1] - self.start_coords_mouse[1])
        else:
            self.rect = self.start_coords




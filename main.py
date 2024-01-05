import sys
import pygame
import os
import csv
from copy import deepcopy

pygame.init()
pygame.display.set_caption("ChessVille: The Strategy of Empires")

info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
players_group1 = pygame.sprite.Group()
players_group2 = pygame.sprite.Group()
neytral_group = pygame.sprite.Group()
tyman_group1 = pygame.sprite.Group()
tyman_group2 = pygame.sprite.Group()
system_group = pygame.sprite.Group()

fps = 60
clock = pygame.time.Clock()

pygame.event.set_grab(True)

select_icon = 0
tile_width = tile_height = 100
map_width = map_height = 30
HOD = None


def load_image(name, directory='Фото персонажей', colorkey=None):
    fullname = os.path.join(directory, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = 'white'
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


images = {
    1: load_image('Разведчик.jpg', colorkey=-1),
    2: load_image('Герой.jpg', colorkey=-1),
    3: load_image('Разведчик.jpg', colorkey=-1),
    4: load_image('Разведчик.jpg', colorkey=-1),
    5: load_image('Герой.jpg', colorkey=-1),
    6: load_image('Разведчик.jpg', colorkey=-1),
    7: load_image('Холм.jpg'),
    8: load_image('Поле с речкой.jpg'),
    9: load_image('Поле.png'),
    10: load_image('Гора.jpg'),
    11: load_image('Туман войны.jpg'),
    12: load_image('Разбойник 1.jpg', colorkey=-1),
    13: load_image('Разбойник 2.jpg', colorkey=-1),
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        surface.set_alpha(10)
        pygame.draw.rect(surface, (110, 110, 110), [0, 0, 100, 100], 1)  # Рисование прямоугольника
        self.image.blit(surface, (0, 0))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Players1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(players_group1, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()
        self.tip = tile_type
        self.steps = 0
        self.board = [[None for _1 in range(map_width)] for _2 in range(map_height)]

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y, mapa):
        self.pos = pos_x, pos_y
        self._define_rect()
        self.update_board(mapa)

    def update_steps(self):
        if self.tip in (2, 5):
            self.steps = 6
        elif self.tip in (1, 3, 4, 6):
            self.steps = 4

    def update_board(self, mapa):
        board = [[[None, '', '', '']] * map_width for _ in range(map_height)]
        for y in range(map_height):
            for x in range(map_width):
                if mapa.fon[y][x] == 9:
                    board[y][x] = [None, "Поле"]
                elif mapa.fon[y][x] == 10:
                    board[y][x] = [None, "Гора"]
                elif mapa.fon[y][x] == 7:
                    board[y][x] = [None, "Холм"]
                elif mapa.fon[y][x] == 8:
                    board[y][x] = [None, "Река"]

                if mapa.neytral[y][x] in (12, 13):
                    board[y][x].append('Нейтрал')
                elif mapa.players[y][x] in (4, 5, 6):
                    board[y][x].append('Вражеский герой')
                elif mapa.players[y][x] in (1, 2, 3):
                    board[y][x].append('Союзный герой')
                elif mapa.players[y][x] == 0:
                    board[y][x].append('Пусто')

                if mapa.tyman1[y][x] == 11:
                    board[y][x].append('Туман')
                elif mapa.tyman1[y][x] == 0:
                    board[y][x].append('Тумана нет')

        board[self.pos[1]][self.pos[0]] = [0, 'Моя позция', 'Я', 'Тумана нет']

        steps = {'Поле': 1,
                 'Холм': 2,
                 'Река': 2,
                 'Моя позция': 0,
                 'Нейтрал': 2,
                 'Вражеский герой': 2,
                 'Пусто': 0,
                 'Я': 0}

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if abs(self.pos[1] - y) <= 10 and abs(self.pos[0] - x) <= 10 and ceil1[0] is None and ceil1[
                        1] != 'Гора' and ceil1[2] not in ('Я', 'Союзный герой') and ceil1[3] != 'Туман':
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            board_copy[y][x] = [optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]], *ceil1[1:]]
                            c += 1
                        else:
                            pass
            board = deepcopy(board_copy)

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if ceil1[0]:
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            numb = optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]]
                            if numb != ceil1[0]:
                                board_copy[y][x] = [numb, *ceil1[1:]]
                                c += 1
                        else:
                            pass
            board = deepcopy(board_copy)

        self.board = deepcopy(board)


class Players2(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(players_group2, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()
        self.tip = tile_type
        self.steps = 0
        self.board = [[None for _1 in range(map_width)] for _2 in range(map_height)]

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y, mapa):
        self.pos = pos_x, pos_y
        self._define_rect()
        self.update_board(mapa)

    def update_steps(self):
        if self.tip in (2, 5):
            self.steps = 6
        elif self.tip in (1, 3, 4, 6):
            self.steps = 4

    def update_board(self, mapa):
        board = [[[None, '', '', '', '']] * map_width for _ in range(map_height)]
        for y in range(map_height):
            for x in range(map_width):
                if mapa.fon[y][x] == 9:
                    board[y][x] = [None, "Поле"]
                elif mapa.fon[y][x] == 10:
                    board[y][x] = [None, "Гора"]
                elif mapa.fon[y][x] == 7:
                    board[y][x] = [None, "Холм"]
                elif mapa.fon[y][x] == 8:
                    board[y][x] = [None, "Река"]

                if mapa.neytral[y][x] in (12, 13):
                    board[y][x].append('Нейтрал')
                elif mapa.players[y][x] in (1, 2, 3):
                    board[y][x].append('Вражеский герой')
                elif mapa.players[y][x] in (4, 5, 6):
                    board[y][x].append('Союзный герой')
                elif mapa.players[y][x] == 0:
                    board[y][x].append('Пусто')

                if mapa.tyman2[y][x] == 11:
                    board[y][x].append('Туман')
                elif mapa.tyman2[y][x] == 0:
                    board[y][x].append('Тумана нет')

        board[self.pos[1]][self.pos[0]] = [0, 'Моя позция', 'Я', 'Тумана нет']

        steps = {'Поле': 1,
                 'Холм': 2,
                 'Река': 2,
                 'Моя позция': 0,
                 'Нейтрал': 2,
                 'Вражеский герой': 2,
                 'Пусто': 0,
                 'Я': 0}

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if abs(self.pos[1] - y) <= 10 and abs(self.pos[0] - x) <= 10 and ceil1[0] is None and ceil1[
                        1] != 'Гора' and ceil1[2] not in ('Я', 'Союзный герой') and ceil1[3] != 'Туман':
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            board_copy[y][x] = [optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]], *ceil1[1:]]
                            c += 1
                        else:
                            pass
            board = deepcopy(board_copy)

        c = True
        while c:
            c = 0
            board_copy = deepcopy(board)
            for y in range(map_height):
                for x in range(map_width):
                    ceil1 = board[y][x]
                    if ceil1[0]:
                        lst_sosedey = []
                        for dy in range(-1, 1 + 1):
                            for dx in range(-1, 1 + 1):
                                if x + dx < 0 or y + dy < 0:
                                    continue
                                if x + dx >= map_width or y + dy >= map_height:
                                    continue
                                if dx == 0 and dy == 0:
                                    continue

                                ceil = board[y + dy][x + dx]
                                if isinstance(ceil[0], int) and ceil[1] != 'Гора' and ceil1[2] != 'Союзный герой' and \
                                        ceil[3] != 'Туман':
                                    lst_sosedey.append(ceil)

                        if lst_sosedey:
                            optional_ceil = min(lst_sosedey, key=lambda i: i[0] + steps[i[1]] + steps[i[2]])
                            numb = optional_ceil[0] + steps[ceil1[1]] + steps[ceil1[2]]
                            if numb != ceil1[0]:
                                board_copy[y][x] = [numb, *ceil1[1:]]
                                c += 1
                        else:
                            pass
            board = deepcopy(board_copy)
        self.board = deepcopy(board)


class Neytral(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(neytral_group, all_sprites)
        self.image = images[tile_type]
        self.pos = pos_x, pos_y
        self._define_rect()

    def _define_rect(self):
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])

    def move(self, pos_x, pos_y):
        self.pos = pos_x, pos_y
        self._define_rect()


class Tyman1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tyman_group1, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tyman2(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tyman_group2, all_sprites)
        self.pos = pos_x, pos_y
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Map:
    def __init__(self):
        self.ox = 30
        self.oy = 30
        with (open('many_map/Фон 1.csv') as fon, open('many_map/Нейтральные юниты 1.csv') as neytral, open(
                'many_map/Туман войны 1.csv') as tyman1, open('many_map/Игроки 1.csv') as players,
              open('many_map/Туман войны 2.csv') as tyman2):
            self.fon = [[int(elem) for elem in lst] for lst in csv.reader(fon, delimiter=',')]
            self.neytral = [[int(elem) for elem in lst] for lst in csv.reader(neytral, delimiter=',')]
            self.tyman1 = [[int(elem) for elem in lst] for lst in csv.reader(tyman1, delimiter=',')]
            self.tyman2 = [[int(elem) for elem in lst] for lst in csv.reader(tyman2, delimiter=',')]
            self.players = [[int(elem) for elem in lst] for lst in csv.reader(players, delimiter=',')]
        for y in range(self.oy):
            for x in range(self.ox):
                sprite = self.fon[y][x]
                if sprite:
                    Tile(sprite, x, y)
                sprite = self.neytral[y][x]
                if sprite:
                    Neytral(sprite, x, y)
                sprite = self.tyman1[y][x]
                if sprite:
                    Tyman1(sprite, x, y)
                sprite = self.tyman2[y][x]
                if sprite:
                    Tyman2(sprite, x, y)
                sprite = self.players[y][x]
                if sprite in (1, 2, 3):
                    Players1(sprite, x, y)
                elif sprite in (4, 5, 6):
                    Players2(sprite, x, y)

    def draw_map(self, screen):
        if HOD == 'first':
            tiles_group.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            neytral_group.draw(screen)
            tyman_group1.draw(screen)
            system_group.draw(screen)
        elif HOD == 'second':
            tiles_group.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            neytral_group.draw(screen)
            tyman_group2.draw(screen)
            system_group.draw(screen)


class MyCursor(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self, *group):
        super().__init__(system_group, all_sprites, *group)
        self.image = MyCursor.image
        self.image.set_alpha(80)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        if args[0] and args[0].type == pygame.MOUSEMOTION:
            self.rect.topleft = args[0].pos
            pygame.draw.rect(self.image, 'red', [0, 0, 50, 47], 2)


class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.camera_x = self.camera_y = 0
        self.target_x = self.target_y = screen_width // 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

    def update_camera(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Ограничиваем положение target_x и target_y, чтобы не выходили за границы карты
        self.target_x = max(self.screen_width // 2, min(self.map_width - self.screen_width // 2, mouse_x))
        self.target_y = max(self.screen_height // 2, min(self.map_height - self.screen_height // 2, mouse_y))

        # Проверка, достигла ли мышь границ экрана для перемещения карты
        if (
                mouse_x < self.screen_width * 0.05
                and self.camera_x > 0
        ):
            self.camera_x -= 8
        elif (
                mouse_x > self.screen_width * 0.95
                and self.camera_x < self.map_width - self.screen_width
        ):
            self.camera_x += 8

        if (
                mouse_y < self.screen_height * 0.05
                and self.camera_y > 0
        ):
            self.camera_y -= 8
        elif (
                mouse_y > self.screen_height * 0.95
                and self.camera_y < self.map_height - self.screen_height
        ):
            self.camera_y += 8

    def update_targets(self):
        for sprite in tiles_group:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group1:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in players_group2:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in neytral_group:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in tyman_group1:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)
        for sprite in tyman_group2:
            sprite.rect = sprite.image.get_rect().move(tile_width * sprite.pos[0] - self.camera_x,
                                                       tile_height * sprite.pos[1] - self.camera_y)


class PlayerIcon(pygame.sprite.Sprite):
    images = {0: load_image('Иконка 1.jpg'), 1: load_image('Иконка 2.jpg'), 2: load_image('Иконка 3.jpg')}

    def __init__(self, position, player_number):
        super().__init__(system_group, all_sprites)
        self.image = PlayerIcon.images[player_number]
        self.rect = self.image.get_rect(topleft=position)
        self.numb = player_number

    def draw(self):
        if self.numb == select_icon:
            rect = self.rect[0] - 10, self.rect[1] - 10, self.rect[2] + 20, self.rect[3] + 20
            pygame.draw.rect(screen, 'red', rect, 10)

    def update(self, *args):
        global select_icon
        for ev in args:
            if ev and ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(ev.pos):
                select_icon = self.numb


def new_hod(player):
    global HOD
    if player == 'first':
        HOD = 'first'
        for sprite in players_group1:
            sprite.update_steps()
    elif player == 'second':
        HOD = 'second'
        for sprite in players_group2:
            sprite.update_steps()


def move(player, hero, pos_x, pos_y, mapa):
    my_hero = None
    if player == 'first':
        for sprite in players_group1:
            if sprite.tip == hero + 1:
                my_hero = sprite
        if not isinstance(my_hero.board[pos_y][pos_x][0], int):
            return  # звук "сюда нельзя пойти"
        elif my_hero.board[pos_y][pos_x][0] > my_hero.steps:
            return  # звук "слишком далеко"
        elif my_hero.board[pos_y][pos_x][2] in ['Нейтрал', 'Вражеский герой']:
            ok = ...  # Окошко вопрос pyqt хочет ли игрок пройти войной
            if ok:
                chess_boy()
            else:
                return
        else:
            mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0
            mapa.players[pos_y][pos_x] = my_hero.tip

            vision = 4 if my_hero.tip in (1, 3) else 3
            for sprite in tyman_group1:
                if abs(sprite.pos[0] - pos_x) <= vision and abs(sprite.pos[1] - pos_y) <= vision:
                    mapa.tyman1[sprite.pos[1]][sprite.pos[0]] = 0
                    sprite.kill()

            my_hero.steps -= my_hero.board[pos_y][pos_x][0]
            my_hero.move(pos_x, pos_y, mapa)


    elif player == 'second':
        for sprite in players_group2:
            if sprite.tip == hero + 4:
                my_hero = sprite
        if not isinstance(my_hero.board[pos_y][pos_x][0], int):
            return  # звук "сюда нельзя пойти"
        elif my_hero.board[pos_y][pos_x][0] > my_hero.steps:
            return  # звук "слишком далеко"
        elif my_hero.board[pos_y][pos_x][2] in ['Нейтрал', 'Вражеский герой']:
            ok = ...  # Окошко вопрос pyqt хочет ли игрок пройти войной
            if ok:
                chess_boy()
            else:
                return
        else:
            mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0
            mapa.players[pos_y][pos_x] = my_hero.tip

            vision = 4 if my_hero.tip in (4, 6) else 3
            for sprite in tyman_group2:
                if abs(sprite.pos[0] - pos_x) <= vision and abs(sprite.pos[1] - pos_y) <= vision:
                    mapa.tyman2[sprite.pos[1]][sprite.pos[0]] = 0
                    sprite.kill()

            my_hero.steps -= my_hero.board[pos_y][pos_x][0]
            my_hero.move(pos_x, pos_y, mapa)


def main():
    map_game = Map()
    new_hod('first')
    for sprite in players_group1:
        sprite.move(*sprite.pos, map_game)
    for sprite in players_group2:
        sprite.move(*sprite.pos, map_game)

    camera = Camera(screen.get_width(), screen.get_height(), 30 * tile_width, 30 * tile_height)
    player_icon_positions = [(10, height - 110), (120, height - 110), (230, height - 110)]
    player_icon = [PlayerIcon(position, i) for i, position in enumerate(player_icon_positions)]

    MyCursor()
    event_mousemotion = event_mousedown = None
    pygame.mouse.set_visible(False)
    game_running = True
    while game_running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
            if event.type == pygame.MOUSEMOTION:
                event_mousemotion = event
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_mousedown = event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Получение координат мыши
                tile_size = 100
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Нахождение координат клетки карты
                tile_x = (mouse_x + camera.camera_x) // tile_size
                tile_y = (mouse_y + camera.camera_y) // tile_size

                move(HOD, select_icon, tile_x, tile_y, map_game)
                print("Координаты клетки карты:", tile_x, tile_y)
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                new_hod('first' if HOD == 'second' else 'second')

        camera.update_camera()
        camera.update_targets()
        system_group.update(event_mousemotion, event_mousedown)
        all_sprites.update(event_mousemotion, event_mousedown)
        map_game.draw_map(screen)
        for icon in player_icon:
            icon.draw()

        clock.tick(fps)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())

import sys
import pygame
import os
from classes_map import Map  # класс инициализации игры
from classes_camera_cursor_pause_timer import MyCursor, Camera, TimerAnim, Pause, Timer  # курсор, камера, песочные часы по центру, пауза
from classes_icons_and_select import PlayerIcon  # иконки игркоов
from classes_windows import SmallWindow, LoseWindow
from classes_info import MiniMap, TableSteps  # миникарта, табличка информации об очках передвижения слева
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group, info_group, button_group, window_group, stop_menu_group  # все группы спрайтов
from constants import *  # константы
import threading
from classes_stop_menu import Pause_fon, Exit_button_pause, Return_to_game
from classes_music import Music

pygame.init()
pygame.display.set_caption("ChessVille: The Strategy of Empires")


fps = 60
clock = pygame.time.Clock()
pygame.event.set_grab(True)  # мышка не уйдёт с окошка пайгейм
HOD = ''  # переменная текущего хода (пол механик на ней держится)
select_icon = 0  # индекс выбранной иконки (тоже во многих механиках передаётся аргументом)
font = pygame.font.Font(None, 36)  # шрифт для фпс
Music()

def open_pause():
    pause_fon.rect.center = (width / 2, height / 2 - 50)
    exit_but.rect.center = (width / 2, height / 2 + 110)
    return_to_game.rect.center = (width / 2, height / 2 - 90)

def close_pause():
    for sprite in stop_menu_group:
        sprite.rect.center = (-1000, -1000)

def new_hod(player, camera, timer):  # функция начала нового хода
    global HOD, select_icon  # объявляем переменные глобальными, чтобы изменения распространялись на весь код
    timer.restart_time()
    if player == 'first':  # если ход передаётся первому игроку
        HOD = 'first'  # текущий ход - первый игрок
        for sprite in players_group1:
            sprite.update_steps()  # обновляем очки передвижения у каждого героя из группы героев первого игрока
        select_icon = 1  # назначаем выбранным героем центрального
        target = None  # переменная для текущего выбранного героя (центрального)
        for sprite in players_group1:
            if sprite.tip == select_icon + 1 and sprite.live is True:
                target = sprite
                break
        else:
            for sprite in sorted(players_group1.sprites(), key=lambda i: i.tip):
                if sprite.live is True:
                    target = sprite
                    select_icon = sprite.tip - 1
                    break
        camera.focus_target(target)  # фокусировка камеры на выбранном герое
    elif player == 'second':  # если ход передаётся второму игроку
        HOD = 'second'  # текущий ход - второй игрок
        for sprite in players_group2:
            sprite.update_steps()  # обновляем очки передвижения у каждого героя из группы героев второго игрока
        select_icon = 1  # назначаем выбранным героем центрального
        target = None  # переменная для текущего выбранного героя (центрального)
        for sprite in players_group2:
            if sprite.tip == select_icon + 4 and sprite.live is True:
                target = sprite
                break
        else:
            for sprite in sorted(players_group2.sprites(), key=lambda i: i.tip):
                if sprite.live is True:
                    target = sprite
                    select_icon = sprite.tip - 4
                    break
        camera.focus_target(target)  # фокусировка камеры на выбранном герое


def update_icon(event, camera, HOD, died=False):  # обновление выбранной иконки героя, на вход событие нажатия левой кнопки мыши, камера и текущий ход
    global select_icon  # объявляем переменную глобальной, чтобы изменения видел весь код
    if died:
        if HOD == 'first':  # если ход первого игрока
            for sprite1 in sorted(players_group1.sprites(), key=lambda i: i.tip):
                if sprite1.live is True:
                    select_icon = sprite1.tip - 1
                    camera.focus_target(sprite1)  # фокусируем камеру на игроке, которого выбрали через иконку
                    break
        elif HOD == 'second':  # если ход второго игрока
            for sprite1 in sorted(players_group2.sprites(), key=lambda i: i.tip):
                if sprite1.live is True:
                    select_icon = sprite1.tip - 4
                    camera.focus_target(sprite1)  # фокусируем камеру на игроке, которого выбрали через иконку
                    break
        return True
    for sprite in system_group:
        if isinstance(sprite, PlayerIcon) and sprite.rect.collidepoint(event.pos):  # если спрайт относится к классу иконок и на него нажали
            if HOD == 'first':  # если ход первого игрока
                for sprite1 in players_group1:
                    if sprite.numb + 1 == sprite1.tip and sprite1.live is True:
                        camera.focus_target(sprite1)  # фокусируем камеру на игроке, которого выбрали через иконку
                        select_icon = sprite.numb  # выбранным спрайтом объявляем спрайт, на который нажали
            elif HOD == 'second':  # если ход второго игрока
                for sprite1 in players_group2:
                    if sprite.numb + 4 == sprite1.tip and sprite1.live is True:
                        camera.focus_target(sprite1)  # фокусируем камеру на игроке, которого выбрали через иконку
                        select_icon = sprite.numb  # выбранным спрайтом объявляем спрайт, на который нажали
            return True  # нажатие на иконку произошло, спрайты под иконкой трогать не надо
    return False  # нажатия на иконку не произошло, можно обрабатывать клик дальше


def move(player, hero, pos_x, pos_y, mapa):  # передвижение игрока, аргументы: текущий ход, выбранная иконка, новая позиция по х, новая позиция по у, класс карты
    my_hero = None
    if player == 'first':  # если ход первого игрока
        for sprite in players_group1:
            if sprite.tip == hero + 1:
                my_hero = sprite  # находим спрайт выбранного героя
                my_hero.update_board(mapa)  # обновляем его вычисление пути до всех клеток на карте
        if not isinstance(my_hero.board[pos_y][pos_x][0], int):  # если дальность клетки None (нельзя пройти)
            # звук "сюда нельзя пойти"
            return
        elif my_hero.board[pos_y][pos_x][0] > my_hero.steps:  # если шагов до клетки больше, чем есть очков передвижения
            # звук "слишком далеко"
            return
        elif my_hero.board[pos_y][pos_x][2] in ['Нейтрал', 'Вражеский герой']:  # если в этой клетке враг
            for sprite in neytral_group:
                if sprite.pos == (pos_x, pos_y):
                    enemy = sprite
            for sprite in players_group2:
                if sprite.pos == (pos_x, pos_y):
                    enemy = sprite
            my_hero_strong = sum(my_hero.army[key] * ceil[key] for key in my_hero.army)
            enemy_strong = sum(enemy.army[key] * ceil[key] for key in enemy.army)
            if my_hero_strong >= enemy_strong:
                print('Я сильнее')
                ...
            else:
                LoseWindow(my_hero)
                mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0
                my_hero.live = False
                my_hero.steps = 0
                my_hero.move(-map_width, -map_height, mapa)
        else:  # герой может пройти на клетку
            mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0  # убираем героя с прошлой позиции в классе карты игры
            mapa.players[pos_y][pos_x] = my_hero.tip  # ставим в новую позицию числовой тип героя (тот же номер, что и на картах csv)

            vision = 4 if my_hero.tip in (1, 3) else 3  # в зависимости от типа 3 или 4 клетки обзора
            for sprite in tyman_group1:  # проходимся по туману войны
                if abs(sprite.pos[0] - pos_x) <= vision and abs(sprite.pos[1] - pos_y) <= vision:
                    mapa.tyman1[sprite.pos[1]][sprite.pos[0]] = 0  # удаляем туман из класса карты, если он близко
                    sprite.kill()  # убиваем спрайт тумана, если он близко

            my_hero.steps -= my_hero.board[pos_y][pos_x][0]  # уменьшаем очки передвижения героя
            my_hero.move(pos_x, pos_y, mapa)

    elif player == 'second':  # если ход второго игрока
        for sprite in players_group2:
            if sprite.tip == hero + 4:
                my_hero = sprite  # находим спрайт выбранного героя
                my_hero.update_board(mapa)  # обновляем его вычисление пути до всех клеток на карте
        if not isinstance(my_hero.board[pos_y][pos_x][0], int):  # если дальность клетки None (нельзя пройти)
            # звук "сюда нельзя пойти"
            return
        elif my_hero.board[pos_y][pos_x][0] > my_hero.steps:  # если шагов до клетки больше, чем есть очков передвижения
            # звук "слишком далеко"
            return
        elif my_hero.board[pos_y][pos_x][2] in ['Нейтрал', 'Вражеский герой']:
            for sprite in neytral_group:
                if sprite.pos == (pos_x, pos_y):
                    enemy = sprite
            for sprite in players_group1:
                if sprite.pos == (pos_x, pos_y):
                    enemy = sprite
            my_hero_strong = sum(my_hero.army[key] * ceil[key] for key in my_hero.army)
            enemy_strong = sum(enemy.army[key] * ceil[key] for key in enemy.army)
            if my_hero_strong >= enemy_strong:
                print('Я сильнее')
                ...
            else:
                LoseWindow(my_hero)
                mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0
                my_hero.live = False
                my_hero.steps = 0
                my_hero.pos = (-map_width, -map_height)

        else:  # герой может пройти на клетку
            mapa.players[my_hero.pos[1]][my_hero.pos[0]] = 0 # убираем героя с прошлой позиции в классе карты игры
            mapa.players[pos_y][pos_x] = my_hero.tip # ставим в новую позицию числовой тип героя (тот же номер, что и на картах csv)

            vision = 4 if my_hero.tip in (4, 6) else 3  # в зависимости от типа 3 или 4 клетки обзора
            for sprite in tyman_group2:  # проходимся по туману войны
                if abs(sprite.pos[0] - pos_x) <= vision and abs(sprite.pos[1] - pos_y) <= vision:
                    mapa.tyman2[sprite.pos[1]][sprite.pos[0]] = 0  # удаляем туман из класса карты, если он близко
                    sprite.kill()  # убиваем спрайт тумана, если он близко

            my_hero.steps -= my_hero.board[pos_y][pos_x][0]  # уменьшаем очки передвижения героя
            my_hero.move(pos_x, pos_y, mapa)  # от лица героя меняем свои координаты, обновляем карту, куда можно пойти

def create_SmallWindow(sprite, tile_x, tile_y, pos):
    SmallWindow(sprite, tile_x, tile_y, HOD, pos)


def main():
    global HOD, select_icon
    HOD = ''
    all_sprites.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    tiles_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    players_group1.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    players_group2.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    neytral_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    tyman_group1.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    tyman_group2.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    info_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    system_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    window_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    button_group.empty()  # очищаем группу спрайтов (нужно при рестарте игры)
    stop_menu_group.empty() # очищаем группу спрайтов (нужно при рестарте игры)

    map_game = Map()    # создаём карту, создаём все спрайты согласно картам csv файлов
    mimmap_game = MiniMap(map_game)  # создаём миникарту на основе основной игровой карты
    table_parametrs = TableSteps()  # добавляем табличку про очки перемещения
    timer = TimerAnim(7, 1, width // 2 - 30, height - 150)  # анимация таймера
    pause = Pause()  # кнопка паузы
    timer_number = Timer()

    global pause_fon, exit_but, return_to_game

    pause_fon = Pause_fon() 
    exit_but = Exit_button_pause() # кнопка выхода
    return_to_game = Return_to_game()
    close_pause()

    timer_event = pygame.USEREVENT + 1  # собственный ивент для анимации часов
    pygame.time.set_timer(timer_event, 1000)
    anim_event = pygame.USEREVENT + 2
    pygame.time.set_timer(anim_event, 285)

    camera = Camera(screen.get_width(), screen.get_height(), 30 * tile_width, 30 * tile_height)  # создание камеры
    new_hod('first', camera, timer_number)  # запускаем первый ход
    for sprite in players_group1:
        sprite.move(*sprite.pos, map_game)
    for sprite in players_group2:
        sprite.move(*sprite.pos, map_game)
    mimmap_game.update(HOD, map_game)  # ставим героев, обновляем их путь до соседних клеток, строим миникарту

    player_icon_positions = [(7, height - 104 - 150), (114, height - 104 - 150), (221, height - 104 - 150)]  # позиции иконок героев
    player_icon = [PlayerIcon(position, i) for i, position in enumerate(player_icon_positions)]  # создаём иконки

    MyCursor()  # делаем свой курсор
    event_mousemotion = None
    pygame.mouse.set_visible(False)  # прячем стандартный курсор
    game_running = True
    while game_running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:  # реакция на esc
                if event.key == pygame.K_ESCAPE:
                    # game_running = False
                    open_pause()
            if event.type == pygame.MOUSEMOTION:  # реакция на движение мыши
                event_mousemotion = event  # запоминаем для курсора на будущее
            if event.type == anim_event:  # событие анимашки таймера
                timer.update_value()
                for sprite in players_group1:
                    sprite.update_value()
                for sprite in players_group2:
                    sprite.update_value()
                for sprite in neytral_group:
                    sprite.update_value()
            if event.type == timer_event:
                result = timer_number.update_time()
                if result is False:
                    new_hod('first' if HOD == 'second' else 'second', camera, timer_number)
                    mimmap_game.update(HOD, map_game)
                    table_parametrs.update_stats(HOD, select_icon)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # нажатие левой кнопки мыши
                f = 0
                for sprite in window_group:
                    if isinstance(sprite, LoseWindow):
                        f = 1
                        if sprite.button_ok.rect.collidepoint(event.pos):
                            sprite.button_ok.kill()
                            sprite.kill()
                            update_icon(None, camera, HOD, True)
                            mimmap_game.update(HOD, map_game)
                            break
                if f:
                    break
                if update_icon(event, camera, HOD) is True:  # если нажали на иконку
                    pass
                elif pause.rect.collidepoint(event.pos):  # если нажали на паузу
                    open_pause()
                elif return_to_game.rect.collidepoint(event.pos):
                    close_pause()                  
                elif exit_but.rect.collidepoint(event.pos):
                    game_running = False
                elif mimmap_game.button_stats.rect.collidepoint(event.pos):  # если нажали на кнопку подробных характеристик
                    pass
                elif mimmap_game.button_wait.rect.collidepoint(event.pos):  # нажатие на кнопку убрать очки перемещения
                    mimmap_game.button_wait.click(HOD, select_icon)  # убираем очки передвижения
                    mimmap_game.button_unit_wait.upgrade(HOD)  # обновляем кнопку юнит ждёт приказа
                    table_parametrs.update_stats(HOD, select_icon)  # обновляем информацию таблички перемещения
                elif mimmap_game.button_unit_wait.rect.collidepoint(event.pos):  # нажатие на кнопку юнит ждёт приказа
                    sost, sprite, numb = mimmap_game.button_unit_wait.upgrade(HOD, True)  # обновляем выбранную иконку
                    if sost == 'юнит ждёт приказа':  # если было состояние юнит ждёт приказа
                        select_icon = numb
                        camera.focus_target(sprite)
                    else:  # если было состояние следующий ход
                        new_hod('first' if HOD == 'second' else 'second', camera, timer_number)
                        mimmap_game.update(HOD, map_game)
                    table_parametrs.update_stats(HOD, select_icon)
                else:  # если нажали с целью сделать ход
                    # Получение координат мыши
                    tile_size = tile_width
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Нахождение координат клетки карты
                    tile_x = (mouse_x + camera.camera_x) // tile_size
                    tile_y = (mouse_y + camera.camera_y) // tile_size

                    move(HOD, select_icon, tile_x, tile_y, map_game)  # перемещаемся героем выбранным
                    mimmap_game.button_unit_wait.upgrade(HOD)
                    mimmap_game.update(HOD, map_game)
                    table_parametrs.update_stats(HOD, select_icon)
            if event.type == pygame.MOUSEMOTION:  # реакция на движение мыши
                mimmap_game.update_select(event)  # затемняем кнопки, на которые навели мышью
                tile_size = tile_width
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Нахождение координат клетки карты
                tile_x = (mouse_x + camera.camera_x) // tile_size
                tile_y = (mouse_y + camera.camera_y) // tile_size
                if map_game.tyman1[tile_y][tile_x] == 0 and HOD == 'first' or \
                        map_game.tyman2[tile_y][tile_x] == 0 and HOD == 'second':
                    for sprite in players_group1:
                        if sprite.rect.collidepoint(event.pos):
                            tim = threading.Timer(1.1, create_SmallWindow, args=(sprite, tile_x, tile_y, pygame.mouse.get_pos()))  # Задержка в 5 секунд
                            tim.start()
                    for sprite in players_group2:
                        if sprite.rect.collidepoint(event.pos):
                            tim = threading.Timer(1.1, create_SmallWindow, args=(sprite, tile_x, tile_y, pygame.mouse.get_pos()))  # Задержка в 5 секунд
                            tim.start()
                    for sprite in neytral_group:
                        if sprite.rect.collidepoint(event.pos):
                            tim = threading.Timer(1.1, create_SmallWindow, args=(sprite, tile_x, tile_y, pygame.mouse.get_pos()))  # Задержка в 5 секунд
                            tim.start()

        stop_menu_group.update()
        camera.update_camera()  # проверяем, с краю ли мышка, надо ли двигать карту
        camera.update_targets()  # сдвигаем карту на текущее отклонение камеры
        system_group.update(event_mousemotion)
        window_group.update(camera, event_mousemotion)
        table_parametrs.update_stats(HOD, select_icon)
        map_game.draw_map(screen, HOD)  # рисуем карту
        for icon in player_icon:  # рисуем рамки иконок
            icon.draw_base_rama(HOD, select_icon)
        for icon in player_icon:
            icon.draw_select_rama(select_icon)

        fps_now = str(int(clock.get_fps()))  # выводим фпс
        fps_text = font.render("FPS: " + fps_now, True, (255, 255, 255), (0, 0, 0))
        screen.blit(fps_text, (width - 100, 10))

        clock.tick(fps)
        pygame.display.flip()

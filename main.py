import sys
import pygame
import os
from classes_map import Map
from classes_camera_cursor_pause_timer import MyCursor, Camera, TimerAnim
from classes_icons_and_select import PlayerIcon
from classes_info import MiniMap, TableSteps
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group, info_group, button_group, window_group
from constants import *

pygame.init()
pygame.display.set_caption("ChessVille: The Strategy of Empires")

fps = 60
clock = pygame.time.Clock()
pygame.event.set_grab(True)
HOD = ''
select_icon = 0
font = pygame.font.Font(None, 36)


def new_hod(player, camera):
    global HOD, select_icon
    if player == 'first':
        HOD = 'first'
        for sprite in players_group1:
            sprite.update_steps()
        select_icon = 1
        target = None
        for sprite in players_group1:
            if sprite.tip == select_icon + 1:
                target = sprite
        camera.focus_target(target)
    elif player == 'second':
        HOD = 'second'
        for sprite in players_group2:
            sprite.update_steps()
        select_icon = 1
        target = None
        for sprite in players_group2:
            if sprite.tip == select_icon + 4:
                target = sprite
        camera.focus_target(target)


def update_icon(event, camera, HOD):
    global select_icon
    for sprite in system_group:
        if isinstance(sprite, PlayerIcon) and sprite.rect.collidepoint(event.pos):
            select_icon = sprite.numb
            if HOD == 'first':
                for sprite1 in players_group1:
                    if select_icon + 1 == sprite1.tip:
                        camera.focus_target(sprite1)
            elif HOD == 'second':
                for sprite1 in players_group2:
                    if select_icon + 4 == sprite1.tip:
                        camera.focus_target(sprite1)
            return True
    return False


def move(player, hero, pos_x, pos_y, mapa):
    my_hero = None
    if player == 'first':
        for sprite in players_group1:
            if sprite.tip == hero + 1:
                my_hero = sprite
                my_hero.update_board(mapa)
        if not isinstance(my_hero.board[pos_y][pos_x][0], int):
            return  # звук "сюда нельзя пойти"
        elif my_hero.board[pos_y][pos_x][0] > my_hero.steps:
            return  # звук "слишком далеко"
        elif my_hero.board[pos_y][pos_x][2] in ['Нейтрал', 'Вражеский герой']:
            print(1)
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
            # camera.focus_target(my_hero)

    elif player == 'second':
        for sprite in players_group2:
            if sprite.tip == hero + 4:
                my_hero = sprite
                my_hero.update_board(mapa)
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
            # camera.focus_target(my_hero)


def main():
    global HOD, select_icon
    HOD = ''
    all_sprites.empty()
    tiles_group.empty()
    players_group1.empty()
    players_group2.empty()
    neytral_group.empty()
    tyman_group1.empty()
    tyman_group2.empty()
    info_group.empty()
    system_group.empty()
    window_group.empty()
    button_group.empty()

    map_game = Map()
    mimmap_game = MiniMap(map_game)
    table_parametrs = TableSteps()
    timer = TimerAnim(7, 1, width // 2 - 30, height - 150)
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 285)
    camera = Camera(screen.get_width(), screen.get_height(), 30 * tile_width, 30 * tile_height)
    new_hod('first', camera)
    for sprite in players_group1:
        sprite.move(*sprite.pos, map_game)
    for sprite in players_group2:
        sprite.move(*sprite.pos, map_game)
    mimmap_game.update(HOD, map_game)

    player_icon_positions = [(7, height - 104 - 150), (114, height - 104 - 150), (221, height - 104 - 150)]
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
                mimmap_game.update_select(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_mousedown = event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if update_icon(event, camera, HOD) is True:
                    pass
                elif mimmap_game.button_stats.rect.collidepoint(event.pos):
                    pass
                elif mimmap_game.button_wait.rect.collidepoint(event.pos):
                    mimmap_game.button_wait.click(HOD, select_icon)
                    mimmap_game.button_unit_wait.upgrade(HOD)
                    table_parametrs.update_stats(HOD, select_icon)
                elif mimmap_game.button_unit_wait.rect.collidepoint(event.pos):
                    sost, sprite, numb = mimmap_game.button_unit_wait.upgrade(HOD, True)
                    if sost == 'юнит ждёт приказа':
                        select_icon = numb
                        camera.focus_target(sprite)
                    else:
                        new_hod('first' if HOD == 'second' else 'second', camera)
                        mimmap_game.update(HOD, map_game)
                    table_parametrs.update_stats(HOD, select_icon)
                else:
                    # Получение координат мыши
                    tile_size = 100
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Нахождение координат клетки карты
                    tile_x = (mouse_x + camera.camera_x) // tile_size
                    tile_y = (mouse_y + camera.camera_y) // tile_size

                    move(HOD, select_icon, tile_x, tile_y, map_game)
                    mimmap_game.button_unit_wait.upgrade(HOD)
                    mimmap_game.update(HOD, map_game)
                    table_parametrs.update_stats(HOD, select_icon)
            if event.type == timer_event:
                timer.update_value()

        camera.update_camera()
        camera.update_targets()
        system_group.update(event_mousemotion, event_mousedown)
        all_sprites.update(event_mousemotion, event_mousedown)
        table_parametrs.update_stats(HOD, select_icon)
        map_game.draw_map(screen, HOD)
        for icon in player_icon:
            icon.draw_base_rama(select_icon)
        for icon in player_icon:
            icon.draw_select_rama(select_icon)
        fps_now = str(int(clock.get_fps()))
        fps_text = font.render("FPS: " + fps_now, True, (255, 255, 255), (0, 0, 0))
        screen.blit(fps_text, (width - 100, 10))

        clock.tick(fps)
        pygame.display.flip()

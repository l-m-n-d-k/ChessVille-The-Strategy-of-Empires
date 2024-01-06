import sys
import pygame
import os
from classes_map import Map
from classes_camera_cursor_pause_timer import MyCursor, Camera
from classes_icons_and_select import PlayerIcon
from groups_sprites import all_sprites, tiles_group, players_group1, players_group2, neytral_group, tyman_group1, \
    tyman_group2, system_group
from constants import *

pygame.init()
pygame.display.set_caption("ChessVille: The Strategy of Empires")

fps = 60
clock = pygame.time.Clock()
pygame.event.set_grab(True)
HOD = ''
select_icon = 0


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


def update_icon(event):
    global select_icon
    for sprite in system_group:
        if isinstance(sprite, PlayerIcon) and sprite.rect.collidepoint(event.pos):
            select_icon = sprite.numb
            return True
    return False


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
    global HOD
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
                if update_icon(event) is False:
                    # Получение координат мыши
                    tile_size = 100
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Нахождение координат клетки карты
                    tile_x = (mouse_x + camera.camera_x) // tile_size
                    tile_y = (mouse_y + camera.camera_y) // tile_size

                    move(HOD, select_icon, tile_x, tile_y, map_game)
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                new_hod('first' if HOD == 'second' else 'second')

        camera.update_camera()
        camera.update_targets()
        system_group.update(event_mousemotion, event_mousedown)
        all_sprites.update(event_mousemotion, event_mousedown)
        map_game.draw_map(screen, HOD)
        for icon in player_icon:
            icon.draw(select_icon)

        clock.tick(fps)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())

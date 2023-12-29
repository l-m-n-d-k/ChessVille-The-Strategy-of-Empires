import sys
import pygame
import pytmx
import os

pygame.init()
pygame.display.set_caption("ChessVille: The Strategy of Empires")
width, height = 1200, 800
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
fps = 60
pygame.event.set_grab(True)
tmx_data = pytmx.load_pygame(r'many_map/test_map1.tmx')
select_icon = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MyCursor(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MyCursor.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, 'red', self.rect, 2)

    def update(self, *args):
        if args[0] and args[0].type == pygame.MOUSEMOTION:
            self.rect.topleft = args[0].pos


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
            self.camera_x -= 5
        elif (
                mouse_x > self.screen_width * 0.95
                and self.camera_x < self.map_width - self.screen_width
        ):
            self.camera_x += 5

        if (
                mouse_y < self.screen_height * 0.05
                and self.camera_y > 0
        ):
            self.camera_y -= 5
        elif (
                mouse_y > self.screen_height * 0.95
                and self.camera_y < self.map_height - self.screen_height
        ):
            self.camera_y += 5


class PlayerIcon(pygame.sprite.Sprite):
    images = {0: load_image('Иконка 1.jpg'), 1: load_image('Иконка 2.jpg'), 2: load_image('Иконка 3.jpg')}

    def __init__(self, position, player_number, *group):
        super().__init__(*group)
        self.image = PlayerIcon.images[player_number]
        self.rect = self.image.get_rect(topleft=position)
        self.numb = player_number

    def draw(self):
        if self.numb == select_icon:
            rect = self.rect[0] - 10, self.rect[1] - 10, self.rect[2] + 20, self.rect[3] + 20
            pygame.draw.rect(screen, 'red', rect, 10)

    def update(self, *args):
        for ev in args:
            if ev and ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(ev.pos):
                global select_icon
                select_icon = self.numb


def main():
    all_sprites = pygame.sprite.Group()
    camera = Camera(screen.get_width(), screen.get_height(), tmx_data.width * tmx_data.tilewidth,
                    tmx_data.height * tmx_data.tileheight)
    player_icons = pygame.sprite.Group()
    player_icon_positions = [(10, height - 110), (120, height - 110), (230, height - 110)]

    player_icon = [PlayerIcon(position, i, all_sprites, player_icons) for i, position in
                   enumerate(player_icon_positions)]
    cursor = MyCursor(all_sprites)
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

                print("Координаты клетки карты:", tile_x, tile_y)

        for icon in player_icons:
            icon.draw()
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (
                            x * tmx_data.tilewidth - camera.camera_x, y * tmx_data.tileheight - camera.camera_y))

        if event_mousemotion:
            camera.update_camera()
        cursor.draw(screen)
        for icon in player_icon:
            icon.draw()
        all_sprites.update(event_mousemotion, event_mousedown)
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
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


def main():
    all_sprites = pygame.sprite.Group()
    cursor = MyCursor(all_sprites)
    camera = Camera(screen.get_width(), screen.get_height(), tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

    event_mousemotion = None
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

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tmx_data.tilewidth - camera.camera_x, y * tmx_data.tileheight - camera.camera_y))

        if event_mousemotion:
            camera.update_camera()
        cursor.draw(screen)
        all_sprites.update(event_mousemotion)
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    sys.exit(main())

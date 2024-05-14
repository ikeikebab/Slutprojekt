import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2

window = pygame.display.set_mode((WIDTH, HEIGHT))

class GraphicsManager:
    @staticmethod
    def get_background(name, width, height):
        image = pygame.image.load(join("assets", "Background", name)).convert()
        _, _, image_width, image_height = image.get_rect()
        tiles = []

        for i in range(width // image_width + 1):
            for j in range(height // image_height + 1):
                pos = (i * image_width, j * image_height)
                tiles.append(pos)

        return tiles, image

    @staticmethod
    def flip(sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    @staticmethod
    def load_sprite_sheets(dir1, dir2, width, height, direction=False):
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = GraphicsManager.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites

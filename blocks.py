
import pygame
from graphics_manager import GraphicsManager
from os.path import join
from os import listdir
from os.path import isfile

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class ObjectManager:
    @staticmethod
    def get_block(size):
        path = join("assets", "Terrain", "Terrain.png")
        image = pygame.image.load(path).convert()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

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

    @staticmethod
    def create_block(x, y, size):
        block = Object(x, y, size, size)
        block.image.blit(ObjectManager.get_block(size), (0, 0))
        block.mask = pygame.mask.from_surface(block.image)
        return block

    @staticmethod
    def create_fire(x, y, width, height):
        fire = Object(x, y, width, height, "fire")
        fire_sprites = ObjectManager.load_sprite_sheets("Traps", "Fire", width, height)
        fire.image = fire_sprites["on"][0]
        fire.mask = pygame.mask.from_surface(fire.image)
        fire.animation_count = 0
        fire.animation_name = "off"
        return fire


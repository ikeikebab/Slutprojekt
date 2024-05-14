import pygame
import os
from os.path import join

PLAYER_VEL = 5
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))

class Utility:
    @staticmethod
    def flip(sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    @staticmethod
    def load_sprite_sheets(dir1, dir2, width, height, direction=False):
        path = os.path.join("assets", dir1, dir2)
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = Utility.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites
    

    @staticmethod
    def get_block(size):
        path = os.path.join("assets", "Terrain", "Terrain.png")
        image = pygame.image.load(path).convert()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

    @staticmethod
    def handle_vertical_collision(player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()

                collided_objects.append(obj)

        return collided_objects

    @staticmethod
    def collide(player, objects, dx):
        player.move(dx, 0)
        player.update()
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                collided_object = obj
                break

        player.move(-dx, 0)
        player.update()
        return collided_object

    @staticmethod
    def handle_move(player, objects):
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        collide_left = Utility.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = Utility.collide(player, objects, PLAYER_VEL * 2)

        if keys[pygame.K_a] and not collide_left:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_d] and not collide_right:
            player.move_right(PLAYER_VEL)

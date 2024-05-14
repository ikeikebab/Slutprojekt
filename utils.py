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
    def get_background(name):
        image = pygame.image.load(join("assets", "Background", name)).convert()
        _, _, width, height = image.get_rect()
    tiles = []
    

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

        if dy > 0:  # If moving down
            for obj in objects:
                if pygame.sprite.collide_rect(player, obj):
                    player.rect.bottom = obj.rect.top  # Adjust player's position
                    player.landed()  # Reset jump count
                    collided_objects.append(obj)
        elif dy < 0:  # If moving up
            for obj in objects:
                if pygame.sprite.collide_rect(player, obj):
                    player.rect.top = obj.rect.bottom  # Adjust player's position
                    player.hit_head()  # Reverse vertical velocity
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

        # Horizontal movement
        if keys[pygame.K_a]:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_d]:
            player.move_right(PLAYER_VEL)

        # Check for collisions horizontally
        collide_left = Utility.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = Utility.collide(player, objects, PLAYER_VEL * 2)

        # Apply gravity only if player is in the air
        if not player.is_landed(objects):
            player.apply_gravity()

        # Vertical movement (jumping)
        if keys[pygame.K_SPACE] and player.is_landed(objects):
            player.jump()

        # Apply vertical movement
        player.move(0, player.y_vel)

        # Check for collisions vertically
        collided_objects_y = Utility.handle_vertical_collision(player, objects, player.y_vel)

        # Update player position after movement
        player.update()

        # If collided vertically, reset vertical velocity
        if collided_objects_y:
            player.y_vel = 0



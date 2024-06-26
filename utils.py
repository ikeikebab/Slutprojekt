import pygame
import os
from os.path import join

PLAYER_VEL = 5  # Spelarens hastighet
WIDTH, HEIGHT = 1280, 720  # Fönstrets bredd och höjd
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Skapa ett fönster med angiven storlek

class Utility:
    @staticmethod
    def flip(sprites):
        # Funktion för att spegelvända sprites horisontellt
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    @staticmethod
    def load_sprite_sheets(dir1, dir2, width, height, direction=False):
        # Ladda in sprite-ark och skapa en lista med sprites
        path = os.path.join("assets", dir1, dir2)  # Sökväg till sprite-arkivet
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]  # Lista med filer i mappen

        all_sprites = {}  # Dictionary för att lagra alla sprites

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()  # Ladda in sprite-arket

            sprites = []  # Lista för att lagra sprites från sprite-arket
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # Skapa en yta för varje sprite
                rect = pygame.Rect(i * width, 0, width, height)  # Rektangel för att klippa ut en sprite från arkivet
                surface.blit(sprite_sheet, (0, 0), rect)  # Klipp ut och klistra in spriten på ytan
                sprites.append(pygame.transform.scale2x(surface))  # Skalning av spriten

            if direction:
                # Om riktning är sann, skapa sprites för både höger och vänster rörelse
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = Utility.flip(sprites)
            else:
                # Annars, lägg till sprites i dictionary
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites  # Returnera dictionary med alla sprites

    @staticmethod
    def collide(player, objects, dy):
        # Kollisionshantering mellan spelaren och objekt
        collided_objects = []  # Lista för kolliderande objekt
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                # Om spelaren kolliderar med ett objekt
                if dy > 0:
                    player.rect.bottom = obj.rect.top  # Justera spelarens position vid bottenkollision
                    player.landed()  # Anropa spelarens landningsfunktion
                elif dy < 0:
                    player.rect.top = obj.rect.bottom  # Justera spelarens position vid toppkollision
                    player.hit_head()  # Anropa spelarens funktion för träff i huvudet
                collided_objects.append(obj)  # Lägg till objektet i listan över kolliderande objekt
        return collided_objects  # Returnera listan över kolliderande objekt

    @staticmethod
    def handle_move(player, objects):
        # Hantera spelarens rörelse bas
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        if keys[pygame.K_a]:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_d]:
            player.move_right(PLAYER_VEL)

        player.update()

        Utility.collide(player, objects, player.y_vel)


import pygame   
from os.path import join

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        # Skapa en yta för objektet med önskad färg och storlek
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # Skapa en rektangel för objektets position och storlek
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, offset_x):
        # Rita objektet på skärmen med given förskjutning
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Blocks(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 0, 0))
        # Fyll ytan med transparent färg för att göra blocket osynligt
        self.image.fill((0, 0, 0, 0))
        # Skapa en mask för kollision med blocket
        self.mask = pygame.mask.from_surface(self.image)

class Block(Blocks):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size) # Anropa överordnad klass' init-metod med position och storlek
        block_image = self.get_block(size) # Hämta blockbild med given storlek från get_block
        self.image.blit(block_image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image) # Skapa en mask för kollision med blocket
    
    @staticmethod
    def get_block(size):
        # Skapa en block-yta med angiven storlek
        path = join("assets", "Terrain", "Terrain.png") # Sökväg till block-bild
        image = pygame.image.load(path).convert_alpha() # Ladda in block-bilden
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # Skapa en yta för blocket
        rect = pygame.Rect(96, 0, size, size) # Rektangel för att klippa ut blocket från bilden
        surface.blit(image, (0, 0), rect) # Klipp ut och klistra in blocket på ytan
        return pygame.transform.scale2x(surface) # Skalning av blocket


class SpawnBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size) # Anropa Block-klassens init-metod med position och storlek
        self.image = self.get_spawn_block(size) # Hämta startpunktens bild med given storlek från get_spawn_block
        self.mask = pygame.mask.from_surface(self.image) # Skapa en mask för kollision med startpunkten
        
    @staticmethod
    def get_spawn_block(size):
        # Skapa en startpunkt-yta med angiven storlek
        path = join("assets", "Terrain", "Spawn.png") # Sökväg till startpunkt-bild
        image = pygame.image.load(path).convert_alpha() # Ladda in startpunkt-bilden
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # Skapa en yta för startpunkten
        rect = pygame.Rect(0, 0, size, size) # Rektangel för att klippa ut startpunkten från bilden
        surface.blit(image, (0, 0), rect) # Klipp ut och klistra in startpunkten på ytan
        return pygame.transform.scale2x(surface) # Skalning av startpunkten

class CheckpointBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size) # Anropa Block-klassens init-metod med position och storlek
        self.image = self.get_checkpoint_block(size) # Hämta startpunktens bild med given storlek från get_checkpoint_block
        self.mask = pygame.mask.from_surface(self.image) # Skapa en mask för kollision med blocket
        
    @staticmethod
    def get_checkpoint_block(size):
        # Skapa en kontrollpunkt-yta med angiven storlek
        path = join("assets", "Terrain", "Checkpoint.png") # Sökväg till kontrollpunkt-bild
        image = pygame.image.load(path).convert_alpha() # Ladda in kontrollpunkt-bilden
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # Skapa en yta för kontrollpunkten
        rect = pygame.Rect(32, 0, size, size) # Rektangel för att klippa ut kontrollpunkten från bilden
        surface.blit(image, (0, 0), rect) # Klipp ut och klistra in kontrollpunkten på ytan
        return pygame.transform.scale2x(surface) # Skalning av kontrollpunkten

class GoalBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size) # Anropa Block-klassens init-metod med position och storlek 
        self.image = self.get_goal_block(size) # Hämta startpunktens bild med given storlek från get_goal_block
        self.mask = pygame.mask.from_surface(self.image) # Skapa en mask för kollision med startpunkten
        
    @staticmethod
    def get_goal_block(size):
        # Skapa en målpunkt-yta med angiven storlek
        path = join("assets", "Terrain", "Goal.png") # Sökväg till målpunkt-bild
        image = pygame.image.load(path).convert_alpha() # Ladda in målpunkt-bilden
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # Skapa en yta för målpunkten
        rect = pygame.Rect(64, 0, size, size) # Rektangel för att klippa ut målpunkten från bilden
        surface.blit(image, (0, 0), rect) # Klipp ut och klistra in målpunkten på ytan
        return pygame.transform.scale2x(surface) # Skalning av målpunktens

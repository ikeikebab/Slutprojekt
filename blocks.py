import pygame
from sprites import Blocks  # Importera Blocks-klassen från sprites-modulen
from utils import Utility  # Importera Utility-klassen från utils-modulen

class Block(Blocks):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)  # Anropa överordnad klass' init-metod med position och storlek
        block_image = Utility.get_block(size)  # Hämta blockbild med given storlek från Utility
        self.image.blit(block_image, (0, 0)) 
        self.mask = pygame.mask.from_surface(self.image)  # Skapa en mask för kollision med blocket

class SpawnBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)  # Anropa Block-klassens init-metod med position och storlek
        block_image = Utility.get_spawn_block(size)  # Hämta startpunktens bild med given storlek från Utility
        self.image = block_image 
        self.mask = pygame.mask.from_surface(self.image)  # Skapa en mask för kollision med startpunkten

class CheckpointBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)  # Anropa Block-klassens init-metod med position och storlek
        block_image = Utility.get_checkpoint_block(size)  # Hämta kontrollpunktens bild med given storlek från Utility
        self.image = block_image  
        self.mask = pygame.mask.from_surface(self.image)  # Skapa en mask för kollision med kontrollpunkten

class GoalBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)  # Anropa Block-klassens init-metod med position och storlek
        block_image = Utility.get_goal_block(size)  # Hämta målpunktens bild med given storlek från Utility
        self.image = block_image  
        self.mask = pygame.mask.from_surface(self.image)  # Skapa en mask för kollision med målpunkten

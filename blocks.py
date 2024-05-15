import pygame
from sprites import Obstacle # Importerar Obstacle-klassen från modulen sprites
from utils import Utility # Importerar Utility-klassen från modulen utils

class Block(Obstacle): # Klassen Block ärver från Obstacle-klassen
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size) # Anropar superklassens konstruktor med x, y och storleken som parametrar
        block = Utility.get_block(size) # Använder Utility-klassen för att hämta blockbild baserat på storleken
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image) # Skapar en mask för kollision

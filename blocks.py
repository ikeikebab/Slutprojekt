import pygame
from sprites import Obstacle
from utils import Utility

class Block(Obstacle):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = Utility.get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

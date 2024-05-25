import pygame
from sprites import Blocks
from utils import Utility

class Block(Blocks):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_image = Utility.get_block(size)
        self.image.blit(block_image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class SpawnBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        block_image = Utility.get_spawn_block(size)
        self.image = block_image
        self.mask = pygame.mask.from_surface(self.image)

class CheckpointBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        block_image = Utility.get_checkpoint_block(size)
        self.image = block_image
        self.mask = pygame.mask.from_surface(self.image)

class GoalBlock(Block):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        block_image = Utility.get_goal_block(size)
        self.image = block_image
        self.mask = pygame.mask.from_surface(self.image)
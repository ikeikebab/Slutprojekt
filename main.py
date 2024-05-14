import os
import random
import math
import pygame
from player import Player # type: ignore
from level import GameManager
pygame.init()

# Constants
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2
GAME_OVER_SCREEN = 3

# Set up pygame window
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    game_manager = GameManager(window, WIDTH, HEIGHT, FPS)
    game_manager.main()

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()

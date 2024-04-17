import pygame
import os
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platform Game")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    width, height = image.get_rect().size

    tiles = []

    for i in range(0, WIDTH, width):
        for j in range(0, HEIGHT, height):
            pos = (i, j)
            tiles.append(pos)

    return tiles, image 

def draw(window,background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock() 
    background, bg_image = get_background("Gray.png")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_image)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
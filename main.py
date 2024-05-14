import pygame
import os
from os.path import join
from sprites import Player, Obstacle
from utils import Utility
from level import LevelManager, level_manager
from menu import UIManager
from blocks import Fire, Block

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_VEL = 5
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name)).convert()
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Gray.png")

    player = Player(100, 100, 50, 50)  # Instantiate the player

    offset_x = 0
    scroll_area_width = 200

    play_button_icon = pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()

    current_screen = START_SCREEN
    run_game = True  
    game_state = "playing"
    restart = False 
    while run_game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        if current_screen == START_SCREEN:
            current_screen = UIManager.main_menu(window, play_button_icon)
        elif current_screen == LEVEL_SELECTION_SCREEN:
            current_screen, level_definition = UIManager.level_selection(window)
            blocks, fire_positions = level_manager.create_level("level_1")  # Provide level_name
            current_level = 1 if level_definition == level_manager.levels["level_1"] else 2
        elif current_screen == GAME_SCREEN:
            run = True
            while run:
                clock.tick(FPS)

                blocks, fire_positions = level_manager.create_level("level_1")  # Provide level_name

                fires = []

                for fire_position in fire_positions:
                    fire = Fire(fire_position[0], fire_position[1] + 15, 16, 32)
                    fire.on()
                    fires.append(fire)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_game = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player.jump_count < 2:
                            player.jump()

                player.loop(FPS)
                Utility.handle_move(player, blocks)

                for fire in fires:
                    fire.loop()

                for fire in fires:
                    if pygame.sprite.collide_mask(player, fire): # type: ignore
                        player.make_hit()

                draw(window, background, bg_image, player, blocks, offset_x)

                for fire in fires:
                    fire.draw(window, offset_x)

                if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel
                
                if player.rect.bottom > HEIGHT or player.hit:
                    game_state = "game_over"

                if game_state == "game_over":
                    restart = UIManager.game_over_screen(window)
                if restart:
                    UIManager.restart_level(player)
                    game_state = "playing"
                    restart = False 
                else:
                    run_game = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)

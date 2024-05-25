import pygame
from os.path import join
from sprites import GameObject, Player
from utils import Utility
from level import level_manager
from menu import UIManager

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2

import time 

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
    block_size = 96

    player = Player(100, 100, 50, 50)  

    offset_x = 0
    scroll_area_width = 200

    play_button_icon = pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()
    exit_button_icon = pygame.image.load("assets/Menu/Buttons/Close.png").convert_alpha()
    menu_bg, menu_bg_image = get_background("Blue.png")

    current_screen = START_SCREEN
    run_game = True  
    game_state = "playing"
    restart = False 


    start_time = None
    end_time = None
    current_screen = START_SCREEN
    run_game = True

    def draw_timer(window, start_time):
        if start_time:
            elapsed_time = time.time() - start_time
            timer_text = pygame.font.SysFont('Arial', 30).render(f'Time: {elapsed_time:.2f}', True, (255, 255, 255))
            window.blit(timer_text, (10, 10))

    while run_game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        if current_screen == START_SCREEN:
            current_screen = UIManager.main_menu(window, play_button_icon, exit_button_icon, menu_bg, menu_bg_image)
        elif current_screen == LEVEL_SELECTION_SCREEN:
            current_screen, selected_level = UIManager.level_selection(window)
            print(f"Selected level: {selected_level}")
            blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)
            current_level = 1 if selected_level == "level_1" else 2

            if spawn_point:
                player = Player(spawn_point[0], spawn_point[1], 50, 50)
            else:
                player = Player(100, 100, 50, 50)  

        elif current_screen == GAME_SCREEN:
            run = True
            while run:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_game = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player.jump_count < 2:
                            player.jump()
                        if start_time is None and (event.key == pygame.K_a or event.key == pygame.K_d):
                            start_time = time.time()

                player.loop(FPS)
                Utility.handle_move(player, blocks)

                draw(window, background, bg_image, player, blocks, offset_x)
                draw_timer(window, start_time)

                if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                if player.rect.bottom > HEIGHT or player.hit:
                    game_state = "game_over"

                if game_state == "game_over":
                    restart = UIManager.game_over_screen(window)

                if restart:
                    if spawn_point:
                        player.rect.x, player.rect.y = spawn_point
                        start_time = None 
                    else:
                        player.rect.x, player.rect.y = 100, 100  
                        start_time = None 

                    game_state = "playing"
                    restart = False
                else:
                    run_game = False

                if goal_point and player.rect.colliderect(pygame.Rect(goal_point[0], goal_point[1], block_size, block_size)):
                    end_time = time.time()
                    if start_time is not None and end_time is not None:
                     elapsed_time = end_time - start_time
                    print(f"Level completed in {elapsed_time:.2f} seconds")
                    goal_screen_choice = UIManager.goal_screen(window, elapsed_time)

                    if goal_screen_choice == "restart":
                        current_screen = GAME_SCREEN  
                        if spawn_point:
                            player.rect.x, player.rect.y = spawn_point
                        else:
                            player.rect.x, player.rect.y = 100, 100 
                        start_time = None 
                        draw(window, background, bg_image, player, blocks, offset_x)  
                        continue 

                    elif goal_screen_choice == "next_level":
                        current_screen = GAME_SCREEN 
                        selected_level = "level_2"  

                        blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)
                        if spawn_point:
                            player.rect.x, player.rect.y = spawn_point
                        else:
                            player.rect.x, player.rect.y = 100, 100  

                    start_time = None 

                    continue 


    pygame.quit()

if __name__ == "__main__":
    main(window)


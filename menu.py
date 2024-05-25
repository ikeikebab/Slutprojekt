import pygame
from level import LevelManager

WIDTH, HEIGHT = 1280, 720
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2

class UIManager:
    # Skapa en instans av LevelManager-klassen
    level_manager = LevelManager()

    @staticmethod
    def draw_menu(window, play_button_icon, exit_button_icon, menu_bg, menu_bg_image):

        for tile in menu_bg:
            window.blit(menu_bg_image, tile)
        

        font = pygame.font.Font(None, 72)
        title_text = font.render("Frog Jumper", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))
        window.blit(title_text, title_rect)
        

        title_bottom = title_rect.bottom
        

        button_y = title_bottom + 50  
        

        center_x = 500
        

        button_x = center_x
        

        play_button_rect = play_button_icon.get_rect(center=(button_x, button_y))
        play_button_rect.size = (300, 150)
        play_button_icon = pygame.transform.scale(play_button_icon, play_button_rect.size)
        window.blit(play_button_icon, play_button_rect)


        exit_button_rect = exit_button_icon.get_rect(center=(button_x, play_button_rect.bottom + 50))
        exit_button_rect.size = (300, 150)
        exit_button_icon = pygame.transform.scale(exit_button_icon, exit_button_rect.size)
        window.blit(exit_button_icon, exit_button_rect)

        pygame.display.update()

        return play_button_rect, exit_button_rect

    @staticmethod
    def main_menu(window, play_button_icon, exit_button_icon, menu_bg, menu_bg_image):
        play_button_rect, exit_button_rect = UIManager.draw_menu(window, play_button_icon, exit_button_icon, menu_bg, menu_bg_image)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()

                        if play_button_rect.collidepoint(mouse_pos):
                            UIManager.draw_level_selection(window)
                            return LEVEL_SELECTION_SCREEN

                        elif exit_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            quit()

            pygame.display.update()

    @staticmethod
    def draw_level_selection(window):
        UIManager.level_manager = LevelManager() 
        UIManager.level_manager.add_level("level_1", UIManager.level_manager.import_level_definitions("level1.json"))
        UIManager.level_manager.add_level("level_2", UIManager.level_manager.import_level_definitions("level2.json"))

        level1_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(window, (255, 255, 255), level1_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Level 1", True, (0, 0, 0))
        window.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))

        level2_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(window, (255, 255, 255), level2_button_rect)
        text = font.render("Level 2", True, (0, 0, 0))
        window.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 + 60))

        pygame.display.update()

    @staticmethod
    def level_selection(window):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()

                        if (WIDTH // 2 - 100) <= mouse_pos[0] <= (WIDTH // 2 + 100) and \
                                (HEIGHT // 2 - 50) <= mouse_pos[1] <= (HEIGHT // 2 + 0):
                            return GAME_SCREEN, "level_1" 

                        elif (WIDTH // 2 - 100) <= mouse_pos[0] <= (WIDTH // 2 + 100) and \
                                (HEIGHT // 2 + 50) <= mouse_pos[1] <= (HEIGHT // 2 + 100):
                            return GAME_SCREEN, "level_2"  


            pygame.display.update()

    @staticmethod
    def game_over_screen(window):
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        restart_text = font.render("Restart", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        window.fill((0, 0, 0))
        window.blit(game_over_text, game_over_rect)
        pygame.draw.rect(window, (0, 128, 0), restart_rect)
        window.blit(restart_text, restart_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if restart_rect.collidepoint(mouse_pos):
                            return True
            pygame.display.update()

    @staticmethod
    def restart_level(player):
        # Funktion för att återställa spelarens position och status vid omstart av nivån
        player.rect.x = 100
        player.rect.y = 100
        player.x_vel = 0
        player.y_vel = 0
        player.hit = False
        player.hit_count = 0
        player.animation_count = 0
        player.jump_count = 0
        player.fall_count = 0

    @staticmethod
    def goal_screen(window, elapsed_time):
        font = pygame.font.Font(None, 36)
        finish_time_text = font.render(f"Finish Time: {elapsed_time:.2f} seconds", True, (255, 255, 255))
        restart_text = font.render("Restart", True, (255, 255, 255))
        next_level_text = font.render("Next Level", True, (255, 255, 255))

        finish_time_rect = finish_time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        next_level_rect = next_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

        window.fill((0, 0, 0))
        window.blit(finish_time_text, finish_time_rect)
        pygame.draw.rect(window, (0, 128, 0), restart_rect)
        window.blit(restart_text, restart_rect)
        pygame.draw.rect(window, (0, 128, 0), next_level_rect)
        window.blit(next_level_text, next_level_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if restart_rect.collidepoint(mouse_pos):
                            return "restart"
                        elif next_level_rect.collidepoint(mouse_pos):
                            return "next_level"
            pygame.display.update()



import pygame
from level import LevelManager

WIDTH, HEIGHT = 1280, 720
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2

class UIManager:
    level_manager = LevelManager()  # Instantiate LevelManager

    @staticmethod
    def draw_menu(window, play_button_icon):
        window.fill((0, 0, 0))
        window.blit(play_button_icon, (WIDTH // 2 - 16, HEIGHT // 2 - 16))
        pygame.display.update()

    @staticmethod
    def draw_level_selection(window):
        UIManager.level_manager = LevelManager()  # Re-instantiate LevelManager to ensure fresh data
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
    def main_menu(window, play_button_icon):
        UIManager.draw_menu(window, play_button_icon)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if (WIDTH // 2 - 16) <= mouse_pos[0] <= (WIDTH // 2 + 16) and \
                                (HEIGHT // 2 - 16) <= mouse_pos[1] <= (HEIGHT // 2 + 16):
                            UIManager.draw_level_selection(window)
                            return LEVEL_SELECTION_SCREEN

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
                            return GAME_SCREEN, "level_1"  # Pass level definition for level 1
                        elif (WIDTH // 2 - 100) <= mouse_pos[0] <= (WIDTH // 2 + 100) and \
                                (HEIGHT // 2 + 50) <= mouse_pos[1] <= (HEIGHT // 2 + 100):
                            return GAME_SCREEN, "level_2"  # Pass level definition for level 2


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
        player.rect.x = 100
        player.rect.y = 100
        player.x_vel = 0
        player.y_vel = 0
        player.hit = False
        player.hit_count = 0
        player.animation_count = 0
        player.jump_count = 0
        player.fall_count = 0

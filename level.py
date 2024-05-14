import pygame
from blocks import ObjectManager

class GameManager:
    def __init__(self, window, width, height, fps):
        self.window = window
        self.width = width
        self.height = height
        self.fps = fps
        self.current_screen = 0
        self.play_button_icon = pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()

    def main(self):
        pygame.display.set_caption("Frog Jumper")
        clock = pygame.time.Clock()

        while True:
            if self.current_screen == 0:
                self.current_screen = self.main_menu()
            elif self.current_screen == 1:
                self.current_screen, level_definition = self.level_selection()
                blocks, fire_positions = ObjectManager.create_block(level_definition, self.width, self.height)
            elif self.current_screen == 2:
                self.game(blocks, fire_positions)

            clock.tick(self.fps)

    def draw_menu(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.play_button_icon, (self.width // 2 - 16, self.height // 2 - 16))
        pygame.display.update()

    def draw_level_selection(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Select Level", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.window.blit(text, text_rect)

        level1_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2, 200, 50)
        pygame.draw.rect(self.window, (255, 255, 255), level1_button_rect)
        text = font.render("Level 1", True, (0, 0, 0))
        text_rect = text.get_rect(center=level1_button_rect.center)
        self.window.blit(text, text_rect)

        level2_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 100, 200, 50)
        pygame.draw.rect(self.window, (255, 255, 255), level2_button_rect)
        text = font.render("Level 2", True, (0, 0, 0))
        text_rect = text.get_rect(center=level2_button_rect.center)
        self.window.blit(text, text_rect)

        pygame.display.update()

    def main_menu(self):
        self.draw_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if (self.width // 2 - 16) <= mouse_pos[0] <= (self.width // 2 + 16) and \
                                (self.height // 2 - 16) <= mouse_pos[1] <= (self.height // 2 + 16):
                            self.draw_level_selection()
                            return LEVEL_SELECTION_SCREEN

            pygame.display.update()

    def level_selection(self):
        self.draw_level_selection()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if (self.width // 2 - 100) <= mouse_pos[0] <= (self.width // 2 + 100):
                            if (self.height // 2) <= mouse_pos[1] <= (self.height // 2 + 50):
                                return GAME_SCREEN, level_1_definition
                            elif (self.height // 2 + 100) <= mouse_pos[1] <= (self.height // 2 + 150):
                                return GAME_SCREEN, level_2_definition

            pygame.display.update()

    def game(self, blocks, fire_positions):
        # Your game logic here
        pass

    def game_over_screen(self):
        # Your game over screen logic here
        pass

    def restart_level(self):
        # Your restart level logic here
        pass

# Constants
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2
GAME_OVER_SCREEN = 3

# Level definitions
level_1_definition = [
    "             ",
    "             ",
    "             ",
    "             ",
    "             ",
    "             ",
    "###FFFFFF####",
    "  ########   "
]

level_2_definition = [
    "            ",
    "            ",
    "            ",
    "            ",
    "            ",
    "     ##     ",
    "###FFFFFF###",
    "  ########   "
]

# Initialize and run the game manager
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 800))
    game_manager = GameManager(window, 1000, 800, 60)
    game_manager.main()

import pygame
from os.path import join
from sprites import GameObject, Player
from utils import Utility
from level import level_manager
from menu import UIManager
import time

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.block_size = 96
        self.offset_x = 0
        self.scroll_area_width = 200
        self.play_button_icon = pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()
        self.exit_button_icon = pygame.image.load("assets/Menu/Buttons/Close.png").convert_alpha()
        self.menu_bg, self.menu_bg_image = self.get_background("Blue.png")
        self.current_screen = 0
        self.run_game = True
        self.game_state = "playing"
        self.restart = False
        self.start_time = None

    def get_background(self, name):
        image = pygame.image.load(join("assets", "Background", name)).convert()
        _, _, width, height = image.get_rect()
        tiles = []

        for i in range(self.WIDTH // width + 1):
            for j in range(self.HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)

        return tiles, image

    def draw(self, player, objects):
        for tile in self.background:
            self.window.blit(self.bg_image, tile)

        for obj in objects:
            obj.draw(self.window, self.offset_x)

        player.draw(self.window, self.offset_x)

        pygame.display.update()

    def draw_timer(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            timer_text = pygame.font.SysFont('Arial', 30).render(f'Time: {elapsed_time:.2f}', True, (255, 255, 255))
            self.window.blit(timer_text, (10, 10))

    def main(self):
        while self.run_game:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False

            if self.current_screen == 0:
                self.current_screen = UIManager.main_menu(self.window, self.play_button_icon, self.exit_button_icon, self.menu_bg, self.menu_bg_image)
            elif self.current_screen == 1:
                self.current_screen, selected_level = UIManager.level_selection(self.window)
                print(f"Selected level: {selected_level}")
                blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)
                current_level = 1 if selected_level == "level_1" else 2

                if spawn_point:
                    self.player = Player(spawn_point[0], spawn_point[1], 50, 50)
                else:
                    self.player = Player(100, 100, 50, 50)

                self.background, self.bg_image = self.get_background("Gray.png")

            elif self.current_screen == 2:
                run = True
                while run:
                    self.clock.tick(self.FPS)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            self.run_game = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE and self.player.jump_count < 2:
                                self.player.jump()
                            if self.start_time is None and (event.key == pygame.K_a or event.key == pygame.K_d):
                                self.start_time = time.time()

                    self.player.loop(self.FPS)
                    Utility.handle_move(self.player, blocks)

                    self.draw(self.player, blocks)
                    self.draw_timer()

                    if ((self.player.rect.right - self.offset_x >= self.WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
                            (self.player.rect.left - self.offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
                        self.offset_x += self.player.x_vel

                    if self.player.rect.bottom > self.HEIGHT or self.player.hit:
                        self.game_state = "game_over"

                    if self.game_state == "game_over":
                        self.restart = UIManager.game_over_screen(self.window)

                    if self.restart:
                        if spawn_point:
                            self.player.rect.x, self.player.rect.y = spawn_point
                            self.start_time = None
                        else:
                            self.player.rect.x, self.player.rect.y = 100, 100
                            self.start_time = None

                        self.game_state = "playing"
                        self.restart = False
                    else:
                        self.run_game = False

                    if goal_point and self.player.rect.colliderect(pygame.Rect(goal_point[0], goal_point[1], self.block_size, self.block_size)):
                        end_time = time.time()
                        if self.start_time is not None and end_time is not None:
                            elapsed_time = end_time - self.start_time
                        print(f"Level completed in {elapsed_time:.2f} seconds")
                        goal_screen_choice = UIManager.goal_screen(self.window, elapsed_time)

                        if goal_screen_choice == "restart":
                            self.current_screen = 2
                            if spawn_point:
                                self.player.rect.x, self.player.rect.y = spawn_point
                            else:
                                self.player.rect.x, self.player.rect.y = 100, 100
                            self.start_time = None
                            self.draw(self.player, blocks)
                            continue

                        elif goal_screen_choice == "next_level":
                            self.current_screen = 2
                            selected_level = "level_2"

                            blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)
                            if spawn_point:
                                self.player.rect.x, self.player.rect.y = spawn_point
                            else:
                                self.player.rect.x, self.player.rect.y = 100, 100

                        self.start_time = None

                        continue

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.main()

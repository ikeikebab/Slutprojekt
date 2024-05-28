import pygame
from os.path import join
from sprites import Player
from utils import Utility
from level import level_manager
from menu import UIManager
import time

class Game:
    def __init__(self):
        # Initiera pygame
        pygame.init()

        # Fönsterinställningar
        self.WIDTH, self.HEIGHT = 1280, 720  # Fönstrets storlek
        self.FPS = 60  # Bilduppdateringshastighet
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Skapa fönstret
        self.clock = pygame.time.Clock()  # Skapa en klocka för att styra FPS
        self.block_size = 96  # Storlek på spelblock
        self.offset_x = 0  # X-axelns förskjutning för kameran
        self.scroll_area_width = 200  # Bredden på området där kameran följer spelaren
        self.play_button_icon = pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()  # Spelknappens ikon
        self.exit_button_icon = pygame.image.load("assets/Menu/Buttons/Close.png").convert_alpha()  # Avslutningsknappens ikon
        self.menu_bg, self.menu_bg_image = self.get_background("Blue.png")  # Bakgrund för meny
        self.current_screen = 0  # Aktuell skärm: 0 - huvudmeny, 1 - nivåval, 2 - spel
        self.run_game = True  # Kontrollvariabel för huvudspelloopen
        self.game_state = "playing"  # Spelstatus: playing - spel pågår, game_over - spel förlorat
        self.restart = False  # Kontrollvariabel för att återstarta spelet
        self.start_time = None  # Variabel för att hålla reda på starttiden för en nivå

    def get_background(self, name):
        # Funktion för att hämta bakgrundsbild och dess tile-koordinater
        image = pygame.image.load(join("assets", "Background", name)).convert()
        _, _, width, height = image.get_rect()
        tiles = []

        for i in range(self.WIDTH // width + 1):
            for j in range(self.HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)

        return tiles, image

    def draw(self, player, objects):
        # Funktion för att rita spelobjekt på skärmen
        # Rita bakgrund
        for tile in self.background:
            self.window.blit(self.bg_image, tile)

        # Rita spelobjekt
        for obj in objects:
            obj.draw(self.window, self.offset_x)

        # Rita spelaren
        player.draw(self.window, self.offset_x)

        pygame.display.update()

    def draw_timer(self):
        # Funktion för att rita tidräknaren på skärmen
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            timer_text = pygame.font.SysFont('Arial', 30).render(f'Tid: {elapsed_time:.2f}', True, (255, 255, 255))
            self.window.blit(timer_text, (10, 10))

    def main(self):
        # Huvudspelloopen
        while self.run_game:
            self.clock.tick(self.FPS)  # Kontrollera FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False  # Avsluta spelet om fönstret stängs

            if self.current_screen == 0:
                # Huvudmeny
                self.current_screen = UIManager.main_menu(self.window, self.play_button_icon, self.exit_button_icon, self.menu_bg, self.menu_bg_image)
            elif self.current_screen == 1:
                # Nivåval
                self.current_screen, selected_level = UIManager.level_selection(self.window)
                print(f"Vald nivå: {selected_level}")
                blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)
                current_level = 1 if selected_level == "level_1" else 2

                if spawn_point:
                    self.player = Player(spawn_point[0], spawn_point[1], 50, 50)  # Skapa spelaren vid spawnpoint
                else:
                    self.player = Player(100, 100, 50, 50)  # Annars skapa spelaren vid standardposition

                self.background, self.bg_image = self.get_background("Gray.png")  # Ladda bakgrund för nivån

            elif self.current_screen == 2:
                # Spel
                run = True
                while run:
                    self.clock.tick(self.FPS)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            self.run_game = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE and self.player.jump_count < 2:
                                self.player.jump()  # Spelaren hoppar om mellanslag trycks och hoppräknaren är mindre än 2
                            if self.start_time is None and (event.key == pygame.K_a or event.key == pygame.K_d):
                                self.start_time = time.time()  # Starta tidtagning när A eller D trycks för första gången

                    self.player.loop(self.FPS)  # Uppdatera spelarens rörelse
                    Utility.handle_move(self.player, blocks)  # Hantera spelarens kollision med block

                    self.draw(self.player, blocks)  # Rita spelare och block på skärmen
                    self.draw_timer()  # Rita tidräknaren på skärmen

                    # Kamerarörelse för att följa spelaren
                    if ((self.player.rect.right - self.offset_x >= self.WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
                            (self.player.rect.left - self.offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
                        self.offset_x += self.player.x_vel

                    # Kontrollera om spelaren har förlorat
                    if self.player.rect.bottom > self.HEIGHT or self.player.hit:
                        self.game_state = "game_over"

                    # Visa Game Over-skärm om spelaren förlorar
                    if self.game_state == "game_over":
                        self.restart = UIManager.game_over_screen(self.window)

                    # Starta om spelet om spelaren vill
                    if self.restart:
                        if spawn_point:
                            self.player.rect.x, self.player.rect.y = spawn_point
                            self.start_time = None
                        else:
                            self.player.rect.x, self.player.rect.y = 100, 100
                            self.start_time = None

                        self.game_state = "playing"  # Återställ spelstatus till "playing"
                        self.restart = False  # Återställ restart-flaggan

                    # Om spelet inte är över och spelaren inte vill starta om, avsluta spelet
                    else:
                        self.run_game = False

                    # Kontrollera om spelaren har nått målet
                    if goal_point and self.player.rect.colliderect(pygame.Rect(goal_point[0], goal_point[1], self.block_size, self.block_size)):
                        end_time = time.time()  # Sluta mäta tiden när målet nås
                        if self.start_time is not None and end_time is not None:
                            elapsed_time = end_time - self.start_time  # Beräkna tiden som det tog att klara nivån
                        print(f"Nivån klar på {elapsed_time:.2f} sekunder")
                        goal_screen_choice = UIManager.goal_screen(self.window, elapsed_time)  # Visa målskärmen och få spelarens val

                        if goal_screen_choice == "restart":
                            self.current_screen = 2  # Återgå till spelet
                            if spawn_point:
                                self.player.rect.x, self.player.rect.y = spawn_point
                            else:
                                self.player.rect.x, self.player.rect.y = 100, 100
                            self.start_time = None  # Återställ starttiden och rita om spelet
                            self.draw(self.player, blocks)
                            continue  # Fortsätt till nästa iteration av spel-loopen

                        elif goal_screen_choice == "next_level":
                            self.current_screen = 2  # Återgå till spelet
                            selected_level = "level_2"  # Ladda nästa nivå

                            blocks, spawn_point, checkpoints, goal_point = level_manager.create_level(selected_level)  # Skapa nästa nivå
                            if spawn_point:
                                self.player.rect.x, self.player.rect.y = spawn_point  # Flytta spelaren till spawnpoint
                            else:
                                self.player.rect.x, self.player.rect.y = 100, 100  # Annars flytta spelaren till standardposition

                        self.start_time = None  # Återställ starttiden för nästa nivå

                        continue  # Fortsätt till nästa iteration av spel-loopen

        pygame.quit()  # Avsluta pygame när spelet är slut

if __name__ == "__main__":
    game = Game()  # Skapa ett Game-objekt
    game.main()  # Starta huvudspelloopen
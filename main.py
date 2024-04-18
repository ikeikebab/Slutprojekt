import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Frog Jumper")

WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_VEL = 5
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2


window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0


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


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            if pygame.sprite.collide_mask(player, obj):
                player.make_hit()


def create_level(level_definition):
    blocks = []
    block_size = 96
    fire_positions = []  

    for row_index, row in enumerate(level_definition):
        for col_index, symbol in enumerate(row):
            x = col_index * block_size
            y = row_index * block_size
            if symbol == "#":
                block = Block(x, y, block_size)
                blocks.append(block)
            elif symbol == "F":
                fire_positions.append((x, y))  

    return blocks, fire_positions

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

def draw_menu(window, play_button_icon):
    window.fill((0, 0, 0))
    window.blit(play_button_icon, (WIDTH // 2 - 16, HEIGHT // 2 - 16))
    pygame.display.update()

def draw_level_selection(window):
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

def main_menu(window, play_button_icon):
    draw_menu(window, play_button_icon)
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
                        draw_level_selection(window)
                        return LEVEL_SELECTION_SCREEN

        pygame.display.update()
                    
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
                        return GAME_SCREEN, level_1_definition
                    elif (WIDTH // 2 - 100) <= mouse_pos[0] <= (WIDTH // 2 + 100) and \
                            (HEIGHT // 2 + 50) <= mouse_pos[1] <= (HEIGHT // 2 + 100):
                        return GAME_SCREEN, level_2_definition

        pygame.display.update()


def game(window):
    pass

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

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Gray.png")

    block_size = 96

    player = Player(100, 100, 50, 50)

    offset_x = 0
    scroll_area_width = 200

    play_button_icon = pygame.image.load(os.path.join("assets", "Menu", "Buttons", "Play.png")).convert_alpha()

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
            current_screen = main_menu(window, play_button_icon)
        elif current_screen == LEVEL_SELECTION_SCREEN:
            current_screen, level_definition = level_selection(window)
            blocks, fire_positions = create_level(level_definition)
            current_level = 1 if level_definition == level_1_definition else 2
        elif current_screen == GAME_SCREEN:
            run = True
            while run:
                clock.tick(FPS)

                blocks, fire_positions = create_level(level_definition)

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
                handle_move(player, blocks)

                for fire in fires:
                    fire.loop()

                for fire in fires:
                    if pygame.sprite.collide_mask(player, fire):
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
                    restart = game_over_screen(window)
                if restart:
                    restart_level(player)
                    game_state = "playing"
                    restart = False  it
                else:
                    run_game = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)

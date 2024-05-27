import pygame
from utils import Utility

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # Skapa en yta för objektet med önskad färg och storlek
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # Skapa en rektangel för objektets position och storlek
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, offset_x):
        # Rita objektet på skärmen med given förskjutning
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Blocks(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 0, 0))
        # Fyll ytan med transparent färg för att göra blocket osynligt
        self.image.fill((0, 0, 0, 0)) 
        # Skapa en mask för kollision med blocket
        self.mask = pygame.mask.from_surface(self.image)

class Character:
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        # Skapa en rektangel för karaktärens position och storlek
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
        self.max_fall_speed = 10

    def apply_gravity(self):
        # Applicera gravitation på karaktären för att få den att falla
        if self.y_vel < self.max_fall_speed:
            self.y_vel += self.GRAVITY

    def jump(self):
        # Utför ett hopp genom att ändra karaktärens vertikala hastighet
        self.y_vel = -self.GRAVITY * 12
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        # Flytta karaktären med givna förändringar i position
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        # Sätt karaktärens träff-flagga till sann
        self.hit = True

    def move_left(self, vel):
        # Rör karaktären åt vänster med given hastighet
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        # Rör karaktären åt höger med given hastighet
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        # Uppdatera karaktärens position och animation vid varje spel-loop
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
        # Återställ variabler när karaktären landar på marken
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def is_landed(self, objects):
        # Kontrollera om karaktären står på marken genom att kolla kollision med objekt
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj) and self.rect.bottom == obj.rect.top:
                return True
        return False

    def update_sprite(self):
        # Uppdatera karaktärens sprite baserat på dess tillstånd och riktning
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
        sprites = self.SPRITES[sprite_sheet_name]  # type: ignore
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        # Uppdatera karaktärens rektangel och mask baserat på dess sprite
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


class Player(Character):
    COLOR = (255, 0, 0)
    # Ladda in spelarens sprites från spritearkivet
    SPRITES = Utility.load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.direction = "left" 

    def draw(self, win, offset_x):
        # Rita spelaren på skärmen med given förskjutning
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


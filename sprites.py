import pygame
from utils import Utility

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Player(GameObject):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = Utility.load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
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
        if self.y_vel < self.max_fall_speed:
            self.y_vel += self.GRAVITY


    def jump(self):
        self.y_vel = -self.GRAVITY * 12
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
        # Funktion för att ange att spelaren har landat
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    
    def is_landed(self, objects):
        # Kolla om spelaren har landat på något objekt
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj) and self.rect.bottom == obj.rect.top:
                return True
        return False

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        # Uppdatera spelarens sprite baserat på dess tillstånd och riktning
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
        # Uppdatera rektangeln och masken baserat på den aktuella spriten
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Blocks(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 0, 0))
        self.image.fill((0, 0, 0, 0))  # Clear the existing image
        self.mask = pygame.mask.from_surface(self.image)

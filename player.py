import os
import math 
import pygame 
from os import listdir
from os.path import isfile, join
from spriteutils import load_sprite_sheets

class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    gravity = 1
    sprites = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0 

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

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
    
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x

    def loop(self, fps):
        #self.y_vel += min(1, (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1

    def draw(self, win):
        if self.direction == "left":
            self.sprite = self.sprites["idle_left"][0]
        elif self.direction == "right":
            self.sprite = self.sprites["idle_right"][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))


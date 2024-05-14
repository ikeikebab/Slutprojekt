import pygame

# Constants
START_SCREEN = 0
LEVEL_SELECTION_SCREEN = 1
GAME_SCREEN = 2
GAME_OVER_SCREEN = 3

# Set up pygame window
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

class CollisionHandler:
    def __init__(self, player, objects):
        self.player = player
        self.objects = objects

    def handle_vertical_collision(self, dy):
        collided_objects = []
        for obj in self.objects:
            if pygame.sprite.collide_mask(self.player, obj):
                if dy > 0:
                    self.player.rect.bottom = obj.rect.top
                    self.player.landed()
                elif dy < 0:
                    self.player.rect.top = obj.rect.bottom
                    self.player.hit_head()

                collided_objects.append(obj)

        return collided_objects

    def collide(self, dx):
        self.player.move(dx, 0)
        self.player.update()
        collided_object = None
        for obj in self.objects:
            if pygame.sprite.collide_mask(self.player, obj):
                collided_object = obj
                break

        self.player.move(-dx, 0)
        self.player.update()
        return collided_object

    def handle_move(self):
        keys = pygame.key.get_pressed()

        self.player.x_vel = 0
        collide_left = self.collide(-PLAYER_VEL * 2)
        collide_right = self.collide(PLAYER_VEL * 2)

        if keys[pygame.K_a] and not collide_left:
            self.player.move_left(PLAYER_VEL)
        if keys[pygame.K_d] and not collide_right:
            self.player.move_right(PLAYER_VEL)

        vertical_collide = self.handle_vertical_collision(self.player.y_vel)
        to_check = [collide_left, collide_right, *vertical_collide]

        for obj in to_check:
            if obj and obj.name == "fire":
                if pygame.sprite.collide_mask(self.player, obj):
                    self.player.make_hit()

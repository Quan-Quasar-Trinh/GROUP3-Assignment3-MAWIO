import pygame
from entity.obj import Object

class Star(Object):
    def __init__(self, x, y):
        width, height = 16, 16
        super().__init__(x, y, width, height, "Star")
        self.image = pygame.image.load("assets/img/star.png").convert_alpha()
        self.vy = -3
        self.gravity = 0.2

    def update(self, floor):
        self.vy += self.gravity
        self.rect.y += self.vy

        # for block in floor:
        #     if self.rect.colliderect(block.rect) and self.vy > 0:
        #         self.rect.bottom = block.rect.top
        #         self.vy = 0

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

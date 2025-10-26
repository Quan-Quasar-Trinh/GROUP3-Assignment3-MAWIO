import pygame
from entity.obj import Object
from entity.star import Star

class Container(Object):
    def __init__(self, x, y, width, height, image_active, image_used):
        super().__init__(x, y, width, height, "Container")

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
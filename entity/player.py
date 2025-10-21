import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

from entity.obj import Object


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(path, width, height, direction=False):
    
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

class Player(Object):
    GRAVITY = 1
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "player")
        self.rect = pygame.Rect(x, y, width, height)
        self.vx = 0
        self.vy = 0
        self.direction = "right"
        self.on_ground = False
        self.jump_count = 0
        self.fall_count = 0
        self.hit = False
        self.animation_count = 0
        
        
        self.SPRITES = load_sprite_sheets(join("assets", "img", "player"), 32, 32, True)

        
        
    def loop(self, fps):
        # Apply gravity
        self.vy += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.vx, self.vy)
        self.fall_count += 1
        
        self.update_sprite()
        
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def move_left(self, vel):
        self.vx = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.vx = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    def jump(self):
        self.vy = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
            
    def landed(self):
        self.fall_count = 0
        self.vy = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.vy *= -1
        
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.vy < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.vy > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.vx != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.image = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
        self.animation_count += 1
        self.update()

    def update(self):
        
        self.mask = pygame.mask.from_surface(self.sprite)
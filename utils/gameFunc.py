import pygame
import sys
import os
from os.path import join

def get_background(name,WIDTH,HEIGHT):
    image = pygame.image.load(join("assets","img","BG","game_bg",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(base_surface, bg_tiles, bg_image, setting, gear_img, gear_rect, BASE_WIDTH, BASE_HEIGHT, font, sound_volume, back_button, menu_button, res_button, vol_minus, vol_plus, WIDTH, HEIGHT, screen):
    for pos in bg_tiles:
        base_surface.blit(bg_image, pos)
        
    
    
    
    
    if setting:
        # Transparent overlay
        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        base_surface.blit(overlay, (0, 0))

        center_x = BASE_WIDTH // 2
        label_x = BASE_WIDTH * 0.3
        control_x = BASE_WIDTH * 0.6
        line_gap = BASE_HEIGHT * 0.15

        title = font.render("Settings", True, (255, 255, 255))
        base_surface.blit(title, (center_x - title.get_width() // 2, BASE_HEIGHT * 0.1))

        res_label = font.render("Resolution:", True, (255, 255, 255))
        res_y = BASE_HEIGHT * 0.35
        base_surface.blit(res_label, (label_x - res_label.get_width() // 2, res_y))
        res_button.rect.center = (control_x, res_y + res_label.get_height() // 2)
        res_button.draw(base_surface)

        sound_label = font.render("Sound:", True, (255, 255, 255))
        sound_y = res_y + line_gap
        base_surface.blit(sound_label, (label_x - sound_label.get_width() // 2, sound_y))
        vol_text = font.render(f"{sound_volume}%", True, (255, 255, 255))
        gap = BASE_WIDTH * 0.04
        vol_minus.rect.center = (control_x - vol_text.get_width() - gap, sound_y)
        vol_plus.rect.center = (control_x + vol_text.get_width() + gap, sound_y)
        vol_minus.draw(base_surface)
        vol_plus.draw(base_surface)
        base_surface.blit(vol_text, (control_x - vol_text.get_width() // 2, sound_y - vol_text.get_height() // 2))

        back_button.rect.center = (center_x, sound_y + line_gap * 1.5)
        back_button.draw(base_surface)

        menu_button.rect.center = (center_x, sound_y + line_gap * 2.3)
        menu_button.draw(base_surface)

    else:
        base_surface.blit(gear_img, gear_rect)

    # --- Scale and draw to actual screen (keep 16:9 ratio) ---
    window_ratio = WIDTH / HEIGHT
    target_ratio = 16 / 9

    if window_ratio > target_ratio:
        # too wide → add side bars
        scaled_height = HEIGHT
        scaled_width = int(HEIGHT * target_ratio)
        offset_x = (WIDTH - scaled_width) // 2
        offset_y = 0
    else:
        # too tall → add top/bottom bars
        scaled_width = WIDTH
        scaled_height = int(WIDTH / target_ratio)
        offset_x = 0
        offset_y = (HEIGHT - scaled_height) // 2

    scaled_surface = pygame.transform.smoothscale(base_surface, (scaled_width, scaled_height))
    screen.fill((0, 0, 0))  # letterbox background
    screen.blit(scaled_surface, (offset_x, offset_y))

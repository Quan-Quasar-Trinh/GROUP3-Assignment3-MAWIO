import pygame
import sys
from utils.gameFunc import draw, get_background
from utils.button import Button

def game(WIDTH, HEIGHT, sound_volume, level=1):
    pygame.init()
    pygame.display.set_caption("Game Loop")

    BASE_WIDTH, BASE_HEIGHT = 1280, 720  # internal 16:9 resolution
    base_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    setting = False

    # --- Load background and gear icon ---
    bg_tiles, bg_image = get_background("Blue.png", BASE_WIDTH, BASE_HEIGHT)
    gear_img = pygame.image.load("assets/img/icon/setting.png")
    gear_size = int(BASE_WIDTH * 0.04)
    gear_img = pygame.transform.scale(gear_img, (gear_size, gear_size))
    gear_rect = gear_img.get_rect(topright=(BASE_WIDTH - 20, 20))

    # --- Settings data ---
    resolutions = [
        (640, 360),
        (854, 480),
        (960, 540),
        (1024, 576),
        (1152, 648),
        (1280, 720)
    ]
    current_res_index = resolutions.index((WIDTH, HEIGHT)) if (WIDTH, HEIGHT) in resolutions else 5

    # --- Font ---
    font_size = int(BASE_WIDTH * 0.04)
    font = pygame.font.Font(None, font_size)

    # --- Settings buttons ---
    def make_settings_buttons():
        return (
            Button("Back", (BASE_WIDTH // 2 - int(BASE_WIDTH * 0.1), int(BASE_HEIGHT * 0.8)), (BASE_WIDTH * 0.2, BASE_HEIGHT * 0.08)),
            Button("Return to Menu", (BASE_WIDTH // 2 - int(BASE_WIDTH * 0.1), int(BASE_HEIGHT * 0.9)), (BASE_WIDTH * 0.25, BASE_HEIGHT * 0.08)),
            Button(f"{resolutions[current_res_index][0]}x{resolutions[current_res_index][1]}",
                   (BASE_WIDTH // 2 - BASE_WIDTH * 0.1, BASE_HEIGHT * 0.4), (BASE_WIDTH * 0.25, BASE_HEIGHT * 0.08)),
            Button("-", (BASE_WIDTH // 2 - BASE_WIDTH * 0.15, BASE_HEIGHT * 0.55), (BASE_WIDTH * 0.06, BASE_WIDTH * 0.06)),
            Button("+", (BASE_WIDTH // 2 + BASE_WIDTH * 0.09, BASE_HEIGHT * 0.55), (BASE_WIDTH * 0.06, BASE_WIDTH * 0.06))
        )

    back_button, menu_button, res_button, vol_minus, vol_plus = make_settings_buttons()
    
    def load_level(level):
        print(f"Loading level {level}...")
        
    
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if setting:
                        setting = False
                    else:
                        return "menu", WIDTH, HEIGHT, sound_volume, 1
                #dev cheat
                elif event.key == pygame.K_l:
                    level += 1
                    print(f"Level increased to {level}")
                    return "game", WIDTH, HEIGHT, sound_volume, level

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Adjust mouse for scale
                scale_x = BASE_WIDTH / WIDTH
                scale_y = BASE_HEIGHT / HEIGHT
                adj_mouse = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)

                if setting:
                    if back_button.is_clicked(adj_mouse):
                        setting = False
                    elif menu_button.is_clicked(adj_mouse):
                        return "menu", WIDTH, HEIGHT, sound_volume, 1
                    elif res_button.is_clicked(adj_mouse):
                        current_res_index = (current_res_index + 1) % len(resolutions)
                        WIDTH, HEIGHT = resolutions[current_res_index]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        res_button.text = f"{WIDTH}x{HEIGHT}"
                    elif vol_minus.is_clicked(adj_mouse):
                        sound_volume = max(0, sound_volume - 10)
                    elif vol_plus.is_clicked(adj_mouse):
                        sound_volume = min(100, sound_volume + 10)
                else:
                    if gear_rect.collidepoint(adj_mouse):
                        setting = True
        # --- Drawing ---
        draw(base_surface, bg_tiles, bg_image, setting, gear_img, gear_rect, BASE_WIDTH, BASE_HEIGHT, font, sound_volume, back_button, menu_button, res_button, vol_minus, vol_plus, WIDTH, HEIGHT, screen)

        

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

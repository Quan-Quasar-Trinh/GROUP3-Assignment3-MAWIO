import pygame

class Proj:
    def __init__(self, x, y, ally, special, direction):
        self.x = x
        self.y = y
        self.ally = ally
        self.special = special
        if direction == "left":
            self.direction_left = True
        elif direction == "right":
            self.direction_left = False
        
        
        self.width = 20
        self.height = 4
        self.speed = 10

        # --- Assign color once ---
        if self.ally and not self.special:
            self.color = (0, 128, 255)      # Blue - ally normal
        elif self.ally and self.special:
            self.color = (0, 255, 100)      # Green - ally special
        elif not self.ally and not self.special:
            self.color = (255, 50, 50)      # Red - enemy normal
        else:
            self.color = (180, 0, 255)      # Purple - enemy special

    def update(self):
        """Move projectile based on direction."""
        if self.direction_left:
            self.x -= self.speed
        else:
            self.x += self.speed
        

    def draw(self, surface, offsetX, offsetY):
        """Draw projectile as a thin rectangle."""
        rect = pygame.Rect(
            int(self.x - offsetX),
            int(self.y - offsetY),
            self.width,
            self.height
        )
        pygame.draw.rect(surface, self.color, rect)

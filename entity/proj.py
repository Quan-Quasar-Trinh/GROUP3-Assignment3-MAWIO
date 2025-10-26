import pygame

class Proj:
    def __init__(self, x, y, ally, special, direction, dmg = 10):
        self.rect = pygame.Rect(x,y,20,4)
        self.destroyed = False
        self.ally = ally
        self.special = special
        if direction == "left":
            self.direction_left = True
        elif direction == "right":
            self.direction_left = False
        
        
        
        self.speed = 10

        self.dmg = dmg
        
        # --- Assign color once ---
        if self.ally and not self.special:
            self.color = (0, 128, 255)      # Blue - ally normal
        elif self.ally and self.special:
            self.color = (0, 255, 100)      # Green - ally special
        elif not self.ally and not self.special:
            self.color = (255, 50, 50)      # Red - enemy normal
        else:
            self.color = (180, 0, 255)      # Purple - enemy special

    def update(self, objs, player, nor, spe):
        """Move projectile based on direction."""
        if self.direction_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        #Collision to wall
        for terrain in objs:
            if self.rect.colliderect(terrain.rect):
                self.destroyed = True
                if self.special:
                    print("removed spe(Wall)")
                else:
                    print("remove Nor(Wall)")
                return
            
        #Collision to Player/Enemy
        if not self.ally:
            if self.rect.colliderect(player.rect):
                self.destroyed = True
                player.HP -= self.dmg
                if player.HP<0:
                    player.HP = 0
        else:
            pass
        
        

    def draw(self, surface, offsetX, offsetY):
        """Draw projectile as a thin rectangle."""
        rect = pygame.Rect(
            int(self.rect.x - offsetX),
            int(self.rect.y - offsetY),
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(surface, self.color, rect)

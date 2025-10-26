import pygame
from entity.obj import Object
from entity.star import Star

class Container(Object):
    def __init__(self, x, y, volume=100):
        super().__init__(x, y, 48, 48, "Container")

        # Load terrain sprite sheet
        terrain_image = pygame.image.load("assets/img/block/Terrain.png").convert_alpha()

        # Pick a nice yellow container tile (adjust coordinates as needed)
        self.block_img = terrain_image.subsurface(pygame.Rect(0, 0, 48, 48))

        # State
        self.used = False
        self.visible = True       # new: disappears after bounce done
        self.star_spawned = False
        self.star = None
        self.volume = volume

        # Bounce animation
        self.bounce_offset = 0
        self.bouncing = False
        self.bounce_speed = -4
        self.bounce_height = 10
        self.original_y = y

    def hit_from_below(self, player):
        """Triggered when the player jumps and hits the container from below."""
        if not self.used:
            self.used = True
            self.bouncing = True

            # Spawn star slightly above the block
            self.star = Star(self.rect.centerx - 16, self.rect.y - 60, self.volume)
            self.star_spawned = True
            print("⭐ Star released!")

    def update(self, player):
        """Update bounce and star movement."""
        # Handle bounce animation
        if self.bouncing:
            self.rect.y += self.bounce_speed
            self.bounce_offset += abs(self.bounce_speed)

            # Reverse direction at max height
            if self.bounce_offset >= self.bounce_height:
                self.bounce_speed *= -1

            # Stop when back to original position
            if self.bounce_speed > 0 and self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.bouncing = False
                self.bounce_speed = -4
                self.bounce_offset = 0

                # Disappear after bounce ends
                self.visible = False

        # Update star
        if self.star_spawned and self.star:
            self.star.update(player)

    def draw(self, screen, camera_x, camera_y):
        """Draw the container block and its star (if visible)."""
        if self.visible:
            screen.blit(
                self.block_img,
                (self.rect.x - camera_x, self.rect.y - camera_y)
            )

        if self.star_spawned and self.star:
            self.star.draw(screen, camera_x, camera_y)

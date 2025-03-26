import pygame
from constants import *
from variables import *
############################################################################################################
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load both walking images
        self.walk_images = [
            pygame.image.load('Images/PNG/Zombie/Poses/zombie_walk1.png').convert_alpha(),
            pygame.image.load('Images/PNG/Zombie/Poses/zombie_walk2.png').convert_alpha()
        ]
        self.image_index = 0  # Start with the first image
        self.image = pygame.transform.scale(self.walk_images[self.image_index], (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 100, WIDTH + 300)  # Spawn far from the player
        
        # Position the zombie on the ground
        self.rect.y = HEIGHT - ground_height - self.rect.height  # Adjust for ground height
        self.health = 1 + elapsed_time // 60  # Increase health every minute

        # Timer for animation
        self.last_update = pygame.time.get_ticks()  # Track the last time the image was updated
        self.animation_delay = 500  # 500 milliseconds (0.5 seconds)

    def update(self):
        # Update position
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

        # Handle animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_delay:
            self.last_update = current_time
            self.image_index = (self.image_index + 1) % len(self.walk_images)  # Alternate between 0 and 1
            self.image = pygame.transform.scale(self.walk_images[self.image_index], (50, 100))


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 150))
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 200  # Spawn off-screen
        self.rect.y = HEIGHT - self.rect.height
        self.health = 3 + elapsed_time // 60  # Increase health every minute

    def update(self):
        self.rect.x -= SCROLL_SPEED // 1.5  # Moves slower
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += BULLET_SPEED
        if self.rect.left > WIDTH:
            self.kill()

# Group to hold zombies and bullets
zombies = pygame.sprite.Group()
bosses = pygame.sprite.Group()
bullets = pygame.sprite.Group()
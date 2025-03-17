import pygame
from constants import *
from variables import *
############################################################################################################
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('Images/zombie.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 100, WIDTH + 300)  # Spawn far from the player
        self.rect.y = HEIGHT - self.rect.height
        self.health = 1 + elapsed_time // 60  # Increase health every minute

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

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
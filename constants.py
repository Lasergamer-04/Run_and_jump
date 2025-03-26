import random
import pygame
pygame.init()
pygame.mixer.init()

# Constants
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h

FPS = 60
GRAVITY = 1
JUMP_STRENGTH = 15
SCROLL_SPEED = 5
BULLET_SPEED = 10
OBSTACLE_FREQ_MIN, OBSTACLE_FREQ_MAX = 30, 90
next_obstacle_interval = random.randint(OBSTACLE_FREQ_MIN, OBSTACLE_FREQ_MAX)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)
BROWN = (120, 60, 50)
GREEN = (80, 105, 25)
DARK_GREEN = (0, 100, 0)

# Event Timings
ZOMBIE_WAVE_INTERVAL = 13  # Every 13 seconds
BOSS_FIGHT_INTERVAL = 27  # Every 27 seconds


DATA_FILE = "players.json"
CACHE_FILE = "cache.json"

ground_height = 20

jump_sound_1 = pygame.mixer.Sound('sounds/jump1.wav')
jump_sound_2 = pygame.mixer.Sound('sounds/jump2.wav')
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
death_sound = pygame.mixer.Sound('sounds/death.wav')
random_sound = pygame.mixer.Sound('sounds/random.wav')
music = pygame.mixer.Sound('sounds/music.wav')
#zombie_spawn_sound = pygame.mixer.Sound('sounds/zombie_spawn.wav')
#boss_spawn_sound = pygame.mixer.Sound('sounds/boss_spawn.wav')
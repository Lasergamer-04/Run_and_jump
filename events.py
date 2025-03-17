from sprite import *
import pygame

# Spawn a zombie wave
def spawn_zombie_wave(display_message, screen):
    global zombies
    for _ in range(5):  # Spawn 5 zombies at once
        zombie = Zombie()
        zombies.add(zombie)

# Spawn a boss fight
def spawn_boss_fight(display_message, screen):
    global bosses
    boss = Boss()
    bosses.add(boss)
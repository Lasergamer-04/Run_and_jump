import pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer
import random
import time 
import jumpnrun_register as auth
from constants import *
from sprite import *
from variables import *
from events import *

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run and Jump Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

############################################################################################################
def display_message(screen, message, duration=2):
    font = pygame.font.Font(None, 36)
    message_surface = font.render(message, True, WHITE)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(message_surface, message_rect)
    pygame.display.flip()
    
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration * 1000:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key
    return None

def display_event_message(screen, message, duration=2):
    font = pygame.font.Font(None, 36)
    message_surface = font.render(message, True, WHITE)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(message_surface, message_rect)
    pygame.display.flip()
    
    start_time = pygame.time.get_ticks()
    return message_surface, message_rect, start_time, duration * 1000
############################################################################################################

def login_screen():
     # Check cache for automatic login
    cache = auth.load_cache()
    if cache:
        username = cache["username"]
        player_data = cache["player_data"]
        display_message(screen, "Connexion réussie à partir du cache !") 
        return username, player_data
    
    username = ""
    password = ""
    input_active = "username"
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_font.render("Login", True, WHITE), (100, 50))
        screen.blit(font.render("Username:", True, WHITE), (100, 100))
        screen.blit(font.render(username, True, WHITE), (250, 100))
        screen.blit(font.render("Password:", True, WHITE), (100, 150))
        screen.blit(font.render("*" * len(password), True, WHITE), (250, 150))
        screen.blit(font.render("Press ENTER to login", True, WHITE), (100, 200))
        screen.blit(font.render("Press R to register", True, WHITE), (100, 250))
        screen.blit(font.render("Press ESC to quit", True, WHITE), (100, 300))
        screen.blit(font.render("Press Tab to switch between fields", True, WHITE), (100, 350))

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_data = auth.authentication(username, password)
                    if player_data:
                        return username, player_data
                    else:
                        display_message(screen, "Invalid credentials")
                elif event.key == pygame.K_r:
                    register_screen()
                elif event.key == pygame.K_TAB:
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    if input_active == "username":
                        username += event.unicode
                    else:
                        password += event.unicode

def register_screen():
    username = ""
    password = ""
    input_active = "username"
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_font.render("Register", True, WHITE), (100, 50))
        screen.blit(font.render("Username:", True, WHITE), (100, 100))
        screen.blit(font.render(username, True, WHITE), (250, 100))
        screen.blit(font.render("Password:", True, WHITE), (100, 150))
        screen.blit(font.render("*" * len(password), True, WHITE), (250, 150))
        screen.blit(font.render("Press ENTER to register", True, WHITE), (100, 200))
        screen.blit(font.render("Press ESC to return to login", True, WHITE), (100, 250))
        screen.blit(font.render("Press Tab to switch between fields", True, WHITE), (100, 300))

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if auth.register(username, password):
                        display_message(screen, "Registration successful")
                        return
                    else:
                        if username in auth.load_players():
                            display_message(screen, "Username already exists")
                        else:
                            display_message(screen, "Registration failed, Try again")
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_TAB:
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]
                else:
                    if input_active == "username":
                        username += event.unicode
                    else:
                        password += event.unicode

############################################################################################################
class Player:
    def __init__(self, data):
        self.health = data["health"]
        self.health_lvl = data["health_lvl"]
        self.strength = data["strength"]
        self.strength_lvl = data["strength_lvl"]
        self.shooting = data["shooting"]
        self.shooting_lvl = data["shooting_lvl"]
        self.coins = data["coins"]
        self.total_jump = data["total_jump"]
        self.total_kill = data["total_kill"]
        self.total_death = data["total_death"]

        # Charger et redimensionner les images
        self.walk_images = [
            pygame.transform.scale(
                pygame.image.load('Images/PNG/Soldier/Poses/soldier_walk1.png').convert_alpha(),
                (50, 100)  # Taille souhaitée : largeur=50, hauteur=100
            ),
            pygame.transform.scale(
                pygame.image.load('Images/PNG/Soldier/Poses/soldier_walk2.png').convert_alpha(),
                (50, 100)
            )
        ]
        self.slide_image = pygame.transform.scale(
            pygame.image.load('Images/PNG/Soldier/Poses/soldier_slide.png').convert_alpha(),
            (50, 50)  # Taille pour l'image de glissade
        )
        self.jump_image = pygame.transform.scale(
            pygame.image.load('Images/PNG/Soldier/Poses/soldier_jump.png').convert_alpha(),
            (50, 100)  # Taille pour l'image de saut
        )

        # Initialisation de l'état du joueur
        self.image = self.walk_images[0]  # Image par défaut
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Position initiale en x
        self.rect.y = HEIGHT - ground_height - self.rect.height  # Position initiale en y
        self.state = "walking"  # Default state
        self.image_index = 0  # For walking animation
        self.last_update = pygame.time.get_ticks()  # Timer for animation
        self.animation_delay = 200  # Delay between frames (200 ms)

    def update(self, on_ground, is_crouching, is_jumping):
        # Update player state
        if is_jumping:
            self.state = "jumping"
        elif is_crouching:
            self.state = "sliding"
        else:
            self.state = "walking"

        # Update image based on state
        if self.state == "walking":
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.animation_delay:
                self.last_update = current_time
                self.image_index = (self.image_index + 1) % len(self.walk_images)
                self.image = self.walk_images[self.image_index]
        elif self.state == "jumping":
            self.image = self.jump_image
        elif self.state == "sliding":
            self.image = self.slide_image

        
        # Update rect position and size to match the current image
        previous_bottom = self.rect.bottom  # Sauvegarde la position verticale
        self.rect = self.image.get_rect()  # Met à jour la taille de la hitbox pour correspondre à l'image
        self.rect.x = 100  # Position horizontale fixe
        self.rect.bottom = previous_bottom  # Restaure la position verticale

        # Update vertical position if not on the ground
        if not on_ground:
            self.rect.y += GRAVITY

    def upgrade_health(self):
        self.health += 1
        self.health_lvl += 1
        display_message(screen, f"Health upgraded to {self.health}")

    def upgrade_strength(self):
        self.strength += 0.25
        self.strength_lvl += 1
        display_message(screen, f"Strength upgraded to {self.strength}")

    def upgrade_shooting(self):
        self.shooting -= 0.01
        self.shooting_lvl += 1
        display_message(screen, f"Shooting upgraded to {self.shooting}")

    def save_progress(self):
        global coins_collected, jump_count, kill_count, death_count, score
        players = auth.load_players()  # Load existing player data

        players[username] = {
            "password": players[username]["password"],  # Preserve password
            "health": self.health,
            "health_lvl": self.health_lvl,
            "strength": self.strength,
            "strength_lvl": self.strength_lvl,
            "shooting": self.shooting,
            "shooting_lvl": self.shooting_lvl,
            "coins": self.coins + coins_collected,  # Save total coins
            "total_jump": self.total_jump + jump_count,  # Save total jumps
            "total_kill": self.total_kill + kill_count,  # Save total kills
            "total_death": self.total_death + death_count,  # Save total deaths
            "high_score": max(players[username].get("high_score", 0), score)  # Keep highest score
        }

        auth.save_players(players)  # Save updated player data
        coins_collected = 0  # Reset coins collected

username, player_data = login_screen()  # Authentication
player = Player(player_data)  # Create the player object with the player data

Zombie_wave_time = time.time()
Boss_wave_time = time.time()

############################################################################################################

def handle_events(): 
    global Zombie_wave_time, Boss_wave_time, game_over, message_start_time, message_duration, message_surface, message_rect
    if game_over:
        return
    
    current_time = time.time()
    
    if current_time - Zombie_wave_time > ZOMBIE_WAVE_INTERVAL:
        message_surface, message_rect, message_start_time, message_duration = display_event_message(screen, "🔥 ZOMBIE WAVE STARTS! 🔥")
        spawn_zombie_wave(display_message, screen)
        Zombie_wave_time = current_time

    if current_time - Boss_wave_time > BOSS_FIGHT_INTERVAL:
        message_surface, message_rect, message_start_time, message_duration = display_event_message(screen, "👹 BOSS FIGHT STARTS! 👹")
        spawn_boss_fight(display_message, screen)
        Boss_wave_time = current_time

    # Display the message for the specified duration
    if message_start_time and pygame.time.get_ticks() - message_start_time < message_duration:
        screen.blit(message_surface, message_rect)
        pygame.display.flip()
    else:
        message_start_time = None


def check_boss_shot(bosses, bullets, player):
    global coins_collected
    for boss in bosses.sprites():
        for bullet in bullets.sprites():
            if bullet.rect.colliderect(boss.rect):
                boss.health -= player.strength
                bullet.kill()
                if boss.health <= 0:
                    bosses.remove(boss)
                    coins_collected += 5  # Boss gives 5 coins!

# Function to check if a zombie is shot
def check_zombie_shot(zombies, bullets, player):
    global coins_collected
    for zombie in zombies.sprites():
        for bullet in bullets.sprites():
            if bullet.rect.colliderect(zombie.rect):
                zombie.health -= player.strength
                bullet.kill()
                if zombie.health <= 0:
                    zombies.remove(zombie)
                    coins_collected += 1  # Add coins for each zombie killed
                

############################################################################################################

# Function to render the coin counter
def render_coin_count(screen, coins_collected):
    coin_text = font.render(f"Coins: {coins_collected}", True, (255, 255, 255))
    screen.blit(coin_text, (10, 40))

############################################################################################################
def settings_screen():
    running = True
    while running:
        screen.fill((0, 0, 0))  # Black background

        font = pygame.font.Font(None, 36)
        screen.blit(title_font.render("Settings Menu", True, WHITE), (100, 50))
        screen.blit(font.render("1. Toggle Music", True, WHITE), (100, 100))
        screen.blit(font.render("2. Toggle Sound Effects", True, WHITE), (100, 125))
        #screen.blit(font.render("3. Change Difficulty", True, WHITE), (100, 150))
        screen.blit(font.render("Press ESC to return to menu", True, WHITE), (100, 250))

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_ESCAPE:  # Return to menu
                    return "menu"  # Return to menu

                elif event.key == pygame.K_1:  # Toggle music
                    if music.get_volume() == 0:
                        music.set_volume(1)
                        key = display_message(screen, "Music enabled")
                        if key == pygame.K_ESCAPE:
                            return "menu"
                    else:
                        music.set_volume(0)
                        key = display_message(screen, "Music disabled")
                        if key == pygame.K_ESCAPE:
                            return "menu"
                
                elif event.key == pygame.K_2:  # Toggle sound effects
                    if jump_sound_1.get_volume() == 0:
                        jump_sound_1.set_volume(1)
                        jump_sound_2.set_volume(1)
                        shoot_sound.set_volume(1)
                        death_sound.set_volume(1)
                        random_sound.set_volume(1)
                        key = display_message(screen, "Sound effects enabled")
                        if key == pygame.K_ESCAPE:
                            return "menu"
                    else:
                        jump_sound_1.set_volume(0)
                        jump_sound_2.set_volume(0)
                        shoot_sound.set_volume(0)
                        death_sound.set_volume(0)
                        random_sound.set_volume(0)
                        key = display_message(screen, "Sound effects disabled")
                        if key == pygame.K_ESCAPE:
                            return "menu"

############################################################################################################
def stats_screen():
    players = auth.load_players()  # Load player data from JSON
    running = True
    jump = players[username].get("total_jump", 0)  # Get the saved total jumps
    death = players[username].get("total_death", 0)  # Get the saved total deaths
    kill = players[username].get("total_kill", 0)  # Get the saved total kills
    high_score = players[username].get("high_score", 0)  # Get the saved high score
    shooting = players[username].get("shooting", 0)  # Get the saved shooting rate
    health = players[username].get("health", 0)  # Get the saved health
    strength = players[username].get("strength", 0)  # Get the saved strength

    while running:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_font.render("Stats Menu", True, WHITE), (100, 50))
        screen.blit(font.render(f"Total Jumps: {jump}", True, WHITE), (100, 100))
        screen.blit(font.render(f"Total Deaths: {death}", True, WHITE), (100, 125))
        screen.blit(font.render(f"Total Kills: {kill}", True, WHITE), (100, 150))
        screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (100, 175))
        screen.blit(font.render(f"Shooting Rate: {shooting}", True, WHITE), (100, 200))
        screen.blit(font.render(f"Health: {health}", True, WHITE), (100, 225))
        screen.blit(font.render(f"Strength: {strength}", True, WHITE), (100, 250))
        screen.blit(font.render("Press ESC to return to menu", True, WHITE), (100, 275))

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_ESCAPE:  # Return to menu
                    return "menu"  # Return to menu
                
        


############################################################################################################

def upgrade_screen(player):
    global total_coins, coins_collected # Use global coins
    players = auth.load_players()  # Load player data from JSON
    coin_cpt = players[username].get("coins", 0)  # Get the saved total coins
    running = True 
    health_lvl = players[username].get("health_lvl", 0)  # Get the saved health level
    strength_lvl = players[username].get("strength_lvl", 0)  # Get the saved strength level
    shooting_lvl = players[username].get("shooting_lvl", 0)  # Get the saved shooting level

    while running:
        screen.fill((0, 0, 0)) # Black background

        font = pygame.font.Font(None, 36)
        screen.blit(title_font.render("Upgrade Menu", True, WHITE), (100, 50))
        screen.blit(font.render("1. Upgrade Health", True, WHITE), (100, 125))
        screen.blit(font.render(f"LVL: {health_lvl}", True, WHITE), (100, 150))
        screen.blit(font.render("2. Upgrade Strength", True, WHITE), (100, 175))
        screen.blit(font.render(f"LVL: {strength_lvl}", True, WHITE), (100, 200))
        screen.blit(font.render("3. Upgrade Shooting", True, WHITE), (100, 225))
        screen.blit(font.render(f"LVL: {shooting_lvl}", True, WHITE), (100, 250))
        screen.blit(font.render(f"Coins: {coin_cpt}", True, WHITE), (500, 275))
        screen.blit(font.render("Press 1, 2, or 3 to upgrade", True, WHITE), (100, 100))
        screen.blit(font.render("Press ESC to return to menu", True, WHITE), (100, 275))

        pygame.display.flip() # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit the game
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN: # Check for key presses
                if event.key == pygame.K_ESCAPE: # Return to menu
                    player.coins = coin_cpt  # Update player's coins
                    player.save_progress()  # Save player progress
                    return "menu"  # Retour au menu

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]: # Upgrade player stats
                    if coin_cpt > 0:
                        coin_cpt -= 1  # Deduct coins for upgrade
                        players[username]["coins"] = coin_cpt  # Update player's coins
                        player.save_progress()  # Save player progress
                    else:
                        key = display_message(screen, "You don't have enough coins!")
                        if key == pygame.K_ESCAPE:
                            return "menu"
                        continue  

                    if event.key == pygame.K_1:
                        player.upgrade_health()
                    elif event.key == pygame.K_2:
                        player.upgrade_strength()
                    elif event.key == pygame.K_3:
                        player.upgrade_shooting()

                    player.save_progress()  # Save player progress


############################################################################################################

def home_page():
    players = auth.load_players()  # Load player data from JSON
    highest_score = players[username].get("high_score", 0)  # Get the saved high score
    coin_cpt = players[username].get("coins", 0)  # Get the saved total coins

    while True:
        screen.fill(BLUE)
        title_text = title_font.render("Run and Jump Game", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        quit_text = font.render("Press ESC to Quit", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

        coin_text = font.render(f"Total coins: {coin_cpt}", True, WHITE)
        screen.blit(coin_text, (10, 10))

        high_score_text = font.render(f"High Score: {highest_score}", True, WHITE)
        screen.blit(high_score_text, (10, 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    return
                elif event.key == pygame.K_ESCAPE:  # Quit the game
                    pygame.quit()
                    exit()
                
# Start with the home page
home_page()
############################################################################################################

def menu():
    global player, player_data, coins_collected, total_coins, game_over, score
    global player_height, player_y, player_vel_y, on_ground, platforms, obstacles
    global zombies, bosses, Zombie_wave_time, Boss_wave_time
    global username

    players = auth.load_players()  # Load player data from JSON
    highest_score = players[username].get("high_score", 0)  # Get the saved high score
    coin_cpt = players[username].get("coins", 0)  # Get the saved total coins

    while True:
        screen.fill(BLUE)

        game_over_text = title_font.render("Run and Jump Game", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))

        restart_text = font.render("Press ENTER to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - 40))

        upgrade_text = font.render("Press U to Upgrade", True, WHITE)
        screen.blit(upgrade_text, (WIDTH // 2 - upgrade_text.get_width() // 2, HEIGHT // 2 - 20))

        settings_text = font.render("Press S for Settings", True, WHITE)
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2))

        stats_text = font.render("Press T for Stats", True, WHITE)
        screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2 + 20))

        logout_text = font.render("Press L to Logout", True, WHITE)
        screen.blit(logout_text, (WIDTH // 2 - logout_text.get_width() // 2, HEIGHT // 2 + 40))

        score_text = font.render(f"Last Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 60))

        high_score_text = font.render(f"High Score: {highest_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 80))

        coin_text = font.render(f"Total coins: {coin_cpt}", True, WHITE)
        screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, HEIGHT // 2 + 100))

        quit_text = font.render("Press ESC to Quit", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 120))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    reset_game()  # Function to reset variables and restart
                    return  # Clean exit from the menu

                elif event.key == pygame.K_u:  # Go to upgrade screen
                    if upgrade_screen(player) == "menu":
                        continue  # Return to menu after upgrade

                elif event.key == pygame.K_s:  # Go to settings screen
                    if settings_screen() == "menu":
                        continue  # Return to menu after settings

                elif event.key == pygame.K_t:  # Go to stats screen
                    if stats_screen() == "menu":
                        continue  # Return to menu after stats

                elif event.key == pygame.K_l:  # Logout
                    player.save_progress()
                    auth.clear_cache()  # Clear the cache
                    username, player_data = login_screen()  # Redirect to login screen
                    player = Player(player_data)  # Recreate the player object with new data
                    home_page()  # Redirect to home page
                    return  # Exit the menu

                elif event.key == pygame.K_ESCAPE:  # Quit the game
                    pygame.quit()
                    exit()

###############################################################################################################
def reset_game():
    global game_over, score, player_y, player_vel_y, on_ground, platforms, obstacles, coins_collected, zombies, bosses
    game_over = False
    score = 0
    player_y = HEIGHT - standing_height - 20
    player_vel_y = 0
    on_ground = True
    platforms = [(0, HEIGHT - ground_height, WIDTH, ground_height)]
    obstacles = []
    zombies.empty()
    bosses.empty()

        
############################################################################################################
# Game loop
player = Player(player_data)  # On passe les données du joueur, Création unique du joueur
players = auth.load_players()  # Load player data from JSON
highest_score = players[username].get("high_score", 0)  # Get the saved high score

result = None 

while True:
    screen.fill(BLUE)  # Sky color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    elapsed_time += 1 / FPS  # Increment elapsed time

    # Call handle_events to check for and trigger events
    handle_events()

    # Spawn zombies at random intervals
    if random.randint(1, 200) == 50:
        zombie = Zombie()
        zombies.add(zombie)


    # Update zombies
    zombies.update()
    # Update bosses
    bosses.update()
    # Update bullets
    bullets.update()

    if not game_over:
        # Handle input
        music.play()  # Play background music
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and on_ground:  # Jump if on the ground
            player_vel_y = -JUMP_STRENGTH
            on_ground = False
            sound = random.choice([1,2])
            if sound == 1:
                jump_sound_1.play()
            else:
                jump_sound_2.play()
            jump_count += 1  # Increment total jumps
        
        if keys[pygame.K_UP] and on_ground:  # Jump if on the ground
            player_vel_y = -JUMP_STRENGTH
            on_ground = False
            sound = random.choice([1,2])
            if sound == 1:
                jump_sound_1.play()
            else:
                jump_sound_2.play()
            jump_count += 1  # Increment total jumps

        if keys[pygame.K_DOWN] and on_ground and not is_crouching:  # crouch if on the ground
            is_crouching = True
            player_height = crouch_height   # Crouch

        if not keys[pygame.K_DOWN] and is_crouching and on_ground:  # Stand up if not crouching
            is_crouching = False
            player_height = standing_height  # Stand up

        # Inside the game loop
        is_jumping = not on_ground and player_vel_y < 0  # Check if the player is jumping
        is_crouching = keys[pygame.K_DOWN] and on_ground  # Check if the player is crouching

        # Update the player
        player.update(on_ground, is_crouching, is_jumping)

        # Draw the player
        screen.blit(player.image, player.rect)

        # Draw the hitbox (black rectangle)
        pygame.draw.rect(screen, (0, 0, 0), player.rect, 2)  # Dessine un rectangle noir autour de la hitbox

        # Shoot bullets
        if keys[pygame.K_RIGHT]:
            bullet_cooldown = time.time()
            if bullet_cooldown - last_shot_time >= player.shooting:
                bullet = Bullet(player_x + player_width, player_y + player_height // 2)
                bullets.add(bullet)
                shoot_sound.play()
                last_shot_time = bullet_cooldown

        # Draw zombies
        zombies.draw(screen)
        # Draw bosses
        bosses.draw(screen)
        # Draw bullets
        bullets.draw(screen)

        collisions = pygame.sprite.groupcollide(bullets, zombies, True, True)
        if collisions:
            coins_collected += len(collisions)  # Add coins for each zombie hit
            kill_count += len(collisions)  # Increment total kills

        # Check for collisions with zombies
        check_zombie_shot(zombies, bullets, player)
        check_boss_shot(bosses, bullets, player)
        render_coin_count(screen, coins_collected)

        # Gravity
        player_vel_y += GRAVITY  # Apply gravity to the vertical velocity
        player.rect.y += player_vel_y  # Update the player's vertical position

        # Collision with ground
        if player.rect.y + player.rect.height >= HEIGHT - ground_height:
            player.rect.y = HEIGHT - ground_height - player.rect.height  # Reset position to ground level
            player_vel_y = 0  # Stop vertical movement
            on_ground = True
        else:
            on_ground = False  # Player is in the air

        if zombies:
            randomsound = random.randint(1, 500)
            if randomsound == 50:
                random_sound.play()

        # Move platforms (scrolling effect)
        for i in range(len(platforms)):
            platforms[i] = (platforms[i][0] - SCROLL_SPEED, platforms[i][1], platforms[i][2], platforms[i][3])

        # Add new platforms to ensure infinite scrolling
        if platforms[-1][0] + platforms[-1][2] <= WIDTH:
            platforms.append((platforms[-1][0] + platforms[-1][2], HEIGHT - ground_height, WIDTH, ground_height))

        # Remove off-screen platforms
        platforms = [plat for plat in platforms if plat[0] + plat[2] > 0]

        # Add obstacles
        frames_since_last_obstacle += 1
        if frames_since_last_obstacle >= next_obstacle_interval:
            frames_since_last_obstacle = 0
            next_obstacle_interval = random.randint(OBSTACLE_FREQ_MIN, OBSTACLE_FREQ_MAX)
            obstacle_offset = random.choice([0, 50, 100])
            obstacles.append([WIDTH, HEIGHT - ground_height - obstacle_height - obstacle_offset, obstacle_width, obstacle_height])

        # Move obstacles
        for obstacle in obstacles[:]:
            obstacle[0] -= SCROLL_SPEED
            if obstacle[0] + obstacle[2] < 0:  # Remove off-screen obstacles
                obstacles.remove(obstacle)
                score += 1  # Increase score when passing an obstacle

        # Check for collisions with obstacles
        # Utilisez player.rect pour les collisions
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle)
            if player.rect.colliderect(obstacle_rect):  # Utilisez player.rect ici
                death_count += 1
                death_sound.play()
                game_over = True
        
       # Check for collisions with zombies
        for zombie in zombies:
            if player.rect.colliderect(zombie.rect):
                death_count += 1
                death_sound.play()
                game_over = True

        # Check for collisions with bosses
        for boss in bosses:
            if player.rect.colliderect(boss.rect):
                death_count += 1
                death_sound.play()
                game_over = True


        # Draw platforms
        for plat in platforms:
            pygame.draw.rect(screen, BROWN, plat)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {highest_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))




    else:
        player.save_progress()  # Save player progress
        high_score = max(high_score, score)
        result = menu()
        if result == "restart":
            reset_game()
            game_over = False
            continue

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


############################################################################################################
#IDEES D'AMÉLIORATION
# - Ajouter des sons
# - Ajouter des animations
# - Ajouter des niveaux de difficulté
# - Ajouter des power-ups
## - Ajouter des boss
# - Ajouter des obstacles mobiles
# - Ajouter des ennemis à distance
############################################################################################################

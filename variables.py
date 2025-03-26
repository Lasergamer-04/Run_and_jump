from constants import *

# Player variables
player_width = 40 # Width of the player
standing_height = 60 # Height of the player when standing
crouch_height = 30  # Height of the player when crouching
player_height = standing_height  # Height of the player
player_x, player_y = 100, HEIGHT - player_height - 20  # Ground position
player_vel_y = 0
on_ground = True
is_crouching = False
crouch_start_time = None
last_shot_time = 0

# Initialize coin counter
coins_collected = 0
total_coins = 0

# Platform variables
platforms = [(0, HEIGHT - ground_height, WIDTH, ground_height)]  # Initial ground

# Obstacle variables
obstacles = []  # List of obstacles
obstacle_width, obstacle_height = 20, 40
frames_since_last_obstacle = 0

# Score variables
score = 0
high_score = 0
game_over = False

#menu variables
show_upgrade_menu = False

# Player stats variables
kill_count = 0
jump_count = 0
death_count = 0

# time variables
elapsed_time = 0

#event message variables
# Initialize message timing variables
message_start_time = None
message_duration = 0
message_surface = None
message_rect = None
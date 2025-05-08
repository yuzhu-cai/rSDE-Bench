'''
This is the main file for the Battle of Balls game. It initializes the game, sets up the player and enemy balls, and handles user input for movement. The game runs in a loop, updating the state and checking for collisions, while logging events to a file.
'''
import pygame
import random
import json
import time
# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_RADIUS = 20
ENEMY_RADIUS = 15
SPAWN_RADIUS = 5
LOG_FILE = "game.log"
SPAWN_INTERVAL = 2000  # milliseconds
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of Balls")
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Game state
player_pos = [0, 0]
player_radius = PLAYER_RADIUS
active_enemies = [[random.randint(-WIDTH//2, WIDTH//2), random.randint(-HEIGHT//2, HEIGHT//2), ENEMY_RADIUS] for _ in range(3)]
fixed_enemies = [[random.randint(-WIDTH//2, WIDTH//2), random.randint(-HEIGHT//2, HEIGHT//2), ENEMY_RADIUS]]
small_balls = []
# Log initialization
def log_event(event_type):
    timestamp = time.time()
    log_entry = {
        "timestamp": timestamp,
        "EVENT_TYPE": event_type,
        "game_state": {
            "player": {
                "position": player_pos,
                "radius": player_radius,
            },
            "active_enemies": [{"position": enemy[:2], "radius": enemy[2]} for enemy in active_enemies],
            "fixed_enemies": [{"position": enemy[:2], "radius": enemy[2]} for enemy in fixed_enemies],
            "small_balls": [{"position": ball[:2], "radius": ball[2]} for ball in small_balls]
        }
    }
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(json.dumps(log_entry) + "\n")
# Initialize game
log_event("INIT")
# Function to spawn small balls
def spawn_small_ball():
    x = random.randint(-WIDTH//2, WIDTH//2)
    y = random.randint(-HEIGHT//2, HEIGHT//2)
    small_balls.append([x, y, SPAWN_RADIUS])
    log_event("SPAWN_SMALL_BALL")  # Log the spawning event
# Function to check for collisions
def check_collisions():
    global player_radius
    # Check player collisions with active enemies
    for enemy in active_enemies:
        distance = ((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2) ** 0.5
        if distance < player_radius + enemy[2]:  # Collision detected
            player_radius += enemy[2]  # Increase player size
            log_event("EAT_ENEMY")  # Log the event
            enemy[2] = -1  # Mark enemy as consumed
    # Check player collisions with fixed enemies
    for enemy in fixed_enemies:
        distance = ((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2) ** 0.5
        if distance < player_radius + enemy[2]:  # Collision detected
            player_radius += enemy[2]  # Increase player size
            log_event("EAT_FIXED_ENEMY")  # Log the event
            enemy[2] = -1  # Mark enemy as consumed
    # Check for collisions with small balls
    for ball in small_balls:
        distance = ((player_pos[0] - ball[0]) ** 2 + (player_pos[1] - ball[1]) ** 2) ** 0.5
        if distance < player_radius + ball[2]:  # Collision detected
            player_radius += ball[2]  # Increase player size
            log_event("EAT_SMALL_BALL")  # Log the event
            ball[2] = -1  # Mark small ball as consumed
    # Check if player ball is consumed by any enemy
    for enemy in active_enemies + fixed_enemies:
        if enemy[2] != -1:  # Only check if not consumed
            distance = ((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2) ** 0.5
            if distance < enemy[2] + player_radius:  # Collision detected
                log_event("GAME_OVER")  # Log the game over event
                pygame.quit()  # End the game
# Function to update enemy positions (fixed)
def update_enemy_positions():
    # No need to adjust enemy positions; they remain fixed
    pass
# Main game loop
running = True
last_spawn_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos[0] -= 5
                log_event("MOVE_LEFT")
            if event.key == pygame.K_RIGHT:
                player_pos[0] += 5
                log_event("MOVE_RIGHT")
            if event.key == pygame.K_UP:
                player_pos[1] -= 5
                log_event("MOVE_UP")
            if event.key == pygame.K_DOWN:
                player_pos[1] += 5
                log_event("MOVE_DOWN")
    # Spawn small balls at intervals
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        spawn_small_ball()
        last_spawn_time = current_time
    # Update enemy positions (no movement)
    update_enemy_positions()
    # Check for collisions
    check_collisions()
    # Drawing
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (WIDTH//2, HEIGHT//2), player_radius)
    for enemy in active_enemies:
        if enemy[2] != -1:  # Only draw if not consumed
            pygame.draw.circle(screen, RED, (WIDTH//2 + enemy[0], HEIGHT//2 + enemy[1]), enemy[2])
    for enemy in fixed_enemies:
        if enemy[2] != -1:  # Only draw if not consumed
            pygame.draw.circle(screen, GREEN, (WIDTH//2 + enemy[0], HEIGHT//2 + enemy[1]), enemy[2])
    for ball in small_balls:
        if ball[2] != -1:  # Only draw if not consumed
            pygame.draw.circle(screen, YELLOW, (WIDTH//2 + ball[0], HEIGHT//2 + ball[1]), ball[2])
    pygame.display.flip()
    pygame.time.delay(30)
pygame.quit()
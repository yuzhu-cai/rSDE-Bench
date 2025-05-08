'''
This is the main file for the Super Mario game. It initializes the game, sets up the game window, 
handles user input, updates game elements, and manages the game loop.
'''
import pygame
import random
import json
import time
from logger import log_event  # Importing log_event from logger module
# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 50
BLOCK_SIZE = 50
MUSHROOM_SIZE = 30
ENEMY_SIZE = 40
FPS = 60
# Colors
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Game")
# Game variables
mario_pos = [50, HEIGHT - GROUND_HEIGHT - 50]
block_pos = [mario_pos[0], HEIGHT - GROUND_HEIGHT - BLOCK_SIZE]
mushroom_pos = [None, None]
enemy_pos = [random.randint(200, WIDTH - 100), HEIGHT - GROUND_HEIGHT - ENEMY_SIZE]
score = 0
mushroom_direction = -1  # Initially moving left
running = True
clock = pygame.time.Clock()
# Log file
log_file = open('game.log', 'w')
# Game loop
while running:
    screen.fill(WHITE)
    # Draw ground
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    # Draw block
    pygame.draw.rect(screen, GREEN, (block_pos[0], block_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    # Draw Mario
    pygame.draw.rect(screen, RED, (mario_pos[0], mario_pos[1], 50, 50))
    # Draw enemy
    pygame.draw.rect(screen, (0, 0, 255), (enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE))
    # Draw mushroom if it exists
    if mushroom_pos[0] is not None:
        pygame.draw.rect(screen, (255, 165, 0), (mushroom_pos[0], mushroom_pos[1], MUSHROOM_SIZE, MUSHROOM_SIZE))
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Mario controls
            if event.key == pygame.K_LEFT:
                mario_pos[0] -= 5
                log_event("MOVE_LEFT", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
            if event.key == pygame.K_RIGHT:
                mario_pos[0] += 5
                log_event("MOVE_RIGHT", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
            if event.key == pygame.K_UP:
                if mario_pos[1] == HEIGHT - GROUND_HEIGHT - 50:  # Only jump if on the ground
                    mario_pos[1] -= 100
                    log_event("JUMP", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
            if event.key == pygame.K_DOWN:
                if enemy_pos[0] is not None and mario_pos[0] + 50 > enemy_pos[0] and mario_pos[0] < enemy_pos[0] + ENEMY_SIZE:
                    enemy_pos = [None, None]  # Update enemy position immediately
                    log_event("ELIMINATE_ENEMY", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
    # Gravity
    if mario_pos[1] < HEIGHT - GROUND_HEIGHT - 50:
        mario_pos[1] += 5  # Fall down
    else:
        mario_pos[1] = HEIGHT - GROUND_HEIGHT - 50  # Reset to ground level
    # Check for block hit
    if (mario_pos[0] + 50 > block_pos[0] and mario_pos[0] < block_pos[0] + BLOCK_SIZE and 
        mario_pos[1] + 50 > block_pos[1] and mario_pos[1] + 50 < block_pos[1] + BLOCK_SIZE):
        mushroom_pos = [block_pos[0], block_pos[1] - MUSHROOM_SIZE]
        score += 100
        log_event("HIT_BLOCK", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
    # Mushroom movement
    if mushroom_pos[0] is not None:
        mushroom_pos[0] += mushroom_direction * 2  # Move left or right based on direction
        if mushroom_pos[0] <= 0 or mushroom_pos[0] >= WIDTH - MUSHROOM_SIZE:
            mushroom_direction *= -1  # Change direction upon hitting the border
            mushroom_pos[0] = max(0, min(mushroom_pos[0], WIDTH - MUSHROOM_SIZE))  # Keep within bounds
        # Check if Mario touches the mushroom
        if (mario_pos[0] + 50 > mushroom_pos[0] and mario_pos[0] < mushroom_pos[0] + MUSHROOM_SIZE and 
            mario_pos[1] + 50 > mushroom_pos[1] and mario_pos[1] < mushroom_pos[1] + MUSHROOM_SIZE):
            mushroom_pos = [None, None]
            score += 1000
            log_event("TOUCH_MUSHROOM", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
    # Check for reaching flag
    if mario_pos[0] + 50 > WIDTH - 50:
        score += 10000
        log_event("REACH_FLAG", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
        running = False
    # Check for collision with enemy
    if enemy_pos[0] is not None and (mario_pos[0] + 50 > enemy_pos[0] and mario_pos[0] < enemy_pos[0] + ENEMY_SIZE):
        log_event("COLLIDE_ENEMY", score, mario_pos, enemy_pos, block_pos, mushroom_pos)
        raise SystemExit  # Raise SystemExit on collision with enemy
    # Update score every second
    score += 1 / FPS
    pygame.display.flip()
    clock.tick(FPS)
# Clean up
log_file.close()
pygame.quit()
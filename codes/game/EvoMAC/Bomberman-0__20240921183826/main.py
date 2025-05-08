'''
This is the main file for the Bomberman game. It initializes the game, sets up the GUI, and handles the main game loop.
'''
import pygame
import random
import json
import time
import threading
# Constants
GRID_SIZE = 13
CELL_SIZE = 40
OBSTACLES = [(i, j) for i in range(0, GRID_SIZE, 2) for j in range(0, GRID_SIZE, 2)]
PLAYER_START_POS = (0, 0)
ENEMY_START_POS = [(random.randint(1, GRID_SIZE-1), random.randint(1, GRID_SIZE-1)) for _ in range(2)]
INITIAL_PLAYER_HEALTH = 100
INITIAL_ENEMY_HEALTH = 10
INITIAL_SCORE = 0
BOMB_EXPLOSION_DELAY = 2  # seconds
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
# Initialize Pygame
pygame.init()
# Create the game window
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Bomberman Game")
# Game state
player_pos = PLAYER_START_POS
enemies_pos = ENEMY_START_POS
player_health = INITIAL_PLAYER_HEALTH
enemies_health = [INITIAL_ENEMY_HEALTH, INITIAL_ENEMY_HEALTH]
score = INITIAL_SCORE
bombs = []
explosions = []
# Log file initialization
log_file = open("game.log", "w")
initial_state = {
    "timestamp": time.time(),
    "EVENT_TYPE": "INIT",
    "game_board_state": [0] * (GRID_SIZE * GRID_SIZE),
    "player": {"health": player_health, "score": score},
    "enemies": [{"health": health} for health in enemies_health]
}
log_file.write(json.dumps(initial_state) + "\n")
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) in OBSTACLES:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)
def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
def draw_enemies():
    for pos in enemies_pos:
        pygame.draw.rect(screen, RED, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
def draw_bombs():
    for bomb in bombs:
        pygame.draw.rect(screen, GRAY, (bomb[0] * CELL_SIZE, bomb[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
def draw_explosions():
    for explosion in explosions:
        pygame.draw.rect(screen, ORANGE, (explosion[0] * CELL_SIZE, explosion[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
def update_log(event_type):
    global player_health, enemies_health, score
    game_board_state = [0] * (GRID_SIZE * GRID_SIZE)
    game_board_state[player_pos[1] * GRID_SIZE + player_pos[0]] = 1
    for i, pos in enumerate(enemies_pos):
        game_board_state[pos[1] * GRID_SIZE + pos[0]] = 2 if enemies_health[i] > 0 else 0
    for bomb in bombs:
        game_board_state[bomb[1] * GRID_SIZE + bomb[0]] = 3
    for explosion in explosions:
        game_board_state[explosion[1] * GRID_SIZE + explosion[0]] = 4
    for obstacle in OBSTACLES:
        game_board_state[obstacle[1] * GRID_SIZE + obstacle[0]] = -1
    log_entry = {
        "timestamp": time.time(),
        "EVENT_TYPE": event_type,
        "game_board_state": game_board_state,
        "player": {"health": player_health, "score": score},
        "enemies": [{"health": health} for health in enemies_health]
    }
    log_file.write(json.dumps(log_entry) + "\n")
def move_enemies_towards_player():
    global enemies_pos
    for i, enemy_pos in enumerate(enemies_pos):
        if enemies_health[i] > 0:  # Only move if the enemy is alive
            new_pos = enemy_pos
            if enemy_pos[0] < player_pos[0]:
                new_pos = (enemy_pos[0] + 1, enemy_pos[1])
            elif enemy_pos[0] > player_pos[0]:
                new_pos = (enemy_pos[0] - 1, enemy_pos[1])
            elif enemy_pos[1] < player_pos[1]:
                new_pos = (enemy_pos[0], enemy_pos[1] + 1)
            elif enemy_pos[1] > player_pos[1]:
                new_pos = (enemy_pos[0], enemy_pos[1] - 1)
            # Check for obstacles and boundaries
            if new_pos not in OBSTACLES and 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                enemies_pos[i] = new_pos
                update_log("MOVE_ENEMY")  # Log the enemy movement
def explode_bomb(bomb_pos):
    global explosions, player_health, enemies_health, score
    explosions.append(bomb_pos)
    # Check fire spread in all four directions
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for distance in range(1, 4):  # Spread fire for 3 squares
            new_x = bomb_pos[0] + dx * distance
            new_y = bomb_pos[1] + dy * distance
            if (new_x, new_y) in OBSTACLES or not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
                break  # Stop spreading if blocked by an obstacle
            explosions.append((new_x, new_y))
            # Check for player and enemies in the explosion zone
            if (new_x, new_y) == player_pos:
                player_health -= 10
                update_log("INJURED")
            for i, enemy_pos in enumerate(enemies_pos):
                if (new_x, new_y) == enemy_pos and enemies_health[i] > 0:
                    enemies_health[i] = 0  # Enemy is defeated
                    score += 100
                    update_log("INJURED")
def bomb_timer(bomb_pos):
    time.sleep(BOMB_EXPLOSION_DELAY)
    explode_bomb(bomb_pos)
def check_victory_condition():
    if all(health <= 0 for health in enemies_health):
        victory_message = f"Victory! Your score: {score}"
        print(victory_message)  # Display victory message in console
        update_log("VICTORY")  # Log the victory event
        pygame.quit()  # Exit the game after victory
# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_player()
    draw_enemies()
    draw_bombs()
    draw_explosions()
    move_enemies_towards_player()  # Call the enemy movement function
    check_victory_condition()  # Check for victory condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Move left
                new_pos = (max(0, player_pos[0] - 1), player_pos[1])
                if new_pos not in OBSTACLES:  # Check for obstacles
                    player_pos = new_pos
                    update_log("MOVE_LEFT")
            elif event.key == pygame.K_RIGHT:
                # Move right
                new_pos = (min(GRID_SIZE - 1, player_pos[0] + 1), player_pos[1])
                if new_pos not in OBSTACLES:  # Check for obstacles
                    player_pos = new_pos
                    update_log("MOVE_RIGHT")
            elif event.key == pygame.K_UP:
                # Move up
                new_pos = (player_pos[0], max(0, player_pos[1] - 1))
                if new_pos not in OBSTACLES:  # Check for obstacles
                    player_pos = new_pos
                    update_log("MOVE_UP")
            elif event.key == pygame.K_DOWN:
                # Move down
                new_pos = (player_pos[0], min(GRID_SIZE - 1, player_pos[1] + 1))
                if new_pos not in OBSTACLES:  # Check for obstacles
                    player_pos = new_pos
                    update_log("MOVE_DOWN")
            elif event.key == pygame.K_SPACE:
                # Place bomb
                bombs.append(player_pos)
                update_log("PLACE_BOMB")
                threading.Thread(target=bomb_timer, args=(player_pos,)).start()  # Start bomb timer in a new thread
    pygame.display.flip()
pygame.quit()
log_file.close()
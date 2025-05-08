'''
This is the main file for the Single-Player Tank Battle Game. It initializes the game, sets up the GUI, and handles user inputs for controlling the player's tank.
'''
import pygame
import json
import time
# Constants
GRID_SIZE = 20
CELL_SIZE = 30
PLAYER_COLOR = (255, 255, 0)  # Yellow
ENEMY_COLOR = (192, 192, 192)  # Silver
OBSTACLE_COLOR = (139, 69, 19)  # Brown
BACKGROUND_COLOR = (0, 0, 0)  # Black
FPS = 30
# Game state
player_health = 200
enemy_healths = [200, 200]
player_score = 0
player_position = [0, 0]
enemy_positions = [[5, 5], [10, 10]]  # Fixed enemy positions
obstacle_positions = []  # Add obstacles as needed
bullets = []  # List to hold active bullets
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Tank Battle Game")
clock = pygame.time.Clock()
# Log file initialization
log_file = open('game.log', 'w')
log_entry = {
    "timestamp": time.time(),
    "EVENT_TYPE": "INIT",
    "game_state": {
        "player": {
            "position": player_position,
            "health": player_health,
            "score": player_score
        },
        "enemies": [
            {
                "position": enemy_positions[0],
                "health": enemy_healths[0]
            },
            {
                "position": enemy_positions[1],
                "health": enemy_healths[1]
            }
        ],
        "obstacle_position": obstacle_positions
    }
}
log_file.write(json.dumps(log_entry) + "\n")
class Bullet:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction  # (dx, dy)
    def move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    # Draw obstacles
    for (xo, yo) in obstacle_positions:
        pygame.draw.rect(screen, OBSTACLE_COLOR, (xo * CELL_SIZE, yo * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw player tank
    pygame.draw.rect(screen, PLAYER_COLOR, (player_position[0] * CELL_SIZE, player_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw enemy tanks
    for enemy_position in enemy_positions:
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy_position[0] * CELL_SIZE, enemy_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet.position[0] * CELL_SIZE, bullet.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
def move_player(dx, dy):
    global player_position
    new_x = player_position[0] + dx
    new_y = player_position[1] + dy
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        player_position = [new_x, new_y]
        log_event("MOVE", player_position)
def fire_bullet():
    global bullets
    bullet = Bullet(position=player_position.copy(), direction=(0, -1))  # Fire upwards
    bullets.append(bullet)
    log_event("FIRE", player_position)
def update_bullets():
    global player_health, enemy_healths, player_score
    for bullet in bullets[:]:  # Iterate over a copy of the list
        bullet.move()
        # Check for collisions with enemies
        for i, enemy_position in enumerate(enemy_positions):
            if bullet.position == enemy_position:
                enemy_healths[i] -= 100
                bullets.remove(bullet)
                log_event("INJURED", enemy_position)
                if enemy_healths[i] <= 0:
                    player_score += 200
                    enemy_healths[i] = 0  # Mark enemy as destroyed
                    log_event("DESTROYED", enemy_position)  # Log enemy destruction
                break
        # Check for collisions with player
        if bullet.position == player_position:
            player_health -= 10
            bullets.remove(bullet)
            log_event("INJURED", player_position)
            if player_health <= 0:
                player_health = 0  # Mark player as destroyed
                log_event("DESTROYED", player_position)  # Log player destruction
                end_game()  # Call the end game function
def log_event(event_type, position):
    global player_health, player_score
    log_entry = {
        "timestamp": time.time(),
        "EVENT_TYPE": event_type,
        "game_state": {
            "player": {
                "position": player_position,
                "health": player_health,
                "score": player_score
            },
            "enemies": [
                {
                    "position": enemy_positions[0],
                    "health": enemy_healths[0]
                },
                {
                    "position": enemy_positions[1],
                    "health": enemy_healths[1]
                }
            ],
            "obstacle_position": obstacle_positions
        }
    }
    log_file.write(json.dumps(log_entry) + "\n")
def end_game():
    global running
    running = False
    log_entry = {
        "timestamp": time.time(),
        "EVENT_TYPE": "GAME_OVER",
        "game_state": {
            "player": {
                "position": player_position,
                "health": player_health,
                "score": player_score
            },
            "enemies": [
                {
                    "position": enemy_positions[0],
                    "health": enemy_healths[0]
                },
                {
                    "position": enemy_positions[1],
                    "health": enemy_healths[1]
                }
            ],
            "obstacle_position": obstacle_positions
        }
    }
    log_file.write(json.dumps(log_entry) + "\n")
    print(f"Game Over! Your score: {player_score}")
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_player(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)
            elif event.key == pygame.K_RETURN:
                fire_bullet()
    update_bullets()
    draw_grid()
    clock.tick(FPS)
pygame.quit()
log_file.close()
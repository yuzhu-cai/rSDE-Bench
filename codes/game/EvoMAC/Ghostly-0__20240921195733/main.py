'''
This is the main file for the Ghostly game. It initializes the game, sets up the GUI, and handles player input and game logic.
'''
import pygame
import json
import time
# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
FPS = 10
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Game elements initial positions
ghost_position = [1, 1]
pellet_positions = [[3, 3], [4, 2]]
superpellet_positions = [[5, 5], [6, 3]]
other_ghost_positions = [[0, 5], [3, 5]]
walls_position = [[0, 4], [1, 4], [2, 4], [3, 4]]
monster_position = [-1, -1]
game_ticks = 0
superpellet_active = False
game_status = "ongoing"
# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ghostly Game")
clock = pygame.time.Clock()
# Log file setup
log_file = open('game.log', 'w')  # Open log file in write mode to clear previous entries
def log_event(event_type, move_direction, ghost_pos, monster_pos, status):
    timestamp = time.time()
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "move_direction": move_direction,
        "ghost_position": ghost_pos,
        "monster_position": monster_pos,
        "game_status": status
    }
    log_file.write(json.dumps(log_entry) + "\n")
    log_file.flush()
def draw_elements():
    window.fill(WHITE)
    # Draw walls
    for wall in walls_position:
        pygame.draw.rect(window, BLACK, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw pellets
    for pellet in pellet_positions:
        pygame.draw.circle(window, GREEN, (pellet[0] * GRID_SIZE + GRID_SIZE // 2, pellet[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 4)
    # Draw superpellets
    for superpellet in superpellet_positions:
        pygame.draw.circle(window, BLUE, (superpellet[0] * GRID_SIZE + GRID_SIZE // 2, superpellet[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)
    # Draw other ghosts
    for other_ghost in other_ghost_positions:
        pygame.draw.circle(window, RED, (other_ghost[0] * GRID_SIZE + GRID_SIZE // 2, other_ghost[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)
    # Draw player's ghost
    pygame.draw.circle(window, BLACK, (ghost_position[0] * GRID_SIZE + GRID_SIZE // 2, ghost_position[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)
    # Draw monster
    if monster_position != [-1, -1]:
        pygame.draw.circle(window, (255, 165, 0), (monster_position[0] * GRID_SIZE + GRID_SIZE // 2, monster_position[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)
def move_ghost(direction):
    global ghost_position, game_status, superpellet_active
    new_position = ghost_position[:]
    if direction == "up":
        new_position[1] -= 1
    elif direction == "down":
        new_position[1] += 1
    elif direction == "left":
        new_position[0] -= 1
    elif direction == "right":
        new_position[0] += 1
    # Check for wall collision
    if new_position in walls_position:
        log_event("invalid_move", direction, ghost_position, monster_position, game_status)
        return  # Position remains unchanged
    # Check for other ghost collision
    for other_ghost in other_ghost_positions:
        if new_position == other_ghost:
            if superpellet_active:
                other_ghost_positions.remove(other_ghost)
                log_event("eat_other_ghost", direction, ghost_position, monster_position, game_status)
                ghost_position[:] = new_position  # Update position
                return
            else:
                log_event("invalid_move", direction, ghost_position, monster_position, game_status)
                return  # Position remains unchanged
    # Check for pellet collision
    if new_position in pellet_positions:
        pellet_positions.remove(new_position)
        log_event("eat_pellet", direction, ghost_position, monster_position, game_status)
        ghost_position[:] = new_position  # Update position
        return
    # Check for superpellet collision
    if new_position in superpellet_positions:
        superpellet_positions.remove(new_position)
        superpellet_active = True
        log_event("eat_superpellet", direction, ghost_position, monster_position, game_status)
        ghost_position[:] = new_position  # Update position
        return
    # If no collisions, update position
    ghost_position[:] = new_position
    log_event("ordinary_move", direction, ghost_position, monster_position, game_status)
def activate_monster():
    global monster_position
    monster_position = [1, 1]
def move_monster():
    global monster_position, game_status
    if monster_position != [-1, -1]:
        # Calculate potential new position
        new_monster_position = monster_position[:]
        if ghost_position[0] < monster_position[0]:
            new_monster_position[0] -= 1
        elif ghost_position[0] > monster_position[0]:
            new_monster_position[0] += 1
        if ghost_position[1] < monster_position[1]:
            new_monster_position[1] -= 1
        elif ghost_position[1] > monster_position[1]:
            new_monster_position[1] += 1
        # Check for wall collision
        if new_monster_position not in walls_position:
            monster_position[:] = new_monster_position
        # Check for collision with player's ghost
        if ghost_position == monster_position:
            game_status = "lose"
            log_event("monster_eat_ghost", "", ghost_position, monster_position, game_status)
def check_victory():
    global game_status
    if not pellet_positions and not other_ghost_positions:
        game_status = "win"
def main():
    global game_ticks
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_ghost("up")
                if event.key == pygame.K_DOWN:
                    move_ghost("down")
                if event.key == pygame.K_LEFT:
                    move_ghost("left")
                if event.key == pygame.K_RIGHT:
                    move_ghost("right")
        game_ticks += 1
        if game_ticks > 50 and monster_position == [-1, -1]:
            activate_monster()
        move_monster()
        check_victory()
        draw_elements()
        pygame.display.flip()
        clock.tick(FPS)
    log_file.close()
    pygame.quit()
if __name__ == "__main__":
    main()
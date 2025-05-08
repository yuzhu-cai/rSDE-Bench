'''
This script implements a simple Sokoban game with a graphical user interface (GUI) using the Pygame library. 
The player can control the movement of boxes on a grid to reach the goal positions. 
Game progress is logged in a file named 'game.log'.
'''
import pygame
import json
import time
# Constants
GRID_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 7
PLAYER_COLOR = (0, 255, 0)
BOX_COLOR = (255, 165, 0)
GOAL_COLOR = (0, 0, 255)
WALL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
# Initial positions
player_position = [1, 1]
box_positions = [[3, 3], [4, 2]]
goal_positions = [[5, 5], [6, 3]]
wall_positions = [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]]
# Game status
game_status = "ONGOING"
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption("Sokoban Game")
# Create log file and clear it
with open('game.log', 'w') as log_file:
    log_file.write('')
def log_event(event_type):
    global player_position, box_positions, game_status
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = {
        "timestamp": timestamp,
        "EVENT_TYPE": event_type,
        "player_position": player_position,
        "box_positions": box_positions,
        "game_status": game_status
    }
    with open('game.log', 'a') as log_file:
        log_file.write(json.dumps(log_entry) + '\n')
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect)
            if [x, y] in wall_positions:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif [x, y] in goal_positions:
                pygame.draw.rect(screen, GOAL_COLOR, rect)
            elif [x, y] in box_positions:
                pygame.draw.rect(screen, BOX_COLOR, rect)
            if [x, y] == player_position:
                pygame.draw.rect(screen, PLAYER_COLOR, rect)
def move_player(dx, dy):
    global player_position, box_positions, game_status
    new_position = [player_position[0] + dx, player_position[1] + dy]
    # Check for wall collision
    if new_position in wall_positions:
        log_event("INVALID_MOVE")
        return
    # Check for box collision
    if new_position in box_positions:
        new_box_position = [new_position[0] + dx, new_position[1] + dy]
        if new_box_position in wall_positions or new_box_position in box_positions:
            log_event("INVALID_MOVE")
            return
        box_index = box_positions.index(new_position)
        box_positions[box_index] = new_box_position
    # Update player position
    player_position[:] = new_position
    # Log valid moves
    if dx == 1:
        log_event("MOVE_RIGHT")
    elif dx == -1:
        log_event("MOVE_LEFT")
    elif dy == -1:
        log_event("MOVE_UP")
    elif dy == 1:
        log_event("MOVE_DOWN")
    # Check for victory
    if all(box in goal_positions for box in box_positions):
        game_status = "COMPLETE"
        log_event("COMPLETE")
def main():
    global game_status
    clock = pygame.time.Clock()
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
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()
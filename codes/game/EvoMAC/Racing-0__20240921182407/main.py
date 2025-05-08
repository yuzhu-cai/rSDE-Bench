'''
This script implements a racing game using Pygame. The game features a three-lane route with obstacles, player controls for speed and lane changes, and a logging mechanism to track game events.
'''
import pygame
import random
import json
import time
# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
LANE_WIDTH = WIDTH // 3
FPS = 60
CAR_SPEED = 5
OBSTACLE_SPEED = 5
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Game Variables
car_position = 2  # Start in the middle lane (1, 2, 3)
car_speed = 0
distance_traveled = 0
obstacles = []
game_over = False
# Log file setup
log_file = 'game.log'
with open(log_file, 'w') as f:
    f.write('')  # Clear log file at the start
# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")
clock = pygame.time.Clock()
def log_event(event_type):
    '''
    Logs the event to the game.log file with the current timestamp, event type, speed, and position.
    '''
    global car_position, car_speed, distance_traveled
    log_entry = {
        "timestamp": time.time(),
        "EVENT_TYPE": event_type,
        "car_speed": car_speed,
        "car_position": [car_position, distance_traveled]
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
def create_obstacle():
    '''
    Creates a new obstacle with a random lane and type (slow or fatal).
    '''
    lane = random.randint(1, 3)
    return {'lane': lane, 'y': -50, 'type': random.choice(['slow', 'fatal'])}
def draw_obstacles():
    '''
    Draws the obstacles on the screen based on their type.
    '''
    for obstacle in obstacles:
        if obstacle['type'] == 'slow':
            color = GREEN
        else:
            color = RED
        pygame.draw.rect(screen, color, (obstacle['lane'] * LANE_WIDTH - LANE_WIDTH + 10, obstacle['y'], LANE_WIDTH - 20, 30))
def move_obstacles():
    '''
    Moves the obstacles down the screen and checks for collisions with the car.
    '''
    global game_over
    for obstacle in obstacles:
        obstacle['y'] += OBSTACLE_SPEED
        if obstacle['y'] > HEIGHT:
            obstacles.remove(obstacle)
        if obstacle['y'] > HEIGHT - 100 and obstacle['lane'] == car_position:
            if obstacle['type'] == 'fatal':
                game_over = True
                log_event("collide_fatal_obstacles")  # Log fatal collision
            else:
                log_event("collide_slow_down_obstacles")
                global car_speed
                car_speed = max(0, car_speed - 2)
def main():
    '''
    Main game loop that handles user input, updates game state, and renders the game.
    '''
    global car_speed, distance_traveled, game_over, car_position
    running = True
    while running:
        screen.fill(WHITE)
        # Update distance traveled before logging
        distance_traveled += car_speed / FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    car_speed += CAR_SPEED
                    log_event("speed_up")
                if event.key == pygame.K_DOWN:
                    car_speed = max(0, car_speed - CAR_SPEED)
                    log_event("speed_down")
                if event.key == pygame.K_LEFT and car_position > 1:
                    car_position -= 1
                    log_event("move_left")
                if event.key == pygame.K_RIGHT and car_position < 3:
                    car_position += 1
                    log_event("move_right")
                if event.key == pygame.K_s:
                    car_speed = 0
                    log_event("stop")
        if random.randint(1, 100) < 5:
            obstacles.append(create_obstacle())
        move_obstacles()
        draw_obstacles()
        pygame.draw.rect(screen, BLACK, (car_position * LANE_WIDTH - LANE_WIDTH + 10, HEIGHT - 100, LANE_WIDTH - 20, 50))
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f'Speed: {car_speed}', True, BLACK)
        distance_text = font.render(f'Distance: {int(distance_traveled)}', True, BLACK)
        screen.blit(speed_text, (WIDTH - 150, 10))
        screen.blit(distance_text, (WIDTH - 150, 40))
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    main()
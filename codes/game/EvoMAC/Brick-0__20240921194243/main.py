'''
This is the main file for the Brick Breaker game. It initializes the game window, 
sets up the game loop, and handles user input for paddle movement. 
The game logic for bouncing the ball, splitting bricks, and logging events is also implemented here.
'''
import pygame
import json
import time
# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_LIFE = 3
FPS = 60
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - PADDLE_WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH  # Ensure paddle does not exceed right edge
# Ball class
class Ball:
    def __init__(self):
        # Set the initial position of the ball to the center of the game window
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = 4
        self.dy = -4
    def move(self):
        # Check for collisions before updating position
        self.rect.x += self.dx
        self.rect.y += self.dy
# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.life = BRICK_LIFE
    def split(self):
        if self.life > 1:
            new_brick1 = Brick(self.rect.x, self.rect.y)
            new_brick2 = Brick(self.rect.x + BRICK_WIDTH // 2, self.rect.y)
            new_brick1.life = new_brick2.life = self.life - 1  # Set life of new bricks to 2
            self.life = 0  # Mark original brick as having 0 life
            return [new_brick1, new_brick2]
        return None
# Game class
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = self.create_bricks()
        self.running = False
        self.score = 0
    def create_bricks(self):
        bricks = []
        for i in range(5):  # 5 rows of bricks
            for j in range(10):  # 10 bricks per row
                # Adjust the y position calculation to ensure bricks are positioned correctly
                bricks.append(Brick(j * (BRICK_WIDTH + 5) + 35, i * (BRICK_HEIGHT + 5) + 30))
        return bricks
    def log_event(self, timestamp, event_type, log_file):
        log_entry = {
            "timestamp": timestamp,
            "EVENT_TYPE": event_type,
            "paddle_position": [self.paddle.rect.x, self.paddle.rect.y],
            "ball_position": [self.ball.rect.x, self.ball.rect.y],
            "bricks_info": [[brick.rect.x, brick.rect.y, brick.life] if brick.life > 0 else [None, None, 0] for brick in self.bricks]
        }
        log_file.write(json.dumps(log_entry) + "\n")
    def run(self):
        self.running = False  # Initially set to False
        with open('game.log', 'w') as log_file:  # Use context manager for file handling
            while True:  # Main loop to handle game start
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.running = True  # Start the game on first key press
                            if event.key == pygame.K_LEFT:
                                self.paddle.move(-10)
                                self.log_event(time.time(), "PADDLE_MOVE_LEFT", log_file)
                            if event.key == pygame.K_RIGHT:
                                self.paddle.move(10)
                                self.log_event(time.time(), "PADDLE_MOVE_RIGHT", log_file)
                            break  # Exit the event loop to start the game
                if self.running:  # Only run the game loop if running is True
                    # Ball movement and collision detection
                    self.ball.move()
                    # Ball collision with walls
                    if self.ball.rect.x <= 0 or self.ball.rect.x >= WIDTH - BALL_RADIUS * 2:
                        self.ball.dx *= -1
                        self.log_event(time.time(), "BOUNCE_WALL", log_file)
                    if self.ball.rect.y <= 0:
                        self.ball.dy *= -1
                        self.log_event(time.time(), "BOUNCE_WALL", log_file)
                    # Ball collision with paddle
                    if self.ball.rect.colliderect(self.paddle.rect):
                        self.ball.dy *= -1
                        self.log_event(time.time(), "BOUNCE_PADDLE", log_file)
                    # Ball collision with bricks
                    for brick in self.bricks:
                        if brick.life > 0 and self.ball.rect.colliderect(brick.rect):
                            self.ball.dy *= -1
                            new_bricks = brick.split()
                            if new_bricks:
                                self.bricks.remove(brick)
                                self.bricks.extend(new_bricks)
                            self.log_event(time.time(), "BOUNCE_BRICK", log_file)
                            self.score += 1  # Increment score for breaking a brick
                            break
                    # Check if ball is lost
                    if self.ball.rect.y > HEIGHT:
                        self.log_event(time.time(), "BALL_LOST", log_file)
                        self.running = False
                    # Drawing
                    screen.fill(BLACK)
                    pygame.draw.rect(screen, WHITE, self.paddle.rect)
                    pygame.draw.ellipse(screen, WHITE, self.ball.rect)
                    for brick in self.bricks:
                        if brick.life > 0:
                            pygame.draw.rect(screen, GREEN, brick.rect)
                    # Display score
                    font = pygame.font.Font(None, 36)
                    score_text = font.render(f'Score: {self.score}', True, WHITE)
                    screen.blit(score_text, (10, 10))
                    pygame.display.flip()
                    clock.tick(FPS)
        pygame.quit()
if __name__ == "__main__":
    game = Game()
    game.run()
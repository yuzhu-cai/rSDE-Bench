'''
Test the function inputs and the global variables imported in each function. 
Ensure that the input values and global variables used in the function are valid and involved when the function is called.
'''
import unittest
import pygame
from main import Paddle, Ball, Brick, Game
class TestBrickBreaker(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()
    def test_paddle_initial_position(self):
        self.assertEqual(self.game.paddle.rect.x, 350)  # Paddle should start at center
        self.assertEqual(self.game.paddle.rect.y, 570)  # Paddle should be at the bottom
    def test_ball_initial_position(self):
        self.assertEqual(self.game.ball.rect.x, 395)  # Ball should start at center
        self.assertEqual(self.game.ball.rect.y, 290)  # Ball should start slightly above the paddle
    def test_brick_creation(self):
        self.assertEqual(len(self.game.bricks), 50)  # 5 rows of 10 bricks
        for brick in self.game.bricks:
            self.assertEqual(brick.life, 3)  # Each brick should start with 3 lives
    def test_paddle_move_left(self):
        initial_position = self.game.paddle.rect.x
        self.game.paddle.move(-10)
        self.assertEqual(self.game.paddle.rect.x, initial_position - 10)
    def test_paddle_move_right(self):
        initial_position = self.game.paddle.rect.x
        self.game.paddle.move(10)
        self.assertEqual(self.game.paddle.rect.x, initial_position + 10)
    def test_ball_bounce_wall(self):
        self.game.ball.rect.x = 0  # Position ball at the left wall
        self.game.ball.dx = -4  # Set ball direction to left
        self.game.ball.move()
        self.assertEqual(self.game.ball.dx, 4)  # Ball should bounce back
    def test_ball_bounce_paddle(self):
        self.game.ball.rect.x = self.game.paddle.rect.x + 10  # Position ball above paddle
        self.game.ball.rect.y = self.game.paddle.rect.y - 10  # Position ball above paddle
        self.game.ball.dy = 4  # Set ball direction down
        self.game.ball.move()
        self.game.ball.rect.y += self.game.ball.dy  # Move ball down to collide with paddle
        self.game.ball.move()  # Check for collision
        self.assertEqual(self.game.ball.dy, -4)  # Ball should bounce up
    def test_brick_split(self):
        brick = Brick(100, 100)
        brick.split()  # Split the brick
        self.assertEqual(brick.life, 2)  # Original brick life should decrease
        self.assertEqual(len(self.game.bricks), 51)  # One brick should be added
    def tearDown(self):
        pygame.quit()
if __name__ == '__main__':
    unittest.main()
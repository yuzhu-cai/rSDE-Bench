import unittest
import pygame
import json
import time
from main import Game, Paddle, Ball, Brick
class TestBrickBreakerGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()
        self.log_file = open('test_game.log', 'w')  # Create a test log file
    def tearDown(self):
        self.log_file.close()
        pygame.quit()
    def test_paddle_movement_left(self):
        initial_position = self.game.paddle.rect.x
        self.game.paddle.move(-10)
        self.assertEqual(self.game.paddle.rect.x, initial_position - 10)
        self.game.log_event(time.time(), "PADDLE_MOVE_LEFT", self.log_file)
    def test_paddle_movement_right(self):
        initial_position = self.game.paddle.rect.x
        self.game.paddle.move(10)
        self.assertEqual(self.game.paddle.rect.x, initial_position + 10)
        self.game.log_event(time.time(), "PADDLE_MOVE_RIGHT", self.log_file)
    def test_ball_bounce_wall(self):
        self.game.ball.rect.x = 0  # Position the ball at the left wall
        self.game.ball.dx = -4  # Set direction towards the wall
        self.game.ball.move()
        self.assertEqual(self.game.ball.dx, 4)  # Ball should bounce back
        self.game.log_event(time.time(), "BOUNCE_WALL", self.log_file)
    def test_ball_bounce_paddle(self):
        self.game.ball.rect.x = self.game.paddle.rect.x + 10  # Position ball above paddle
        self.game.ball.rect.y = self.game.paddle.rect.y - 10
        self.game.ball.move()
        self.assertEqual(self.game.ball.dy, 4)  # Ball should bounce up
        self.game.log_event(time.time(), "BOUNCE_PADDLE", self.log_file)
    def test_ball_bounce_brick(self):
        brick = Brick(100, 100)
        self.game.bricks.append(brick)
        self.game.ball.rect.x = brick.rect.x + 10  # Position ball above brick
        self.game.ball.rect.y = brick.rect.y - 10
        self.game.ball.move()
        self.assertEqual(self.game.ball.dy, 4)  # Ball should bounce up
        new_bricks = brick.split()
        if new_bricks:
            self.game.bricks.remove(brick)
            self.game.bricks.extend(new_bricks)
        self.assertEqual(len(self.game.bricks), 3)  # Original brick splits into 2 new bricks
        self.game.log_event(time.time(), "BOUNCE_BRICK", self.log_file)
    def test_ball_lost(self):
        self.game.ball.rect.y = self.game.paddle.rect.y + 50  # Position ball below paddle
        self.game.ball.move()
        self.assertTrue(self.game.ball.rect.y > 600)  # Ball should be lost
        self.game.log_event(time.time(), "BALL_LOST", self.log_file)
if __name__ == '__main__':
    unittest.main()
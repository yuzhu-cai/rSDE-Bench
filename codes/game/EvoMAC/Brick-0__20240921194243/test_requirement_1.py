'''
Test the logging mechanism of the Brick Breaker game to ensure that events are logged correctly 
with the right format and order after each action is taken.
'''
import unittest
import json
import os
from unittest.mock import patch
from main import Game
class TestGameLogging(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.log_file_path = 'game.log'
    def tearDown(self):
        # Remove the log file after each test
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)
    def test_log_paddle_move_left(self):
        with open(self.log_file_path, 'w') as log_file:
            self.game.paddle.move(-10)
            self.game.log_event(1, "PADDLE_MOVE_LEFT", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "PADDLE_MOVE_LEFT")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
    def test_log_paddle_move_right(self):
        with open(self.log_file_path, 'w') as log_file:
            self.game.paddle.move(10)
            self.game.log_event(1, "PADDLE_MOVE_RIGHT", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "PADDLE_MOVE_RIGHT")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
    def test_log_bounce_wall(self):
        with open(self.log_file_path, 'w') as log_file:
            self.game.ball.rect.x = 0  # Simulate ball hitting the left wall
            self.game.ball.dx = -4  # Move ball left
            self.game.ball.move()
            self.game.log_event(1, "BOUNCE_WALL", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "BOUNCE_WALL")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
    def test_log_bounce_paddle(self):
        with open(self.log_file_path, 'w') as log_file:
            self.game.ball.rect.x = self.game.paddle.rect.x + 10  # Position ball above paddle
            self.game.ball.rect.y = self.game.paddle.rect.y - 10
            self.game.ball.move()
            self.game.log_event(1, "BOUNCE_PADDLE", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "BOUNCE_PADDLE")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
    def test_log_bounce_brick(self):
        with open(self.log_file_path, 'w') as log_file:
            # Simulate ball hitting a brick
            brick = self.game.bricks[0]
            self.game.ball.rect.x = brick.rect.x + 10  # Position ball above the brick
            self.game.ball.rect.y = brick.rect.y - 10
            self.game.ball.move()
            self.game.log_event(1, "BOUNCE_BRICK", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "BOUNCE_BRICK")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
    def test_log_ball_lost(self):
        with open(self.log_file_path, 'w') as log_file:
            self.game.ball.rect.y = HEIGHT + 10  # Simulate ball falling off the screen
            self.game.log_event(1, "BALL_LOST", log_file)
        with open(self.log_file_path, 'r') as log_file:
            log_entries = log_file.readlines()
            self.assertEqual(len(log_entries), 1)
            log_entry = json.loads(log_entries[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "BALL_LOST")
            self.assertEqual(log_entry["paddle_position"], [self.game.paddle.rect.x, self.game.paddle.rect.y])
            self.assertEqual(log_entry["ball_position"], [self.game.ball.rect.x, self.game.ball.rect.y])
            self.assertEqual(len(log_entry["bricks_info"]), len(self.game.bricks))
if __name__ == '__main__':
    unittest.main()
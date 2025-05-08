'''
REQUIREMENTS
Test the logging mechanism for special triggered conditions, such as when a brick splits or when the ball is lost. Ensure that these events are logged correctly according to the specified format.
'''
import unittest
import json
import time
from unittest.mock import patch, MagicMock
from main import Game, Paddle, Ball, Brick
class TestBrickBreakerLogging(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.log_file = MagicMock()
        self.timestamp = time.time()
    def test_brick_split_logging(self):
        # Simulate a scenario where a brick is hit and splits
        original_brick = self.game.bricks[0]
        original_brick.life = 1  # Set life to 1 so it can split
        self.game.ball.rect.x = original_brick.rect.x + 1  # Position ball to collide with the brick
        self.game.ball.rect.y = original_brick.rect.y + 1
        # Log the event before the collision
        self.game.log_event(self.timestamp, "BOUNCE_BRICK", self.log_file)
        # Perform the collision
        self.game.ball.dy *= -1  # Simulate the ball bouncing off
        new_bricks = original_brick.split()
        if new_bricks:
            self.game.bricks.remove(original_brick)
            self.game.bricks.extend(new_bricks)
        # Log the event after the collision
        self.game.log_event(self.timestamp, "BOUNCE_BRICK", self.log_file)
        # Check if the log file was called correctly
        self.log_file.write.assert_called()
        logged_entries = [json.loads(call[0][0]) for call in self.log_file.write.call_args_list]
        # Check the first log entry for brick split
        self.assertEqual(logged_entries[0]["EVENT_TYPE"], "BOUNCE_BRICK")
        self.assertEqual(logged_entries[0]["bricks_info"][0][2], 0)  # Original brick should have 0 life
        self.assertEqual(len(logged_entries[0]["bricks_info"]), 3)  # Two new bricks + one original brick
    def test_ball_lost_logging(self):
        # Simulate the ball falling off the screen
        self.game.ball.rect.y = self.game.ball.rect.y + 100  # Move ball down to simulate loss
        # Log the event of ball lost
        self.game.log_event(self.timestamp, "BALL_LOST", self.log_file)
        # Check if the log file was called correctly
        self.log_file.write.assert_called()
        logged_entries = [json.loads(call[0][0]) for call in self.log_file.write.call_args_list]
        # Check the last log entry for ball lost
        self.assertEqual(logged_entries[-1]["EVENT_TYPE"], "BALL_LOST")
        self.assertEqual(logged_entries[-1]["ball_position"][1], self.game.ball.rect.y)  # Check ball position
if __name__ == '__main__':
    unittest.main()
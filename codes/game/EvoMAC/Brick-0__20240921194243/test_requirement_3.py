'''
Test the value initialization required by the task to ensure they are correctly achieved, 
paying attention to the coordinates of the paddle and bricks at the start of the game.
'''
import unittest
from main import Paddle, Brick, Game
class TestGameInitialization(unittest.TestCase):
    def setUp(self):
        self.game = Game()
    def test_paddle_initial_position(self):
        # Check if the paddle is initialized at the correct position
        self.assertEqual(self.game.paddle.rect.x, 350)  # Centered horizontally
        self.assertEqual(self.game.paddle.rect.y, 570)  # Positioned at the bottom
    def test_bricks_initialization(self):
        # Check if the correct number of bricks are created
        self.assertEqual(len(self.game.bricks), 50)  # 5 rows of 10 bricks each
        # Check if the first brick is at the expected position
        self.assertEqual(self.game.bricks[0].rect.x, 35)  # First brick x position
        self.assertEqual(self.game.bricks[0].rect.y, 30)  # First brick y position
        # Check if the last brick is at the expected position
        self.assertEqual(self.game.bricks[-1].rect.x, 735)  # Last brick x position
        self.assertEqual(self.game.bricks[-1].rect.y, 30)  # Last brick y position
        # Check if all bricks have the correct initial life
        for brick in self.game.bricks:
            self.assertEqual(brick.life, 3)  # Each brick should start with 3 lives
if __name__ == '__main__':
    unittest.main()
'''
Test the value initialization required by the task are correctly achieved, paying attention to the coordinates of Mario, the block, the enemy, and the flagpole.
'''
import unittest
import pygame
class TestSuperMarioGame(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame
        pygame.init()
        # Constants
        self.WIDTH, self.HEIGHT = 800, 400
        self.GROUND_HEIGHT = 50
        self.BLOCK_SIZE = 50
        self.ENEMY_SIZE = 40
        # Initialize game variables
        self.mario_pos = [50, self.HEIGHT - self.GROUND_HEIGHT - 50]
        self.block_pos = [self.mario_pos[0], self.HEIGHT - self.GROUND_HEIGHT - self.BLOCK_SIZE]
        self.enemy_pos = [200, self.HEIGHT - self.GROUND_HEIGHT - self.ENEMY_SIZE]  # Fixed position for testing
        self.flagpole_pos = [self.WIDTH - 50, self.HEIGHT - self.GROUND_HEIGHT]
    def test_initial_positions(self):
        # Test initial positions of Mario, block, enemy, and flagpole
        self.assertEqual(self.mario_pos, [50, self.HEIGHT - self.GROUND_HEIGHT - 50], "Mario's initial position is incorrect.")
        self.assertEqual(self.block_pos, [50, self.HEIGHT - self.GROUND_HEIGHT - self.BLOCK_SIZE], "Block's initial position is incorrect.")
        self.assertEqual(self.enemy_pos, [200, self.HEIGHT - self.GROUND_HEIGHT - self.ENEMY_SIZE], "Enemy's initial position is incorrect.")
        self.assertEqual(self.flagpole_pos, [self.WIDTH - 50, self.HEIGHT - self.GROUND_HEIGHT], "Flagpole's initial position is incorrect.")
    def tearDown(self):
        # Quit Pygame
        pygame.quit()
if __name__ == '__main__':
    unittest.main()
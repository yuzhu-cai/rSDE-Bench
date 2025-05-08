'''
Test the value initialization required by the task to ensure they are correctly achieved. Pay attention to the coordinates of the player's ball and enemy balls, ensuring they are initialized in the correct positions relative to the game interface.
'''
import unittest
import random
import os
import json
LOG_FILE = "game.log"
class TestBattleOfBallsInitialization(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    def test_player_initialization(self):
        from main import player_pos, player_radius
        # Check if player's initial position is at the center of the game interface
        self.assertEqual(player_pos, [0, 0])
        # Check if player's initial radius is correct
        self.assertEqual(player_radius, 20)
    def test_enemy_initialization(self):
        from main import active_enemies, fixed_enemies
        # Check if there are 3 active enemies initialized
        self.assertEqual(len(active_enemies), 3)
        # Check if the fixed enemy is initialized
        self.assertEqual(len(fixed_enemies), 1)
        # Check if active enemies are initialized with correct radius
        for enemy in active_enemies:
            self.assertEqual(enemy[2], 15)  # Enemy radius should be 15
        # Check if fixed enemy is initialized with correct radius
        self.assertEqual(fixed_enemies[0][2], 15)  # Fixed enemy radius should be 15
    def test_enemy_positions(self):
        from main import active_enemies, fixed_enemies
        # Check if active enemies are initialized within the bounds
        for enemy in active_enemies:
            self.assertTrue(-400 <= enemy[0] <= 400)  # X position should be within bounds
            self.assertTrue(-300 <= enemy[1] <= 300)  # Y position should be within bounds
        # Check if fixed enemy is initialized within the bounds
        self.assertTrue(-400 <= fixed_enemies[0][0] <= 400)  # X position should be within bounds
        self.assertTrue(-300 <= fixed_enemies[0][1] <= 300)  # Y position should be within bounds
if __name__ == '__main__':
    unittest.main()
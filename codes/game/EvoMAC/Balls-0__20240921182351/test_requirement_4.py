'''
Test the function inputs and the global variables imported in each function. Ensure that the input values and global variables used in the functions are valid and involved when the function is called.
'''
import unittest
import json
import os
import random
from main import log_event, player_pos, player_radius, active_enemies, fixed_enemies, small_balls, spawn_small_ball, check_collisions
LOG_FILE = "game.log"
class TestBattleOfBallsFunctions(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        # Reset game state
        global player_pos, player_radius, active_enemies, fixed_enemies, small_balls
        player_pos = [0, 0]
        player_radius = 20
        active_enemies = [[random.randint(-400, 400), random.randint(-300, 300), 15] for _ in range(3)]
        fixed_enemies = [[random.randint(-400, 400), random.randint(-300, 300), 15]]
        small_balls = []
    def test_spawn_small_ball(self):
        # Test the spawning of small balls
        spawn_small_ball()
        self.assertEqual(len(small_balls), 1)
        self.assertEqual(small_balls[0][2], 5)  # Check if the radius is correct
    def test_check_collisions_with_small_ball(self):
        # Test collision with small balls
        spawn_small_ball()
        small_balls[0][0] = 0  # Position small ball at the player's position
        small_balls[0][1] = 0
        initial_radius = player_radius
        check_collisions()
        self.assertGreater(player_radius, initial_radius)  # Player's radius should increase
    def test_check_collisions_with_active_enemy(self):
        # Test collision with active enemies
        active_enemies[0][0] = 0  # Position enemy at the player's position
        active_enemies[0][1] = 0
        initial_radius = player_radius
        check_collisions()
        self.assertGreater(player_radius, initial_radius)  # Player's radius should increase
    def test_check_collisions_with_fixed_enemy(self):
        # Test collision with fixed enemies
        fixed_enemies[0][0] = 0  # Position fixed enemy at the player's position
        fixed_enemies[0][1] = 0
        initial_radius = player_radius
        check_collisions()
        self.assertGreater(player_radius, initial_radius)  # Player's radius should increase
if __name__ == '__main__':
    unittest.main()
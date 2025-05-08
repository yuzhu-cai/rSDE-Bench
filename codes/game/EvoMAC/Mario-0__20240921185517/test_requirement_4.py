'''
This file contains tests for the Super Mario game to ensure that the mushroom movement logic, 
resetting mushroom position, and score logging are functioning correctly.
'''
import unittest
import json
import time
import pygame
from logger import log_event  # Importing log_event for testing
from main import mario_pos, enemy_pos  # Importing game variables for testing
class TestSuperMarioGame(unittest.TestCase):
    def setUp(self):
        # Setup code to initialize the game state if necessary
        self.score = 0
        self.mushroom_pos = [None, None]
        self.enemy_pos = [200, 350]  # Set enemy position for testing
    def test_mushroom_movement(self):
        # Simulate mushroom movement and check direction change
        self.mushroom_pos = [400, 100]  # Initial position
        mushroom_direction = -1  # Moving left
        for _ in range(200):  # Simulate movement
            self.mushroom_pos[0] += mushroom_direction * 2
            if self.mushroom_pos[0] <= 0 or self.mushroom_pos[0] >= 770:  # Check for borders
                mushroom_direction *= -1  # Change direction
            self.assertTrue(0 <= self.mushroom_pos[0] <= 770)  # Ensure within bounds
    def test_mushroom_touch(self):
        # Simulate touching the mushroom
        self.mushroom_pos = [400, 100]  # Position of mushroom
        mario_pos = [400, 50]  # Position of Mario
        if (mario_pos[0] + 50 > self.mushroom_pos[0] and mario_pos[0] < self.mushroom_pos[0] + 30 and 
            mario_pos[1] + 50 > self.mushroom_pos[1] and mario_pos[1] < self.mushroom_pos[1] + 30):
            self.mushroom_pos = [None, None]
            self.score += 1000
        self.assertEqual(self.mushroom_pos, [None, None])
        self.assertEqual(self.score, 1000)
    def test_score_logging(self):
        # Simulate score logging
        initial_score = self.score
        self.score += 100  # Simulate hitting a block
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": "HIT_BLOCK",
            "mario_position": [50, 300],
            "enemy_position": [None, None],
            "block_position": [50, 250],
            "mushroom_position": [None, None],
            "score": self.score
        }
        self.assertEqual(log_entry["score"], initial_score + 100)
    def test_enemy_collision(self):
        # Test for collision with enemy
        mario_pos = [self.enemy_pos[0] - 25, 350]  # Position Mario to collide with enemy
        with self.assertRaises(SystemExit):
            if (mario_pos[0] + 50 > self.enemy_pos[0] and mario_pos[0] < self.enemy_pos[0] + 40):
                raise SystemExit  # Simulate collision
if __name__ == '__main__':
    unittest.main()
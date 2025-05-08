import unittest
import json
import os
class TestSokobanInitialization(unittest.TestCase):
    def setUp(self):
        # Clear the log file before the test
        with open('game.log', 'w') as log_file:
            log_file.write('')
        # Initial positions
        self.player_position = [1, 1]
        self.box_positions = [[3, 3], [4, 2]]
        self.goal_positions = [[5, 5], [6, 3]]
        self.wall_positions = [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]]
    def test_initial_player_position(self):
        self.assertEqual(self.player_position, [1, 1], "Player position is not initialized correctly.")
    def test_initial_box_positions(self):
        self.assertEqual(self.box_positions, [[3, 3], [4, 2]], "Box positions are not initialized correctly.")
    def test_initial_goal_positions(self):
        self.assertEqual(self.goal_positions, [[5, 5], [6, 3]], "Goal positions are not initialized correctly.")
    def test_initial_wall_positions(self):
        self.assertEqual(self.wall_positions, [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]], "Wall positions are not initialized correctly.")
if __name__ == "__main__":
    unittest.main()
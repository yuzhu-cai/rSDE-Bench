'''
Test the logging mechanism for the special triggered conditions, such as eating a superpellet, colliding with another ghost, and the monster being activated.
'''
import unittest
import json
import time
from unittest.mock import patch, mock_open
from main import log_event, ghost_position, other_ghost_positions, superpellet_positions, monster_position, game_status
class TestGhostlyGameLogging(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_eat_superpellet_logging(self, mock_file):
        global ghost_position, superpellet_positions, game_status
        ghost_position = [5, 5]  # Position on superpellet
        superpellet_positions = [[5, 5]]  # Superpellet exists at this position
        log_event("eat_superpellet", "right", ghost_position, monster_position, game_status)
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["event_type"], "eat_superpellet")
        self.assertEqual(log_entry["ghost_position"], ghost_position)
        self.assertEqual(log_entry["monster_position"], monster_position)
        self.assertEqual(log_entry["game_status"], game_status)
    @patch('builtins.open', new_callable=mock_open)
    def test_collide_with_other_ghost_logging(self, mock_file):
        global ghost_position, other_ghost_positions, game_status
        ghost_position = [0, 5]  # Position on another ghost
        other_ghost_positions = [[0, 5]]  # Other ghost exists at this position
        game_status = "ongoing"
        log_event("eat_other_ghost", "left", ghost_position, monster_position, game_status)
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["event_type"], "eat_other_ghost")
        self.assertEqual(log_entry["ghost_position"], ghost_position)
        self.assertEqual(log_entry["monster_position"], monster_position)
        self.assertEqual(log_entry["game_status"], game_status)
    @patch('builtins.open', new_callable=mock_open)
    def test_monster_activation_logging(self, mock_file):
        global monster_position, game_status
        monster_position = [-1, -1]  # Monster not activated yet
        game_status = "ongoing"
        # Simulate monster activation
        monster_position = [1, 1]  # Monster activated
        log_event("monster_eat_ghost", "", ghost_position, monster_position, "lose")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["event_type"], "monster_eat_ghost")
        self.assertEqual(log_entry["ghost_position"], ghost_position)
        self.assertEqual(log_entry["monster_position"], monster_position)
        self.assertEqual(log_entry["game_status"], "lose")
if __name__ == '__main__':
    unittest.main()
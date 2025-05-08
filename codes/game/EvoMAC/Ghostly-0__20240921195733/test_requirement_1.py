'''
Test the logging mechanism of the Ghostly game to ensure that events are logged correctly after player actions.
'''
import unittest
import json
import time
from unittest.mock import patch, mock_open
from main import log_event, ghost_position, monster_position, game_status, pellet_positions, superpellet_positions, other_ghost_positions, walls_position
class TestLoggingMechanism(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_log_event_eat_pellet(self, mock_file):
        global ghost_position, monster_position, game_status, pellet_positions
        # Initial state
        ghost_position = [1, 1]
        monster_position = [-1, -1]
        game_status = "ongoing"
        pellet_positions = [[3, 3], [4, 2]]
        # Simulate eating a pellet
        ghost_position = [3, 3]
        pellet_positions.remove(ghost_position)
        log_event("eat_pellet", "right", ghost_position, monster_position, game_status)
        # Check the log file
        mock_file().write.assert_called()
        log_content = mock_file().write.call_args[0][0]
        log_entry = json.loads(log_content)
        # Assertions
        self.assertEqual(log_entry["event_type"], "eat_pellet")
        self.assertEqual(log_entry["move_direction"], "right")
        self.assertEqual(log_entry["ghost_position"], [3, 3])
        self.assertEqual(log_entry["monster_position"], [-1, -1])
        self.assertEqual(log_entry["game_status"], "ongoing")
    @patch('builtins.open', new_callable=mock_open)
    def test_log_event_invalid_move(self, mock_file):
        global ghost_position, monster_position, game_status
        # Initial state
        ghost_position = [1, 1]
        monster_position = [-1, -1]
        game_status = "ongoing"
        # Simulate an invalid move (hitting a wall)
        ghost_position = [0, 4]  # Wall position
        log_event("invalid_move", "up", ghost_position, monster_position, game_status)
        # Check the log file
        mock_file().write.assert_called()
        log_content = mock_file().write.call_args[0][0]
        log_entry = json.loads(log_content)
        # Assertions
        self.assertEqual(log_entry["event_type"], "invalid_move")
        self.assertEqual(log_entry["move_direction"], "up")
        self.assertEqual(log_entry["ghost_position"], [0, 4])
        self.assertEqual(log_entry["monster_position"], [-1, -1])
        self.assertEqual(log_entry["game_status"], "ongoing")
    @patch('builtins.open', new_callable=mock_open)
    def test_log_event_eat_superpellet(self, mock_file):
        global ghost_position, monster_position, game_status, superpellet_positions
        # Initial state
        ghost_position = [1, 1]
        monster_position = [-1, -1]
        game_status = "ongoing"
        superpellet_positions = [[5, 5], [6, 3]]
        # Simulate eating a superpellet
        ghost_position = [5, 5]
        superpellet_positions.remove(ghost_position)
        log_event("eat_superpellet", "down", ghost_position, monster_position, game_status)
        # Check the log file
        mock_file().write.assert_called()
        log_content = mock_file().write.call_args[0][0]
        log_entry = json.loads(log_content)
        # Assertions
        self.assertEqual(log_entry["event_type"], "eat_superpellet")
        self.assertEqual(log_entry["move_direction"], "down")
        self.assertEqual(log_entry["ghost_position"], [5, 5])
        self.assertEqual(log_entry["monster_position"], [-1, -1])
        self.assertEqual(log_entry["game_status"], "ongoing")
    @patch('builtins.open', new_callable=mock_open)
    def test_log_event_eat_other_ghost(self, mock_file):
        global ghost_position, monster_position, game_status, other_ghost_positions
        # Initial state
        ghost_position = [1, 1]
        monster_position = [-1, -1]
        game_status = "ongoing"
        other_ghost_positions = [[3, 5]]
        # Simulate eating another ghost
        ghost_position = [3, 5]
        other_ghost_positions.remove(ghost_position)
        log_event("eat_other_ghost", "down", ghost_position, monster_position, game_status)
        # Check the log file
        mock_file().write.assert_called()
        log_content = mock_file().write.call_args[0][0]
        log_entry = json.loads(log_content)
        # Assertions
        self.assertEqual(log_entry["event_type"], "eat_other_ghost")
        self.assertEqual(log_entry["move_direction"], "down")
        self.assertEqual(log_entry["ghost_position"], [3, 5])
        self.assertEqual(log_entry["monster_position"], [-1, -1])
        self.assertEqual(log_entry["game_status"], "ongoing")
if __name__ == '__main__':
    unittest.main()
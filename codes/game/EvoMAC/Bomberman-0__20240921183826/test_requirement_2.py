'''
Test the logging mechanism for special triggered conditions, such as when the player or enemies are injured, when bombs are placed, and when explosions occur. Ensure that the log accurately reflects these events and their impact on the game state.
'''
import unittest
import json
import time
from unittest.mock import patch, mock_open
from main import update_log, explode_bomb, PLAYER_START_POS, INITIAL_PLAYER_HEALTH, INITIAL_ENEMY_HEALTH
class TestBombermanLogging(unittest.TestCase):
    def setUp(self):
        self.player_health = INITIAL_PLAYER_HEALTH
        self.enemies_health = [INITIAL_ENEMY_HEALTH, INITIAL_ENEMY_HEALTH]
        self.score = 0
        self.bomb_pos = (1, 1)
    @patch("builtins.open", new_callable=mock_open)
    def test_log_injury_event(self, mock_file):
        # Simulate player injury
        self.player_health -= 10
        update_log("INJURED")
        # Check if the log file was written to
        mock_file().write.assert_called()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        # Check the log entry format
        self.assertEqual(log_entry["EVENT_TYPE"], "INJURED")
        self.assertEqual(log_entry["player"]["health"], self.player_health)
        self.assertEqual(log_entry["player"]["score"], self.score)
    @patch("builtins.open", new_callable=mock_open)
    def test_log_enemy_injury_event(self, mock_file):
        # Simulate enemy injury
        self.enemies_health[0] = 0  # Enemy defeated
        self.score += 100
        update_log("INJURED")
        # Check if the log file was written to
        mock_file().write.assert_called()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        # Check the log entry format
        self.assertEqual(log_entry["EVENT_TYPE"], "INJURED")
        self.assertEqual(log_entry["player"]["health"], self.player_health)
        self.assertEqual(log_entry["player"]["score"], self.score)
        self.assertEqual(log_entry["enemies"][0]["health"], 0)
    @patch("builtins.open", new_callable=mock_open)
    def test_log_bomb_placement_event(self, mock_file):
        # Simulate bomb placement
        update_log("PLACE_BOMB")
        # Check if the log file was written to
        mock_file().write.assert_called()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        # Check the log entry format
        self.assertEqual(log_entry["EVENT_TYPE"], "PLACE_BOMB")
        self.assertEqual(log_entry["player"]["health"], self.player_health)
        self.assertEqual(log_entry["player"]["score"], self.score)
    @patch("builtins.open", new_callable=mock_open)
    def test_log_explosion_event(self, mock_file):
        # Simulate bomb explosion
        explode_bomb(self.bomb_pos)
        # Check if the log file was written to
        mock_file().write.assert_called()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        # Check the log entry format
        self.assertEqual(log_entry["EVENT_TYPE"], "BOOM")
        self.assertEqual(log_entry["player"]["health"], self.player_health)
        self.assertEqual(log_entry["player"]["score"], self.score)
if __name__ == "__main__":
    unittest.main()
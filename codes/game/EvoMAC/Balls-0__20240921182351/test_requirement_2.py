'''
Test the logging mechanism for special triggered conditions, such as when the player's ball consumes an enemy ball or when the game ends due to the player's ball being consumed. Ensure that these events are logged correctly and that the log entries reflect the appropriate game state.
'''
import unittest
import json
import os
import time
from main import log_event, player_pos, player_radius, active_enemies, fixed_enemies, small_balls
LOG_FILE = "game.log"
class TestBattleOfBallsSpecialConditions(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        # Initialize game state for testing
        player_pos[0] = 0
        player_pos[1] = 0
        player_radius = 20
        active_enemies.clear()
        fixed_enemies.clear()
        small_balls.clear()
        # Add an enemy ball for testing
        active_enemies.append([0, 0, 15])  # Same position as player for collision
    def test_enemy_consumption_logging(self):
        # Simulate the player consuming an enemy ball
        log_event("EAT_ENEMY")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "EAT_ENEMY")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
        self.assertEqual(log_entry["game_state"]["player"]["radius"], player_radius + 15)  # Player radius should increase
    def test_fixed_enemy_consumption_logging(self):
        # Add a fixed enemy and simulate consumption
        fixed_enemies.append([0, 0, 15])  # Same position as player for collision
        log_event("EAT_FIXED_ENEMY")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "EAT_FIXED_ENEMY")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
        self.assertEqual(log_entry["game_state"]["player"]["radius"], player_radius + 15)  # Player radius should increase
    def test_game_over_logging(self):
        # Simulate the player being consumed by an enemy
        active_enemies.append([0, 0, 25])  # Larger enemy to consume player
        log_event("GAME_OVER")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "GAME_OVER")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
        self.assertEqual(log_entry["game_state"]["player"]["radius"], player_radius)  # Player radius should remain unchanged
if __name__ == '__main__':
    unittest.main()
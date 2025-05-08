'''
Test the logging mechanism to ensure it captures the initial state and player movements correctly.
'''
import unittest
import json
import os
from main import log_event, player_pos, player_radius, active_enemies, fixed_enemies, small_balls
LOG_FILE = "game.log"
class TestBattleOfBallsLogging(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    def test_initial_log_entry(self):
        # Simulate the game initialization
        log_event("INIT")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "INIT")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
        self.assertEqual(log_entry["game_state"]["player"]["radius"], player_radius)
        self.assertEqual(len(log_entry["game_state"]["active_enemies"]), len(active_enemies))
        self.assertEqual(len(log_entry["game_state"]["fixed_enemies"]), len(fixed_enemies))
        self.assertEqual(len(log_entry["game_state"]["small_balls"]), len(small_balls))
    def test_movement_logging(self):
        # Simulate movement and log the event
        player_pos[0] = 5  # Simulate movement
        log_event("MOVE_RIGHT")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "MOVE_RIGHT")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
    def test_multiple_movements_logging(self):
        # Simulate multiple movements and log the events
        movements = [("MOVE_LEFT", -5), ("MOVE_UP", -5), ("MOVE_DOWN", 5), ("MOVE_RIGHT", 5)]
        for event_type, change in movements:
            player_pos[0] += change if "RIGHT" in event_type else 0
            player_pos[1] += change if "UP" in event_type else 0
            log_event(event_type)
        with open(LOG_FILE, 'r') as log_file:
            log_entries = [json.loads(line) for line in log_file.readlines()]
        for i, (event_type, _) in enumerate(movements):
            self.assertEqual(log_entries[i]["EVENT_TYPE"], event_type)
            self.assertEqual(log_entries[i]["game_state"]["player"]["position"], player_pos)
if __name__ == '__main__':
    unittest.main()
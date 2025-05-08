'''
This file contains tests for the Battle of Balls game, specifically focusing on the logging mechanism to ensure it captures the initial state and player movements correctly.
'''
import unittest
import json
import os
LOG_FILE = "game.log"
class TestBattleOfBallsLogging(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    def test_initial_log_entry(self):
        # Simulate the game initialization
        from main import log_event, player_pos, player_radius, active_enemies, fixed_enemies, small_balls
        log_event("INIT")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "INIT")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
        self.assertEqual(log_entry["game_state"]["player"]["radius"], player_radius)
    def test_movement_logging(self):
        from main import log_event, player_pos
        player_pos[0] = 5  # Simulate movement
        log_event("MOVE_RIGHT")
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "MOVE_RIGHT")
        self.assertEqual(log_entry["game_state"]["player"]["position"], player_pos)
    def test_small_ball_spawn_logging(self):
        from main import spawn_small_ball, small_balls
        spawn_small_ball()
        with open(LOG_FILE, 'r') as log_file:
            log_entry = json.loads(log_file.readline())
        self.assertEqual(log_entry["EVENT_TYPE"], "SPAWN_SMALL_BALL")
        self.assertEqual(len(small_balls), 1)  # Ensure one small ball is spawned
if __name__ == '__main__':
    unittest.main()
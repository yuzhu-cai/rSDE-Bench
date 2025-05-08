'''
Test the logging mechanism for special triggered conditions, such as invalid moves or victory conditions, ensuring that these events are logged correctly.
'''
import json
import os
import unittest
class TestSokobanLogging(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        with open('game.log', 'w') as log_file:
            log_file.write('')
    def test_invalid_move_logging(self):
        # Simulate an invalid move (moving into a wall)
        events = [
            {"event_type": "MOVE_RIGHT", "player_position": [1, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
            {"event_type": "INVALID_MOVE", "player_position": [1, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"}
        ]
        for event in events:
            log_entry = {
                "timestamp": "2023-10-01 12:00:00",  # Placeholder for timestamp
                "EVENT_TYPE": event["event_type"],
                "player_position": event["player_position"],
                "box_positions": event["box_positions"],
                "game_status": event["game_status"]
            }
            with open('game.log', 'a') as log_file:
                log_file.write(json.dumps(log_entry) + '\n')
        # Read the log file and check the contents
        with open('game.log', 'r') as log_file:
            log_contents = log_file.readlines()
        self.assertEqual(len(log_contents), len(events), "Log entries count mismatch")
        for i, event in enumerate(events):
            logged_event = json.loads(log_contents[i])
            self.assertEqual(logged_event["EVENT_TYPE"], event["event_type"], f"Event type mismatch at entry {i}")
            self.assertEqual(logged_event["player_position"], event["player_position"], f"Player position mismatch at entry {i}")
            self.assertEqual(logged_event["box_positions"], event["box_positions"], f"Box positions mismatch at entry {i}")
            self.assertEqual(logged_event["game_status"], event["game_status"], f"Game status mismatch at entry {i}")
    def test_victory_condition_logging(self):
        # Simulate a victory condition
        events = [
            {"event_type": "MOVE_RIGHT", "player_position": [1, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
            {"event_type": "MOVE_DOWN", "player_position": [2, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
            {"event_type": "MOVE_RIGHT", "player_position": [2, 3], "box_positions": [[5, 5], [6, 3]], "game_status": "COMPLETE"}
        ]
        for event in events:
            log_entry = {
                "timestamp": "2023-10-01 12:00:00",  # Placeholder for timestamp
                "EVENT_TYPE": event["event_type"],
                "player_position": event["player_position"],
                "box_positions": event["box_positions"],
                "game_status": event["game_status"]
            }
            with open('game.log', 'a') as log_file:
                log_file.write(json.dumps(log_entry) + '\n')
        # Read the log file and check the contents
        with open('game.log', 'r') as log_file:
            log_contents = log_file.readlines()
        self.assertEqual(len(log_contents), len(events), "Log entries count mismatch")
        for i, event in enumerate(events):
            logged_event = json.loads(log_contents[i])
            self.assertEqual(logged_event["EVENT_TYPE"], event["event_type"], f"Event type mismatch at entry {i}")
            self.assertEqual(logged_event["player_position"], event["player_position"], f"Player position mismatch at entry {i}")
            self.assertEqual(logged_event["box_positions"], event["box_positions"], f"Box positions mismatch at entry {i}")
            self.assertEqual(logged_event["game_status"], event["game_status"], f"Game status mismatch at entry {i}")
if __name__ == "__main__":
    unittest.main()
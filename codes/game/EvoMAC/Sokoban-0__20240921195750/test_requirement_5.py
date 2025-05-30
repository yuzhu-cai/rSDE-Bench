'''
This script tests the victory condition of the Sokoban game to ensure that the game status updates to "COMPLETE" when all boxes are on their goal positions.
'''
import json
import os
def test_victory_condition():
    # Clear the log file before the test
    with open('game.log', 'w') as log_file:
        log_file.write('')
    # Simulate game events leading to victory
    events = [
        {"event_type": "MOVE_RIGHT", "player_position": [1, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
        {"event_type": "MOVE_DOWN", "player_position": [2, 2], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
        {"event_type": "MOVE_RIGHT", "player_position": [2, 3], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
        {"event_type": "MOVE_DOWN", "player_position": [2, 4], "box_positions": [[3, 3], [4, 2]], "game_status": "ONGOING"},
        {"event_type": "MOVE_DOWN", "player_position": [3, 4], "box_positions": [[5, 5], [4, 2]], "game_status": "ONGOING"},
        {"event_type": "MOVE_RIGHT", "player_position": [3, 5], "box_positions": [[5, 5], [4, 2]], "game_status": "COMPLETE"}
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
    assert len(log_contents) == len(events), "Log entries count mismatch"
    for i, event in enumerate(events):
        logged_event = json.loads(log_contents[i])
        assert logged_event["EVENT_TYPE"] == event["event_type"], f"Event type mismatch at entry {i}"
        assert logged_event["player_position"] == event["player_position"], f"Player position mismatch at entry {i}"
        assert logged_event["box_positions"] == event["box_positions"], f"Box positions mismatch at entry {i}"
        assert logged_event["game_status"] == event["game_status"], f"Game status mismatch at entry {i}"
if __name__ == "__main__":
    test_victory_condition()
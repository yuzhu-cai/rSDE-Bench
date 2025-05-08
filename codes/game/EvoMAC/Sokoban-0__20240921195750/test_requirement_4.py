'''
This script tests the function inputs and global variables used in the move_player function of the Sokoban game.
'''
import json
import os
import time
# Import the main game module
from main import player_position, box_positions, log_event, move_player, game_status
def test_move_player():
    # Clear the log file before the test
    with open('game.log', 'w') as log_file:
        log_file.write('')
    # Initial state
    initial_player_position = player_position[:]
    initial_box_positions = box_positions[:]
    # Move player right
    move_player(1, 0)
    assert player_position == [2, 1], "Player position should be updated to [2, 1]"
    assert box_positions == initial_box_positions, "Box positions should remain unchanged"
    # Move player down
    move_player(0, 1)
    assert player_position == [2, 2], "Player position should be updated to [2, 2]"
    assert box_positions == initial_box_positions, "Box positions should remain unchanged"
    # Move player right into a box
    move_player(1, 0)  # This should move the box
    assert player_position == [2, 2], "Player position should be updated to [2, 2]"
    assert box_positions == [[4, 2], [3, 3]], "Box positions should be updated after moving the box"
    # Move player down into a wall (invalid move)
    move_player(0, 1)
    assert player_position == [2, 2], "Player position should remain unchanged after invalid move"
    # Move player left (valid move)
    move_player(-1, 0)
    assert player_position == [1, 2], "Player position should be updated to [1, 2]"
    # Check log entries
    with open('game.log', 'r') as log_file:
        log_contents = log_file.readlines()
    assert len(log_contents) > 0, "Log should contain entries"
    for entry in log_contents:
        logged_event = json.loads(entry)
        assert logged_event["player_position"] in [[1, 2], [2, 2]], "Player position in log should be valid"
        assert logged_event["box_positions"] == box_positions, "Box positions in log should match current state"
if __name__ == "__main__":
    test_move_player()
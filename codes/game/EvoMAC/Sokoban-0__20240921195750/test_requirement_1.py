'''
This script tests the initial positions of the player, boxes, goals, and walls to ensure they are set correctly according to the task requirements.
'''
from main import player_position, box_positions, goal_positions, wall_positions
def test_initial_positions():
    assert player_position == [1, 1], "Player position should be [1, 1]"
    assert box_positions == [[3, 3], [4, 2]], "Box positions should be [[3, 3], [4, 2]]"
    assert goal_positions == [[5, 5], [6, 3]], "Goal positions should be [[5, 5], [6, 3]]"
    assert wall_positions == [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]], "Wall positions should be [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]]"
if __name__ == "__main__":
    test_initial_positions()
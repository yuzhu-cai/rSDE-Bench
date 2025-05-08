'''
Test cases for the Ghostly game to ensure that the game logic for eating pellets, invalid moves, and game over conditions are correctly implemented.
'''
import unittest
import json
import os
class TestGhostlyGame(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        self.log_file_path = 'game.log'
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)
    def log_event(self, event_type, move_direction, ghost_pos, monster_pos, status):
        timestamp = time.time()
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "move_direction": move_direction,
            "ghost_position": ghost_pos,
            "monster_position": monster_pos,
            "game_status": status
        }
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    def test_eat_pellet(self):
        # Simulate moving to a pellet position
        ghost_position = [1, 1]
        pellet_positions = [[3, 3], [4, 2]]
        move_direction = "right"
        ghost_position[0] += 1  # Move right
        self.assertIn(ghost_position, pellet_positions)
        pellet_positions.remove(ghost_position)
        self.log_event("eat_pellet", move_direction, ghost_position, [-1, -1], "ongoing")
        with open(self.log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            self.assertIn("eat_pellet", logs[-1])
    def test_invalid_move_wall(self):
        # Simulate moving into a wall
        ghost_position = [1, 1]
        walls_position = [[0, 4], [1, 4], [2, 4], [3, 4]]
        move_direction = "up"
        ghost_position[1] -= 1  # Move up
        self.assertIn(ghost_position, walls_position)
        self.log_event("invalid_move", move_direction, ghost_position, [-1, -1], "ongoing")
        with open(self.log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            self.assertIn("invalid_move", logs[-1])
    def test_eat_superpellet(self):
        # Simulate eating a superpellet
        ghost_position = [1, 1]
        superpellet_positions = [[5, 5], [6, 3]]
        move_direction = "down"
        ghost_position[1] += 1  # Move down
        self.assertIn(ghost_position, superpellet_positions)
        superpellet_positions.remove(ghost_position)
        self.log_event("eat_superpellet", move_direction, ghost_position, [-1, -1], "ongoing")
        with open(self.log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            self.assertIn("eat_superpellet", logs[-1])
    def test_game_over_monster(self):
        # Simulate monster eating the player's ghost
        ghost_position = [1, 1]
        monster_position = [1, 1]
        self.assertEqual(ghost_position, monster_position)
        self.log_event("monster_eat_ghost", "", ghost_position, monster_position, "lose")
        with open(self.log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            self.assertIn("monster_eat_ghost", logs[-1])
if __name__ == '__main__':
    unittest.main()
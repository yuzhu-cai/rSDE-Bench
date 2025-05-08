'''
Test cases for the Ghostly game functions to ensure proper handling of inputs and global variables.
'''
import unittest
import json
import time
from main import log_event, move_ghost, activate_monster, move_monster, check_victory, ghost_position, pellet_positions, superpellet_positions, other_ghost_positions, walls_position, monster_position, game_status
class TestGhostlyGame(unittest.TestCase):
    def setUp(self):
        # Reset global variables before each test
        global ghost_position, pellet_positions, superpellet_positions, other_ghost_positions, walls_position, monster_position, game_status
        ghost_position = [1, 1]
        pellet_positions = [[3, 3], [4, 2]]
        superpellet_positions = [[5, 5], [6, 3]]
        other_ghost_positions = [[0, 5], [3, 5]]
        walls_position = [[0, 4], [1, 4], [2, 4], [3, 4]]
        monster_position = [-1, -1]
        game_status = "ongoing"
    def test_move_ghost_valid_move(self):
        move_ghost("right")
        self.assertEqual(ghost_position, [2, 1])
        self.assertEqual(game_status, "ongoing")
    def test_move_ghost_invalid_move_wall(self):
        move_ghost("up")  # This should hit the wall
        self.assertEqual(ghost_position, [1, 1])  # Position should remain unchanged
        self.assertEqual(game_status, "ongoing")
    def test_move_ghost_eat_pellet(self):
        move_ghost("down")  # Move to [1, 2]
        move_ghost("down")  # Move to [1, 3]
        move_ghost("right")  # Move to [2, 3]
        move_ghost("right")  # Move to [3, 3] and eat pellet
        self.assertEqual(ghost_position, [3, 3])
        self.assertNotIn([3, 3], pellet_positions)  # Pellet should be removed
    def test_move_ghost_eat_superpellet(self):
        move_ghost("down")  # Move to [1, 2]
        move_ghost("down")  # Move to [1, 3]
        move_ghost("right")  # Move to [2, 3]
        move_ghost("right")  # Move to [3, 3] and eat pellet
        move_ghost("down")  # Move to [3, 4]
        move_ghost("down")  # Move to [4, 4]
        move_ghost("down")  # Move to [5, 4]
        move_ghost("down")  # Move to [6, 4]
        move_ghost("down")  # Move to [5, 5] and eat superpellet
        self.assertTrue(superpellet_active)
    def test_move_ghost_eat_other_ghost(self):
        global superpellet_active
        superpellet_active = True  # Activate superpellet
        move_ghost("up")  # Move to [1, 0]
        move_ghost("right")  # Move to [2, 0]
        move_ghost("down")  # Move to [2, 1]
        move_ghost("down")  # Move to [2, 2]
        move_ghost("down")  # Move to [2, 3]
        move_ghost("down")  # Move to [3, 3]
        move_ghost("right")  # Move to [4, 3]
        move_ghost("right")  # Move to [5, 3]
        move_ghost("right")  # Move to [6, 3] and eat other ghost
        self.assertNotIn([0, 5], other_ghost_positions)
    def test_activate_monster(self):
        activate_monster()
        self.assertEqual(monster_position, [1, 1])
    def test_move_monster(self):
        activate_monster()
        move_monster()
        self.assertEqual(monster_position, [1, 1])  # Monster should move towards the ghost
    def test_check_victory(self):
        global pellet_positions, other_ghost_positions
        pellet_positions = []
        other_ghost_positions = []
        check_victory()
        self.assertEqual(game_status, "win")
if __name__ == '__main__':
    unittest.main()
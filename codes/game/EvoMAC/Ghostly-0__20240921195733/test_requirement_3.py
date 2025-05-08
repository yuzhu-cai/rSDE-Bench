'''
Test the value initialization of game elements in the Ghostly game.
'''
import unittest
from main import ghost_position, pellet_positions, superpellet_positions, other_ghost_positions, walls_position
class TestGameInitialization(unittest.TestCase):
    def test_ghost_position_initialization(self):
        expected_position = [1, 1]
        self.assertEqual(ghost_position, expected_position, f"Expected ghost position {expected_position}, but got {ghost_position}")
    def test_pellet_positions_initialization(self):
        expected_pellets = [[3, 3], [4, 2]]
        self.assertEqual(pellet_positions, expected_pellets, f"Expected pellet positions {expected_pellets}, but got {pellet_positions}")
    def test_superpellet_positions_initialization(self):
        expected_superpellets = [[5, 5], [6, 3]]
        self.assertEqual(superpellet_positions, expected_superpellets, f"Expected superpellet positions {expected_superpellets}, but got {superpellet_positions}")
    def test_other_ghost_positions_initialization(self):
        expected_other_ghosts = [[0, 5], [3, 5]]
        self.assertEqual(other_ghost_positions, expected_other_ghosts, f"Expected other ghost positions {expected_other_ghosts}, but got {other_ghost_positions}")
    def test_walls_position_initialization(self):
        expected_walls = [[0, 4], [1, 4], [2, 4], [3, 4]]
        self.assertEqual(walls_position, expected_walls, f"Expected wall positions {expected_walls}, but got {walls_position}")
if __name__ == '__main__':
    unittest.main()
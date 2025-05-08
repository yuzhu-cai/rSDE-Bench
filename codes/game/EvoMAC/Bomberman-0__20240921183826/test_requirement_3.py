'''
Test the value initialization required by the task to ensure they are correctly achieved. 
Pay attention to the coordinates of the player and enemies, ensuring they are initialized at the correct positions on the grid.
'''
import unittest
import random
# Constants
GRID_SIZE = 13
PLAYER_START_POS = (0, 0)
INITIAL_ENEMY_HEALTH = 10
class TestBombermanInitialization(unittest.TestCase):
    def setUp(self):
        # Initialize player and enemies
        self.player_pos = PLAYER_START_POS
        self.enemies_pos = [(random.randint(1, GRID_SIZE-1), random.randint(1, GRID_SIZE-1)) for _ in range(2)]
        self.enemies_health = [INITIAL_ENEMY_HEALTH, INITIAL_ENEMY_HEALTH]
    def test_player_initial_position(self):
        """Test if the player starts at the correct position (0, 0)."""
        self.assertEqual(self.player_pos, PLAYER_START_POS, "Player should start at position (0, 0)")
    def test_enemy_initial_positions(self):
        """Test if enemies are initialized at random positions and not at the player's position."""
        for pos in self.enemies_pos:
            self.assertNotEqual(pos, self.player_pos, "Enemy should not start at the player's position")
            self.assertTrue(1 <= pos[0] < GRID_SIZE and 1 <= pos[1] < GRID_SIZE, 
                            "Enemy positions should be within the grid bounds (1 to 12)")
    def test_enemy_health_initialization(self):
        """Test if enemies start with the correct health value."""
        for health in self.enemies_health:
            self.assertEqual(health, INITIAL_ENEMY_HEALTH, "Each enemy should start with health of 10")
if __name__ == '__main__':
    unittest.main()
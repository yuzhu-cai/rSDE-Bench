'''
Test the function inputs and the global variables imported in each function. Ensure that the input values and global variables used in the functions are valid and involved when the function is called.
'''
import unittest
import time
import json
from main import (GRID_SIZE, CELL_SIZE, PLAYER_START_POS, ENEMY_START_POS, 
                  INITIAL_PLAYER_HEALTH, INITIAL_ENEMY_HEALTH, INITIAL_SCORE, 
                  OBSTACLES, update_log, move_enemies_towards_player, 
                  explode_bomb, bomb_timer)
class TestBombermanGame(unittest.TestCase):
    def setUp(self):
        # Reset the game state for each test
        self.player_pos = PLAYER_START_POS
        self.enemies_pos = ENEMY_START_POS
        self.player_health = INITIAL_PLAYER_HEALTH
        self.enemies_health = [INITIAL_ENEMY_HEALTH, INITIAL_ENEMY_HEALTH]
        self.score = INITIAL_SCORE
        self.bombs = []
        self.explosions = []
    def test_initial_conditions(self):
        self.assertEqual(self.player_pos, PLAYER_START_POS)
        self.assertEqual(len(self.enemies_pos), 2)
        self.assertTrue(all(health == INITIAL_ENEMY_HEALTH for health in self.enemies_health))
        self.assertEqual(self.score, INITIAL_SCORE)
    def test_update_log_format(self):
        event_type = "MOVE_LEFT"
        update_log(event_type)
        with open("game.log", "r") as log_file:
            log_entries = log_file.readlines()
            last_entry = json.loads(log_entries[-1])
            self.assertEqual(last_entry["EVENT_TYPE"], event_type)
            self.assertEqual(len(last_entry["game_board_state"]), GRID_SIZE * GRID_SIZE)
            self.assertIn("player", last_entry)
            self.assertIn("enemies", last_entry)
    def test_move_enemies_towards_player(self):
        self.enemies_pos = [(1, 1), (3, 3)]
        move_enemies_towards_player()
        self.assertIn(self.enemies_pos[0], [(0, 1), (1, 2)])  # Enemy should move towards player
        self.assertIn(self.enemies_pos[1], [(2, 3), (3, 2)])  # Enemy should move towards player
    def test_explode_bomb(self):
        self.bombs.append((1, 1))
        explode_bomb((1, 1))
        self.assertIn((1, 1), self.explosions)  # Bomb position should be in explosions
        self.assertEqual(self.player_health, INITIAL_PLAYER_HEALTH - 10)  # Player should be injured
    def test_bomb_timer(self):
        bomb_pos = (1, 1)
        bomb_timer(bomb_pos)
        time.sleep(2)  # Wait for the bomb to explode
        self.assertIn(bomb_pos, self.explosions)  # Bomb position should be in explosions after delay
if __name__ == '__main__':
    unittest.main()
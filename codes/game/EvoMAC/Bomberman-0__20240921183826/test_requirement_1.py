'''
Test the logging mechanism of the Bomberman game to ensure that the log happens immediately after the action is taken, recording the most recent state. Verify the logging order, ensuring basic operations are recorded first, followed by subsequent events. Check the data format, keys, and values for accuracy, paying attention to the nested data types and ensuring each element is correct.
'''
import unittest
import json
import time
class TestBombermanLogging(unittest.TestCase):
    def setUp(self):
        # Initialize game state
        self.player_health = 100
        self.enemies_health = [10, 10]
        self.score = 0
        self.bombs = []
        self.explosions = []
        self.log_entries = []
    def log_event(self, event_type):
        game_board_state = [0] * (13 * 13)
        game_board_state[0] = 1  # Player position
        for i, health in enumerate(self.enemies_health):
            if health > 0:
                game_board_state[1 + i] = 2  # Enemy positions
        for bomb in self.bombs:
            game_board_state[bomb[1] * 13 + bomb[0]] = 3  # Bomb positions
        for explosion in self.explosions:
            game_board_state[explosion[1] * 13 + explosion[0]] = 4  # Explosion positions
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "game_board_state": game_board_state,
            "player": {"health": self.player_health, "score": self.score},
            "enemies": [{"health": health} for health in self.enemies_health]
        }
        self.log_entries.append(log_entry)
    def test_move_left_logging(self):
        self.log_event("MOVE_LEFT")
        self.assertEqual(len(self.log_entries), 1)
        self.assertEqual(self.log_entries[0]["EVENT_TYPE"], "MOVE_LEFT")
        self.assertEqual(self.log_entries[0]["player"]["health"], self.player_health)
        self.assertEqual(self.log_entries[0]["player"]["score"], self.score)
    def test_place_bomb_logging(self):
        self.bombs.append((0, 0))
        self.log_event("PLACE_BOMB")
        self.assertEqual(len(self.log_entries), 2)
        self.assertEqual(self.log_entries[1]["EVENT_TYPE"], "PLACE_BOMB")
        self.assertIn((0, 0), [bomb for bomb in self.bombs])
    def test_explosion_logging(self):
        self.bombs.append((0, 0))
        self.log_event("BOOM")
        self.assertEqual(len(self.log_entries), 3)
        self.assertEqual(self.log_entries[2]["EVENT_TYPE"], "BOOM")
    def test_injured_logging(self):
        self.player_health -= 10
        self.log_event("INJURED")
        self.assertEqual(len(self.log_entries), 4)
        self.assertEqual(self.log_entries[3]["EVENT_TYPE"], "INJURED")
        self.assertEqual(self.log_entries[3]["player"]["health"], self.player_health)
    def test_victory_logging(self):
        self.enemies_health = [0, 0]
        self.log_event("VICTORY")
        self.assertEqual(len(self.log_entries), 5)
        self.assertEqual(self.log_entries[4]["EVENT_TYPE"], "VICTORY")
if __name__ == '__main__':
    unittest.main()
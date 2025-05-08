'''
Test the logging mechanism for the special triggered conditions, such as when Mario touches the mushroom, hits the block, or reaches the flagpole.
'''
import unittest
import json
import time
class TestSuperMarioGame(unittest.TestCase):
    def setUp(self):
        # This method will run before each test
        self.log_entries = []
        self.score = 0
        self.mario_pos = [50, 350]  # Initial position of Mario
        self.block_pos = [50, 300]  # Position of the block
        self.mushroom_pos = [None, None]
        self.enemy_pos = [200, 350]  # Position of the enemy
    def log_event(self, event_type):
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": self.mario_pos,
            "enemy_position": self.enemy_pos,
            "block_position": self.block_pos,
            "mushroom_position": self.mushroom_pos,
            "score": self.score
        }
        self.log_entries.append(log_entry)
    def test_hit_block_logging(self):
        # Simulate hitting the block
        self.mario_pos[0] = 50  # Mario is directly under the block
        self.score += 100  # Score increases by 100
        self.log_event("HIT_BLOCK")
        # Check the last log entry
        last_entry = self.log_entries[-1]
        self.assertEqual(last_entry["EVENT_TYPE"], "HIT_BLOCK")
        self.assertEqual(last_entry["score"], 100)
        self.assertEqual(last_entry["mario_position"], self.mario_pos)
        self.assertEqual(last_entry["block_position"], self.block_pos)
        self.assertEqual(last_entry["mushroom_position"], [None, None])
    def test_touch_mushroom_logging(self):
        # Simulate the mushroom appearing and Mario touching it
        self.mushroom_pos = [50, 250]  # Position of the mushroom
        self.score += 1000  # Score increases by 1000
        self.log_event("TOUCH_MUSHROOM")
        # Check the last log entry
        last_entry = self.log_entries[-1]
        self.assertEqual(last_entry["EVENT_TYPE"], "TOUCH_MUSHROOM")
        self.assertEqual(last_entry["score"], 1000)
        self.assertEqual(last_entry["mario_position"], self.mario_pos)
        self.assertEqual(last_entry["block_position"], self.block_pos)
        self.assertEqual(last_entry["mushroom_position"], self.mushroom_pos)
    def test_reach_flag_logging(self):
        # Simulate reaching the flag
        self.mario_pos[0] = 750  # Mario reaches the flag
        self.score += 10000  # Score increases by 10000
        self.log_event("REACH_FLAG")
        # Check the last log entry
        last_entry = self.log_entries[-1]
        self.assertEqual(last_entry["EVENT_TYPE"], "REACH_FLAG")
        self.assertEqual(last_entry["score"], 10000)
        self.assertEqual(last_entry["mario_position"], self.mario_pos)
        self.assertEqual(last_entry["block_position"], self.block_pos)
        self.assertEqual(last_entry["mushroom_position"], self.mushroom_pos)
if __name__ == '__main__':
    unittest.main()
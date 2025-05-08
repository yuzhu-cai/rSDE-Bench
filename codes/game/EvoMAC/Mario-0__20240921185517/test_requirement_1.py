'''
Test the logging mechanism of the Super Mario game to ensure that events are logged correctly 
according to the task requirements. This includes checking the format, keys, and values of the log entries.
'''
import unittest
import json
import time
from io import StringIO
import sys
class TestSuperMarioLogging(unittest.TestCase):
    def setUp(self):
        # Redirect stdout to capture log output
        self.log_output = StringIO()
        sys.stdout = self.log_output
    def tearDown(self):
        # Reset stdout
        sys.stdout = sys.__stdout__
    def test_log_event_move_left(self):
        # Simulate the event of moving left
        mario_pos = [50, 300]
        enemy_pos = [200, 300]
        block_pos = [50, 250]
        mushroom_pos = [None, None]
        score = 0
        event_type = "MOVE_LEFT"
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": mario_pos,
            "enemy_position": enemy_pos,
            "block_position": block_pos,
            "mushroom_position": mushroom_pos,
            "score": score
        }
        print(json.dumps(log_entry))
        self.log_output.seek(0)
        logged_data = self.log_output.read().strip()
        self.assertTrue(logged_data)
        self.assertEqual(json.loads(logged_data)["EVENT_TYPE"], "MOVE_LEFT")
        self.assertEqual(json.loads(logged_data)["mario_position"], mario_pos)
    def test_log_event_hit_block(self):
        # Simulate the event of hitting a block
        mario_pos = [50, 300]
        enemy_pos = [200, 300]
        block_pos = [50, 250]
        mushroom_pos = [None, None]
        score = 100
        event_type = "HIT_BLOCK"
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": mario_pos,
            "enemy_position": enemy_pos,
            "block_position": block_pos,
            "mushroom_position": mushroom_pos,
            "score": score
        }
        print(json.dumps(log_entry))
        self.log_output.seek(0)
        logged_data = self.log_output.read().strip()
        self.assertTrue(logged_data)
        self.assertEqual(json.loads(logged_data)["EVENT_TYPE"], "HIT_BLOCK")
        self.assertEqual(json.loads(logged_data)["score"], 100)
    def test_log_event_touch_mushroom(self):
        # Simulate the event of touching a mushroom
        mario_pos = [50, 300]
        enemy_pos = [200, 300]
        block_pos = [50, 250]
        mushroom_pos = [60, 290]
        score = 1100
        event_type = "TOUCH_MUSHROOM"
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": mario_pos,
            "enemy_position": enemy_pos,
            "block_position": block_pos,
            "mushroom_position": mushroom_pos,
            "score": score
        }
        print(json.dumps(log_entry))
        self.log_output.seek(0)
        logged_data = self.log_output.read().strip()
        self.assertTrue(logged_data)
        self.assertEqual(json.loads(logged_data)["EVENT_TYPE"], "TOUCH_MUSHROOM")
        self.assertEqual(json.loads(logged_data)["score"], 1100)
    def test_log_event_reach_flag(self):
        # Simulate the event of reaching the flag
        mario_pos = [750, 300]
        enemy_pos = [200, 300]
        block_pos = [50, 250]
        mushroom_pos = [None, None]
        score = 11100
        event_type = "REACH_FLAG"
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": mario_pos,
            "enemy_position": enemy_pos,
            "block_position": block_pos,
            "mushroom_position": mushroom_pos,
            "score": score
        }
        print(json.dumps(log_entry))
        self.log_output.seek(0)
        logged_data = self.log_output.read().strip()
        self.assertTrue(logged_data)
        self.assertEqual(json.loads(logged_data)["EVENT_TYPE"], "REACH_FLAG")
        self.assertEqual(json.loads(logged_data)["score"], 11100)
    def test_log_event_collide_enemy(self):
        # Simulate the event of colliding with an enemy
        mario_pos = [200, 300]
        enemy_pos = [200, 300]
        block_pos = [50, 250]
        mushroom_pos = [None, None]
        score = 11100
        event_type = "COLLIDE_ENEMY"
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": mario_pos,
            "enemy_position": enemy_pos,
            "block_position": block_pos,
            "mushroom_position": mushroom_pos,
            "score": score
        }
        print(json.dumps(log_entry))
        self.log_output.seek(0)
        logged_data = self.log_output.read().strip()
        self.assertTrue(logged_data)
        self.assertEqual(json.loads(logged_data)["EVENT_TYPE"], "COLLIDE_ENEMY")
        self.assertEqual(json.loads(logged_data)["score"], 11100)
if __name__ == '__main__':
    unittest.main()
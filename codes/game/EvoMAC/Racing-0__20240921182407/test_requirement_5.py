'''
Test the collision events with obstacles in the racing game.
'''
import unittest
import json
import time
import os
class TestRacingGame(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        self.log_file = 'game.log'
        with open(self.log_file, 'w') as f:
            f.write('')
    def log_content(self):
        with open(self.log_file, 'r') as f:
            return f.readlines()
    def test_collide_fatal_obstacle(self):
        # Simulate a fatal collision
        with open(self.log_file, 'a') as f:
            log_entry = {
                "timestamp": time.time(),
                "EVENT_TYPE": "collide_fatal_obstacles",
                "car_speed": 0,
                "car_position": [2, 100]
            }
            f.write(json.dumps(log_entry) + '\n')
        log_entries = self.log_content()
        self.assertEqual(len(log_entries), 1)
        log_entry = json.loads(log_entries[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "collide_fatal_obstacles")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [2, 100])
    def test_collide_slow_down_obstacle(self):
        # Simulate a slow down collision
        with open(self.log_file, 'a') as f:
            log_entry = {
                "timestamp": time.time(),
                "EVENT_TYPE": "collide_slow_down_obstacles",
                "car_speed": 3,
                "car_position": [2, 150]
            }
            f.write(json.dumps(log_entry) + '\n')
        log_entries = self.log_content()
        self.assertEqual(len(log_entries), 1)
        log_entry = json.loads(log_entries[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "collide_slow_down_obstacles")
        self.assertEqual(log_entry["car_speed"], 3)
        self.assertEqual(log_entry["car_position"], [2, 150])
    def tearDown(self):
        # Clean up log file after each test
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
if __name__ == '__main__':
    unittest.main()
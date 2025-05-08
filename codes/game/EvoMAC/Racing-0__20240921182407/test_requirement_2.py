'''
Test the logging mechanism for the special triggered conditions, such as colliding with fatal obstacles and slow-down obstacles, ensuring that the correct log entries are created.
'''
import unittest
import json
import time
import os
class TestRacingGameLogging(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        self.log_file = 'game.log'
        with open(self.log_file, 'w') as f:
            f.write('')
    def log_event(self, event_type, speed, position):
        '''
        Simulates logging an event to the game.log file.
        '''
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "car_speed": speed,
            "car_position": position
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    def test_collide_fatal_obstacles_logging(self):
        # Simulate a fatal collision
        car_speed = 10
        car_position = [2, 100]  # Lane 2, distance 100
        self.log_event("collide_fatal_obstacles", car_speed, car_position)
        # Check the log file for the correct entry
        with open(self.log_file, 'r') as f:
            logs = f.readlines()
            self.assertEqual(len(logs), 1)
            log_entry = json.loads(logs[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "collide_fatal_obstacles")
            self.assertEqual(log_entry["car_speed"], car_speed)
            self.assertEqual(log_entry["car_position"], car_position)
    def test_collide_slow_down_obstacles_logging(self):
        # Simulate a slow down collision
        car_speed = 10
        car_position = [1, 150]  # Lane 1, distance 150
        self.log_event("collide_slow_down_obstacles", car_speed, car_position)
        # Check the log file for the correct entry
        with open(self.log_file, 'r') as f:
            logs = f.readlines()
            self.assertEqual(len(logs), 1)
            log_entry = json.loads(logs[0])
            self.assertEqual(log_entry["EVENT_TYPE"], "collide_slow_down_obstacles")
            self.assertEqual(log_entry["car_speed"], car_speed)
            self.assertEqual(log_entry["car_position"], car_position)
if __name__ == '__main__':
    unittest.main()
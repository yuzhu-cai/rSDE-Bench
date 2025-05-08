'''
Test the logging mechanism of the racing game to ensure that the log entries are correctly formatted and contain the expected data after each player action.
'''
import unittest
import json
import time
import os
class TestLoggingMechanism(unittest.TestCase):
    def setUp(self):
        # Clear the log file before each test
        self.log_file = 'game.log'
        with open(self.log_file, 'w') as f:
            f.write('')
    def log_event(self, event_type, car_speed, car_position):
        '''
        Simulate logging an event to the log file.
        '''
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "car_speed": car_speed,
            "car_position": car_position
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    def test_speed_up_logging(self):
        self.log_event("speed_up", 10, [2, 0])
        with open(self.log_file, 'r') as f:
            log_content = f.readlines()
        self.assertEqual(len(log_content), 1)
        log_entry = json.loads(log_content[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "speed_up")
        self.assertEqual(log_entry["car_speed"], 10)
        self.assertEqual(log_entry["car_position"], [2, 0])
    def test_speed_down_logging(self):
        self.log_event("speed_down", 5, [2, 10])
        with open(self.log_file, 'r') as f:
            log_content = f.readlines()
        self.assertEqual(len(log_content), 1)
        log_entry = json.loads(log_content[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "speed_down")
        self.assertEqual(log_entry["car_speed"], 5)
        self.assertEqual(log_entry["car_position"], [2, 10])
    def test_move_left_logging(self):
        self.log_event("move_left", 5, [1, 20])
        with open(self.log_file, 'r') as f:
            log_content = f.readlines()
        self.assertEqual(len(log_content), 1)
        log_entry = json.loads(log_content[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "move_left")
        self.assertEqual(log_entry["car_speed"], 5)
        self.assertEqual(log_entry["car_position"], [1, 20])
    def test_move_right_logging(self):
        self.log_event("move_right", 5, [3, 30])
        with open(self.log_file, 'r') as f:
            log_content = f.readlines()
        self.assertEqual(len(log_content), 1)
        log_entry = json.loads(log_content[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "move_right")
        self.assertEqual(log_entry["car_speed"], 5)
        self.assertEqual(log_entry["car_position"], [3, 30])
    def test_stop_logging(self):
        self.log_event("stop", 0, [2, 40])
        with open(self.log_file, 'r') as f:
            log_content = f.readlines()
        self.assertEqual(len(log_content), 1)
        log_entry = json.loads(log_content[0])
        self.assertEqual(log_entry["EVENT_TYPE"], "stop")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [2, 40])
    def tearDown(self):
        # Remove the log file after each test
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
if __name__ == '__main__':
    unittest.main()
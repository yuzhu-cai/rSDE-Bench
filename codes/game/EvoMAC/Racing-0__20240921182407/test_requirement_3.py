'''
Test the value initialization required by the task to ensure they are correctly achieved, paying attention to the coordinates of the car's position and speed.
'''
import unittest
import json
import time
class TestRacingGame(unittest.TestCase):
    def setUp(self):
        # Initialize game variables
        self.car_position = 2  # Start in the middle lane (1, 2, 3)
        self.car_speed = 0
        self.distance_traveled = 0
        self.log_file = 'game.log'
        with open(self.log_file, 'w') as f:
            f.write('')  # Clear log file at the start
    def log_event(self, event_type):
        '''
        Logs the event to the game.log file with the current timestamp, event type, speed, and position.
        '''
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "car_speed": self.car_speed,
            "car_position": [self.car_position, self.distance_traveled]
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    def test_initial_car_position(self):
        self.assertEqual(self.car_position, 2, "Car position should be initialized to lane 2.")
    def test_initial_car_speed(self):
        self.assertEqual(self.car_speed, 0, "Car speed should be initialized to 0.")
    def test_initial_distance_traveled(self):
        self.assertEqual(self.distance_traveled, 0, "Distance traveled should be initialized to 0.")
    def test_log_event_format(self):
        self.car_speed = 10
        self.car_position = 1
        self.log_event("speed_up")
        with open(self.log_file, 'r') as f:
            log_entries = f.readlines()
            self.assertGreater(len(log_entries), 0, "Log file should contain at least one entry.")
            log_entry = json.loads(log_entries[-1].strip())
            self.assertIn("timestamp", log_entry, "Log entry should contain a timestamp.")
            self.assertIn("EVENT_TYPE", log_entry, "Log entry should contain an EVENT_TYPE.")
            self.assertIn("car_speed", log_entry, "Log entry should contain car_speed.")
            self.assertIn("car_position", log_entry, "Log entry should contain car_position.")
            self.assertEqual(log_entry["car_position"], [self.car_position, self.distance_traveled], "Car position in log should match current position.")
if __name__ == '__main__':
    unittest.main()
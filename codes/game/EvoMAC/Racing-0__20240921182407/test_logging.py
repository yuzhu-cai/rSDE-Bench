'''
This script implements unit tests for the logging mechanism of the racing game.
'''
import unittest
import json
import time
from unittest.mock import patch, mock_open
from main import log_event
class TestLoggingMechanism(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_log_speed_up(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 10
        car_position = 2
        distance_traveled = 50
        log_event("speed_up")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "speed_up")
        self.assertEqual(log_entry["car_speed"], 10)
        self.assertEqual(log_entry["car_position"], [2, 50])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_speed_down(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 5
        car_position = 1
        distance_traveled = 100
        log_event("speed_down")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "speed_down")
        self.assertEqual(log_entry["car_speed"], 5)
        self.assertEqual(log_entry["car_position"], [1, 100])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_move_left(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 0
        car_position = 2
        distance_traveled = 150
        log_event("move_left")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "move_left")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [2, 150])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_move_right(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 0
        car_position = 1
        distance_traveled = 200
        log_event("move_right")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "move_right")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [1, 200])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_stop(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 0
        car_position = 3
        distance_traveled = 250
        log_event("stop")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "stop")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [3, 250])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_collide_fatal_obstacles(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 0
        car_position = 2
        distance_traveled = 300
        log_event("collide_fatal_obstacles")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "collide_fatal_obstacles")
        self.assertEqual(log_entry["car_speed"], 0)
        self.assertEqual(log_entry["car_position"], [2, 300])
    @patch('builtins.open', new_callable=mock_open)
    def test_log_collide_slow_down_obstacles(self, mock_file):
        global car_speed, car_position, distance_traveled
        car_speed = 5
        car_position = 1
        distance_traveled = 350
        log_event("collide_slow_down_obstacles")
        mock_file().write.assert_called_once()
        log_entry = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(log_entry["EVENT_TYPE"], "collide_slow_down_obstacles")
        self.assertEqual(log_entry["car_speed"], 5)
        self.assertEqual(log_entry["car_position"], [1, 350])
if __name__ == '__main__':
    unittest.main()
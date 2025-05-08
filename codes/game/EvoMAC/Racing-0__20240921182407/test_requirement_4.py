'''
Test cases for the racing game implemented in main.py. The tests focus on validating function inputs and global variables used in the functions.
'''
import unittest
import json
import time
from main import log_event, create_obstacle, move_obstacles
class TestRacingGame(unittest.TestCase):
    def setUp(self):
        # Reset global variables before each test
        global car_position, car_speed, distance_traveled, obstacles, game_over
        car_position = 2
        car_speed = 0
        distance_traveled = 0
        obstacles = []
        game_over = False
    def test_log_event(self):
        global car_position, car_speed
        car_speed = 10
        log_event("speed_up")
        with open('game.log', 'r') as f:
            logs = f.readlines()
        self.assertGreater(len(logs), 0, "Log file should have at least one entry.")
        log_entry = json.loads(logs[-1])
        self.assertEqual(log_entry["EVENT_TYPE"], "speed_up")
        self.assertEqual(log_entry["car_speed"], car_speed)
        self.assertEqual(log_entry["car_position"], [car_position, distance_traveled])
    def test_create_obstacle(self):
        obstacle = create_obstacle()
        self.assertIn('lane', obstacle)
        self.assertIn('y', obstacle)
        self.assertIn('type', obstacle)
        self.assertIn(obstacle['lane'], [1, 2, 3])
        self.assertEqual(obstacle['y'], -50)
        self.assertIn(obstacle['type'], ['slow', 'fatal'])
    def test_move_obstacles(self):
        global obstacles, car_position, car_speed, game_over
        obstacles.append({'lane': 2, 'y': 500, 'type': 'slow'})
        car_speed = 5
        move_obstacles()
        # Check if the obstacle moves down
        self.assertEqual(obstacles[0]['y'], 505)
        # Check collision with slow obstacle
        obstacles[0]['y'] = 500  # Set position for collision
        move_obstacles()
        self.assertEqual(car_speed, 3)  # Speed should decrease by 2
        self.assertFalse(game_over)
        # Test fatal collision
        obstacles[0]['type'] = 'fatal'
        obstacles[0]['y'] = 500  # Set position for collision
        move_obstacles()
        self.assertTrue(game_over)
if __name__ == '__main__':
    unittest.main()
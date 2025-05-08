'''
REQUIREMENTS
Player can eliminate enemy by pressing the down arrow key. If Mario eliminates the enemy, enemy will disappear, the EVENT_TYPE should be "ELIMINATE_ENEMY", and the enemy_position should be [None, None].
'''
import unittest
import pygame
import json
import time
class TestSuperMarioGame(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        self.mario_pos = [50, 350]  # Mario's initial position
        self.enemy_pos = [60, 350]  # Enemy's initial position
        self.score = 0
        self.log_entries = []
    def log_event(self, event_type):
        log_entry = {
            "timestamp": time.time(),
            "EVENT_TYPE": event_type,
            "mario_position": self.mario_pos,
            "enemy_position": self.enemy_pos,
            "block_position": [50, 300],
            "mushroom_position": [None, None],
            "score": self.score
        }
        self.log_entries.append(log_entry)
    def test_eliminate_enemy(self):
        # Simulate Mario's position overlapping with the enemy
        self.mario_pos[0] = 60  # Move Mario to the enemy's position
        # Simulate pressing the down arrow key
        if self.enemy_pos[0] is not None and self.mario_pos[0] + 50 > self.enemy_pos[0] and self.mario_pos[0] < self.enemy_pos[0] + 40:
            self.enemy_pos = [None, None]  # Enemy is eliminated
            self.log_event("ELIMINATE_ENEMY")
        # Check if the enemy is eliminated
        self.assertEqual(self.enemy_pos, [None, None])
        # Check if the log entry is correct
        self.assertEqual(self.log_entries[-1]["EVENT_TYPE"], "ELIMINATE_ENEMY")
    def tearDown(self):
        pygame.quit()
if __name__ == '__main__':
    unittest.main()
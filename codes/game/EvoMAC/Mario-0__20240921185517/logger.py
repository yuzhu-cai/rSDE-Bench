'''
This module contains the logging functionality for the Super Mario game.
'''
import json
import time
log_file = open('game.log', 'w')
def log_event(event_type, score, mario_pos, enemy_pos, block_pos, mushroom_pos):
    log_entry = {
        "timestamp": time.time(),
        "EVENT_TYPE": event_type,
        "mario_position": mario_pos,
        "enemy_position": enemy_pos,
        "block_position": block_pos,
        "mushroom_position": mushroom_pos,
        "score": score
    }
    log_file.write(json.dumps(log_entry) + '\n')
    log_file.flush()
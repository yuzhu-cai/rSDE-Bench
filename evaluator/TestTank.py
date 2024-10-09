import os
import cv2
import time
import json
import math
import subprocess

import pyautogui as pg

from collections import deque
import sys
sys.path.append(os.path.dirname(__file__))
from utils import *
from checker import Checker

class TestTank():

    def __init__(self, checker, py, time=3):
        if not os.path.exists('test'):
            os.makedirs('test')

        self.checker = checker
        self.time = time
        self.py = py

        self.process = None
        self.rect = None
        self.width = None
        self.height = None
        self.clicks = None

        self.obstracal_pos = None
        self.enemies_pos = None

        self.event = ["INIT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "FIRE", "INJURED"]
        self.direction = {
            "(0, 1)": 'down',
            "(1, 0)": 'right',
            '(0, -1)': 'up',
            '(-1, 0)': 'left'
        }
        self.move = {
            "right": 'MOVE_RIGHT',
            "left": 'MOVE_LEFT',
            'down': 'MOVE_DOWN',
            'up': 'MOVE_UP'
        }
        self.succ = 1
        self.total_test = 8


    def tear_down(self):
        self.process.terminate() 

    def test_set_up(self):
        print("=======================Test Set Up=======================")
        try:
            self.process = subprocess.Popen(['python', f'{self.py}'])
        except:
            return 0
        
        time.sleep(self.time)

        rect = get_window_rect(self.process.pid)
        self.rect = rect

        self.clicks = [
            (int(0.5*(rect[0]+rect[2])), int(0.5*(rect[1]+rect[3]))),
        ]
        if rect == -1:
            print("FAIL")
            return 0
        
        print("SUCCESS")
        return 1

    def test_init(self):
        print("=======================Test init=======================")
        if not os.path.exists('game.log'):
            print('FAIL')
            return 0
        
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            print('FAIL')
            return 0
        
        log_entry = json.loads(lines[0].strip())
        event = log_entry['EVENT_TYPE']
        player = log_entry['game_state']['player']
        enemies = log_entry['game_state']['enemies']
        _enemy_pos = [tuple(enemy['position']) for enemy in enemies]
        self.enemies_pos = _enemy_pos
        # self.obstracal_pos = [tuple(item) for item in log_entry['obstacle_position']]
        self.obstracal_pos = [tuple(item) for item in log_entry['game_state']['obstacle_position']]
        
        if event != 'INIT':
            print('FAIL')
            return 0

        # player
        if player['score'] != 0:
            print('FAIL')
            return 0
        if player['position'] != [0, 0]:
            print('FAIL')
            return 0
        if player['health'] != 200:
            print('FAIL')
            return 0
        
        # enemies
        if len(enemies) != 2:
            print('FAIL')
            return 0
        
        # postion check
        for enemy in enemies:
            if enemy['health'] != 200:
                print('FAIL')
                return 0
        player_pos = tuple(player['position'])
        for enemy_pos in _enemy_pos:
            if player_pos[0] == enemy_pos[0] or player_pos[1] == enemy_pos[1]:
                print('FAIL')
                return 0
        if _enemy_pos[0][0] == _enemy_pos[1][0] or _enemy_pos[0][1] == _enemy_pos[1][1]:
            print('FAIL')
            return 0    
        
        # obstracal check
        if len(self.obstracal_pos) < 1:
            print('FAIL')
            return 0

        print('SUCCESS')
        return 1
    
    def test_move(self):

        print("=======================Test move=======================")
        pg.press('right',presses=1,interval=0)
        pg.press('down',presses=1,interval=0)
        pg.press('left',presses=1,interval=0)
        pg.press('up',presses=1,interval=0)
        time.sleep(self.time)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        exp_event = ['INIT', 'MOVE_RIGHT', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_UP']
        player_pos = [0,0]
                
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            if event != exp_event[idx]:
                print('FAIL')
                return 0
            
            player_pos_ = log_entry['game_state']['player']['position']
            new_pos = player_pos.copy()  
            if event == 'MOVE_RIGHT':  
                new_pos[0] = min(player_pos[0] + 1, 19)
            elif event == 'MOVE_DOWN':  
                new_pos[1] = min(player_pos[1] + 1, 19) 
            elif event == 'MOVE_LEFT':  
                new_pos[0] = max(player_pos[0] - 1, 0)
            elif event == 'MOVE_UP':  
                new_pos[1] = max(player_pos[1] - 1, 0)

            if new_pos in self.obstracal_pos:
                new_pos = player_pos

            if new_pos != player_pos_:
                print('FAIL')
                return 0
            
            player_pos = new_pos
            
        print('SUCCESS')
        return 1

    def bfs_shortest_path(self, start, goal, grid):  
        if start == goal:  
            return []  
        
        queue = deque([(start, [])])  
        visited = set()  
        visited.add(start)  

        while queue:  
            current_position, path = queue.popleft()  
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  
                next_position = (current_position[0] + direction[0], current_position[1] + direction[1])  
                if next_position == goal:  
                    return path + [next_position]  
 
                if (0 <= next_position[0] < len(grid) and  
                    0 <= next_position[1] < len(grid[0]) and  
                    grid[next_position[0]][next_position[1]] == 0 and 
                    next_position not in visited):  
                    
                    visited.add(next_position)  
                    queue.append((next_position, path + [next_position]))  

        return None  

    def move_towards_nearest_enemy(self, player_pos, enemies, grid):  
        nearest_enemy = None  
        min_distance = float('inf')  

        for enemy in enemies:  
            distance = abs(player_pos[0] - enemy[0]) + abs(player_pos[1] - enemy[1]) 
            if distance < min_distance:  
                min_distance = distance  
                nearest_enemy = enemy

        if nearest_enemy is None:  
            return [player_pos] 
        
        path = self.bfs_shortest_path(player_pos, nearest_enemy, grid)  

        if path:    
            return path  
        else:  
            return [player_pos]

    def test_fire(self):
        print("=======================Test fire=======================")
        self.tear_down()
        if os.path.exists('game.log'):
            os.remove('game.log')
        time.sleep(self.time)
        self.process = subprocess.Popen(['python', f'{self.py}'])
        time.sleep(self.time)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            print('FAIL')
            return 0
        
        log_entry = json.loads(lines[0].strip())
        # self.obstracal_pos = [tuple(item) for item in log_entry['obstacle_position']]
        self.obstracal_pos = [tuple(item) for item in log_entry['game_state']['obstacle_position']]
        self.enemies_pos = [tuple(enemy['position']) for enemy in log_entry['game_state']['enemies']]

        grid = [[0] * 20 for _ in range(20)]

        for obstracal in self.obstracal_pos:
            grid[obstracal[0]][obstracal[1]] = 1

        move_path  = self.move_towards_nearest_enemy((0,0), self.enemies_pos, grid)  
        
        directions = [move_path[0]]
        for i in range(len(move_path)-2):
            directions.append((move_path[i+1][0]-move_path[i][0], move_path[i+1][1]-move_path[i][1]))

        for direction in directions:
            press = self.direction[str(direction)]
            pg.press(press,presses=1,interval=0)
        pg.press('enter',presses=4,interval=1)
        press = self.direction[str(directions[-1])]
        pg.press(press,presses=1,interval=0)
        time.sleep(self.time)


        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        previous_enemies = None
        is_fire = False
        for line in lines:
            log_entry = json.loads(line.strip())
            event = log_entry['EVENT_TYPE']
            current_enemies = log_entry['game_state']['enemies']

            if event != 'FIRE':
                continue
            else:
                is_fire = True
                if previous_enemies is not None:
                    diff_1 = previous_enemies[0]['health'] - current_enemies[0]['health']
                    diff_2 = previous_enemies[1]['health'] - current_enemies[1]['health']
                    if previous_enemies[0]['health'] == 200 and previous_enemies[1]['health'] == 200:
                        if diff_1 != 100 and diff_2 != 100:
                            print('FAIL')
                            return 0
                    if previous_enemies[0]['health'] == 100 or previous_enemies[1]['health'] == 100:
                        if diff_1 != 100 and diff_2 != 100:
                            print('FAIL')
                            return 0
                    if previous_enemies[0]['health'] == 0 or previous_enemies[1]['health'] == 0:
                        if diff_1 != 0 and diff_2 != 0:
                            print('FAIL')
                            return 0
            
            previous_enemies = current_enemies

        if is_fire:
            print('SUCCESS')
            return 1
        else:
            print('FAIL')
            return 0


    def test_score(self):
        print("=======================Test score=======================")
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        exp_score = 0
        for line in lines:
            log_entry = json.loads(line.strip())
            event = log_entry['EVENT_TYPE']
            current_enemies = log_entry['game_state']['enemies']

            for enemy in current_enemies:
                if enemy['health'] == 0:
                    exp_score += 200
            
            if log_entry['game_state']['player']['score'] != exp_score:
                print('FAIL')
                return 0

        if exp_score == 0:
            print('FAIL')
            return 0
        print('SUCCESS')
        return 1

    def test_injured(self):
        print("=======================Test injured=======================")

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        previous_player = None
        is_injured = False
        for line in lines:
            log_entry = json.loads(line.strip())
            event = log_entry['EVENT_TYPE']
            current_player = log_entry['game_state']['player']

            if event != 'INJURED':
                continue
            else:
                is_injured = True
                if previous_player is not None:
                    diff = previous_player['health'] - current_player['health']
                    if diff != 10:
                        print('FAIL')
                        return 0
            
            previous_player = current_player

        if is_injured:
            print('SUCCESS')
            return 1
        else:
            print('FAIL')
            return 0


    def test_block(self):
        print("=======================Test block=======================")
        self.tear_down()
        if os.path.exists('game.log'):
            os.remove('game.log')
        time.sleep(self.time)
        self.process = subprocess.Popen(['python', f'{self.py}'])
        time.sleep(self.time)
        grid = [[0] * 20 for _ in range(20)]
        
        for enemy in self.enemies_pos:
            grid[enemy[0]][enemy[1]] = 1

        move_path  = self.move_towards_nearest_enemy((0,0), self.obstracal_pos, grid)  
        
        directions = [move_path[0]]
        for i in range(len(move_path)-1):
            directions.append((move_path[i+1][0]-move_path[i][0], move_path[i+1][1]-move_path[i][1]))
        
        for direction in directions:
            press = self.direction[str(direction)]
            pg.press(press,presses=1,interval=0)
        
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        i = 0
        for line in lines:
            log_entry = json.loads(line.strip())
            event = log_entry['EVENT_TYPE']

            if event not in self.move.values():
                continue
            
            player_pos = tuple(log_entry['game_state']['player']['position'])
            # print(i, len(move_path) - 1, player_pos, move_path[i], event, self.move[self.direction[str(directions[i])]])
            if i != len(move_path) - 1:
                if player_pos != move_path[i] or event != self.move[self.direction[str(directions[i])]]:
                    print('FAIL')
                    return 0
                i += 1
            else:
                if player_pos == move_path[i-1] and event == self.move[self.direction[str(directions[i])]]:
                    print('SUCCESS')
                    return 1
                else:
                    print('FAIL')
                    return 0
        
        last_log_entry = json.loads(lines[-1].strip())
        player_pos = tuple(last_log_entry['game_state']['player']['position'])
        if player_pos == move_path[-2]:
            print('SUCCESS')
            return 1
        print('FAIL')
        return 0

    def test_log(self):
        print("=======================Test log=======================")
        with open('game.log', 'r') as file:
            lines = file.readlines()
        for line in lines:
            log_entry = json.loads(line.strip())

            if 'timestamp' not in log_entry:  
                print('FAIL')
                return 0
            
            if 'EVENT_TYPE' not in log_entry or log_entry['EVENT_TYPE'] not in self.event:
                print('FAIL')
                return 0
            
            if 'game_state' not in log_entry or not isinstance(log_entry['game_state'], dict):  
                print('FAIL')
                return 0

            player = log_entry['game_state'].get('player')  
            if not player or not isinstance(player, dict):
                print('player FAIL')
                return 0
            if 'position' not in player or not isinstance(player['position'], list) or len(player['position']) != 2:  
                print('position FAIL')
                return 0  
            if max(player['position'][0], player['position'][1]) > 19 or min(player['position'][0], player['position'][1]) < 0:
                print('position range FAIL')
                return 0 
            if 'health' not in player or not isinstance(player['health'], (int, float)):  
                print('health FAIL')
                return 0  
            if player['health'] > 200 or player['health'] < 0:
                print('health range FAIL')
                return 0 
            if 'score' not in player or not isinstance(player['score'], (int, float)):  
                print('score FAIL')
                return 0  
            if player['score'] > 400 or player['score'] < 0:
                print('score range FAIL')
                return 0 

            enemies = log_entry['game_state'].get('enemies')  
            if not isinstance(enemies, list):  
                print('enemies FAIL')
                return 0   
            for enemy in enemies:  
                if not isinstance(enemy, dict):  
                    print('enemies type FAIL')
                    return 0   
                if 'position' not in enemy or not isinstance(enemy['position'], list) or len(enemy['position']) != 2:  
                    print('enemy position FAIL')
                    return 0   
                if max(enemy['position'][0], enemy['position'][1]) > 19 or min(enemy['position'][0], enemy['position'][1]) < 0:
                    print('enemy position range FAIL')
                    return 0
                if 'health' not in enemy or not isinstance(enemy['health'], (int, float)):  
                    print('enemy health FAIL')
                    return 0   
                if enemy['health'] > 200 or enemy['health'] < 0:
                    print('enemy health range FAIL')
                    return 0
            
            if ('obstacle_position' not in log_entry and 'obstacle_position' not in log_entry['game_state']) or not isinstance(log_entry['game_state']['obstacle_position'], list):  
                print('obstacle_position FAIL')
                return 0
            for obstacle in log_entry['game_state']['obstacle_position']:  
                if len(obstacle) != 2:  
                    print('obstacle_position type FAIL')
                    return 0 
                if max(obstacle[0], obstacle[1]) > 19 or min(obstacle[0], obstacle[1]) < 0:
                    print('obstacle_position range FAIL')
                    return 0
            
        print('SUCCESS')
        return 1
        

    def main(self):
        result = {
            'total': 8,
            'total_basic': 5,
            'total_advanced': 3,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0,
                'init': 0,
                'move': 0,
                'block': 0,
                'fire': 0,
                'injured': 0,
                'score': 0,
                'log': 0,
            }
        }
        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except:
            self.tear_down()

        if result['test_cases']['set_up'] == 1:
            try:
                result['test_cases']['init'] += self.test_init()
            except:
                print('ERROR')
            try:
                result['test_cases']['move'] += self.test_move()
            except:
                print('ERROR')
            try:
                result['test_cases']['block'] += self.test_block()
            except:
                print('ERROR')
            try:
                result['test_cases']['fire'] += self.test_fire()
            except:
                print('ERROR')
            try:
                result['test_cases']['injured'] += self.test_injured()
            except:
                print('ERROR')
            try:
                result['test_cases']['score'] += self.test_score()
            except:
                print('ERROR')
            try:
                result['test_cases']['log'] += self.test_log()
            except:
                print('ERROR')

        self.tear_down()
        result['basic'] = result['test_cases']['set_up'] + result['test_cases']['init'] + result['test_cases']['log'] + result['test_cases']['move'] + result['test_cases']['block']
        result['advanced'] = result['test_cases']['fire'] + result['test_cases']['injured'] + result['test_cases']['score']
        
        return result
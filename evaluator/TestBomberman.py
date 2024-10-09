import os
import cv2
import time
import json
import subprocess
import math

import pyautogui as pg
import sys  
import os  
sys.path.append(os.path.abspath('evaluator')) 
from utils import *

class TestBomberman():

    def __init__(self, checker, py, time=2):
        if not os.path.exists('test'):
            os.makedirs('test')

        self.checker = checker
        self.time = time
        self.py = py

        self.process = None
        self.rect = None

        self.succ = 1
        self.total_test = 9
    
    def tear_down(self):
        self.process.terminate() 

    def test_set_up(self):
        print("=======================Test Set Up=======================")
        try:
            self.process = subprocess.Popen(['python', f'{self.py}'])
        except:
            print('FAIL')
            return 0
        
        time.sleep(self.time*2)
        print("SUCCESS")
        return 1
    

    def test_init(self):
        print("=======================Test init=======================")
        if not os.path.exists('game.log'):
            print('Log FAIL')
            return 0
        
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            print('FAIL')
            return 0
        
        log_entry = json.loads(lines[0].strip())
        event = log_entry['EVENT_TYPE']
        player = log_entry['player']
        enemies = log_entry['enemies']

        if event != 'INIT':
            print('INIT FAIL')
            return 0

        # player
        if player['score'] != 0:
            print('score FAIL')
            return 0
        if player['health'] != 100:
            print('health FAIL')
            return 0
        
        # enemies
        if len(enemies) != 2:
            print('enemies FAIL')
            return 0
        for enemy in enemies:
            if enemy['health'] != 10:
                print('enemies health FAIL')
                return 0

        # position
        game_board_state = log_entry['game_board_state']
        grid = math.sqrt(len(game_board_state))
        if grid.is_integer():
            grid = int(grid)
            if grid != 13:
                print('game board size FAIL')
                return 0
        else:
            print('game board size FAIL')
            return 0
        
        obstracts_pos = [index for index, value in enumerate(game_board_state) if value == -1]
        for index in obstracts_pos:
            row = index // 13
            col = index % 13
            if row % 2 != 0 or col % 2 != 0:
                print('obstracts FAIL')
                return 0

        player_pos = [index for index, value in enumerate(game_board_state) if value == 1]
        if player_pos[0] != 0 or len(player_pos) != 1:
            print('players FAIL')
            return 0
        
        enemies_pos = [index for index, value in enumerate(game_board_state) if value == 2]
        if len(enemies_pos) != 2:
            print('enemies FAIL')
            return 0
        

        print('SUCCESS')
        return 1
    
    
    def test_log(self):
        print("=======================Test log=======================")
        if not os.path.exists('game.log'):
            print('FAIL')
            return 0
        
        with open('game.log', 'r') as file:
            lines = file.readlines()
        for line in lines:
            log_entry = json.loads(line.strip())

            if 'timestamp' not in log_entry:  
                print('FAIL')
                return 0
            
            if 'EVENT_TYPE' not in log_entry or log_entry['EVENT_TYPE'] not in ['INIT', 'MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_UP', 'MOVE_DOWN', 'PLACE_BOMB', 'BOOM', 'INJURED']:
                print('FAIL')
                return 0
            
            if 'game_board_state' not in log_entry or not isinstance(log_entry['game_board_state'], list):  
                print('FAIL')
                return 0
            else:
                if len(log_entry['game_board_state']) != 169 or not all(isinstance(x, int) for x in log_entry['game_board_state']):
                    print('FAIL')
                    return 0
        
        print('SUCCESS')
        return 1

    def validate_player_move(self, previous_state, current_state, event):
        pre_pos = previous_state.index(1)
        cur_pos = current_state.index(1)

        new_pos = -1
        if event == 'MOVE_RIGHT':
            if pre_pos == 168:
                new_pos = pre_pos
            new_pos = pre_pos + 1
        elif event == 'MOVE_LEFT':
            if pre_pos == 0:
                new_pos = pre_pos
            new_pos = pre_pos - 1
        elif event == 'MOVE_UP':
            if pre_pos < 13:
                new_pos = pre_pos
            new_pos = pre_pos - 13
        elif event == 'MOVE_DOWN':
            if pre_pos >= 13 * 12:
                new_pos = pre_pos
            new_pos = pre_pos + 13
        
        if new_pos != cur_pos:
            return False
        return True

    def test_move(self):
        print("=======================Test move=======================")
        pg.press('right',presses=2,interval=0)
        pg.press('down',presses=2,interval=0)
        pg.press('left',presses=2,interval=0)
        pg.press('up',presses=2,interval=0)
        time.sleep(self.time)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        exp_event = ['MOVE_RIGHT', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_LEFT', 'MOVE_UP']
        previous_state = None
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            current_state = log_entry['game_board_state']
            if event in exp_event:
                if previous_state is not None:
                    if not self.validate_player_move(previous_state, current_state, event):
                        print('FAIL')
                        return 0
            previous_state = current_state

        print('SUCCESS')
        return 1
    

    def test_chase(self):
        print("=======================Test chase=======================")
        self.tear_down()
        time.sleep(self.time)
        if os.path.exists('game.log'):
            os.remove('game.log')
        self.process = subprocess.Popen(['python', f'{self.py}'])
        time.sleep(self.time)
        for i in range(3):
            pg.press('right',presses=1,interval=0)
            pg.press('left',presses=1,interval=0)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        previous_dis = [-1, -1]
        is_closer = False
        for line in lines:
            log_entry = json.loads(line.strip())

            current_state = log_entry['game_board_state']
            enemies_pos = [index for index, value in enumerate(current_state) if value == 2]
            for idx, pos in enumerate(enemies_pos):
                row = pos // 13
                col = pos % 13
                current_dis = row + col
                if previous_dis[idx] != -1:
                    if current_dis < previous_dis[idx]:
                        is_closer = True
                    if current_dis >= previous_dis[idx]:
                        is_closer = False
                previous_dis[idx] = current_dis

        if is_closer:     
            print('SUCCESS')
            return 1
        else:
            print('FAIL')
            return 0



    def test_block(self):
        print("=======================Test block=======================")
        self.tear_down()
        time.sleep(self.time)
        if os.path.exists('game.log'):
            os.remove('game.log')
        self.process = subprocess.Popen(['python', f'{self.py}'])
        time.sleep(self.time)
        pg.press('left',presses=1,interval=0)
        pg.press('right',presses=2,interval=0)
        pg.press('down',presses=1,interval=0)
        time.sleep(self.time)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        exp_event = ['MOVE_RIGHT', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_LEFT', 'MOVE_UP']
        previous_state = None
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            current_state = log_entry['game_board_state']
            if event in exp_event:
                if previous_state is not None:
                    if not self.validate_player_move(previous_state, current_state, event):
                        print('FAIL')
                        return 0
            previous_state = current_state

        print('SUCCESS')
        return 1
    
    def test_place_bomb(self):
        print("=======================Test place bomb=======================")
        self.tear_down()
        time.sleep(self.time)
        if os.path.exists('game.log'):
            os.remove('game.log')
        self.process = subprocess.Popen(['python', f'{self.py}'])
        time.sleep(self.time)
        pg.press('space',presses=1,interval=0)
        pg.press('down',presses=1,interval=0)
        time.sleep(self.time)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            current_state = log_entry['game_board_state']
            is_bomb = False
            if event == 'PLACE_BOMB':
                is_bomb = True
                if current_state[0] != 3:
                    print('FAIL')
                    return 0

            if event == 'BOOM':
                if current_state[1] != 4 or current_state[2] != 4 or current_state[3] != 4 or current_state[13] != 4 or current_state[26] != 4 or current_state[39] != 4:
                    print('FAIL')
                    return 0
        
        if not is_bomb:
            print('FAIL')
            return 0
        
        print('SUCCESS')
        return 1

    def test_injured(self):
        print("=======================Test injured=======================")
        time.sleep(self.time)
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            is_injured = False
            if event == 'INJURED':
                is_injured = True
                health = log_entry['player']['health']
                delta = 100 - health
                if delta % 10:
                    print('FAIL')
                    return 0
        
        if not is_injured:
            print('FAIL')
            return 0
        
        print('SUCCESS')
        return 1

    def test_defeat(self):
        print("=======================Test defeat=======================")
        flag = True
        start_time = time.time()
        while flag:
            with open('game.log', 'r') as file:
                lines = file.readlines()
            if len(lines) <= 1:
                print('FAIL')
                return 0
            log_entry = json.loads(lines[-1].strip())
            if log_entry['player']['score'] != 0:
                if log_entry['enemies'][0]['health'] != 0 and log_entry['enemies'][1]['health'] != 0:
                    print('FAIL')
                    return 0
                print('SUCCESS')
                return 1
            if time.time() - start_time > 3:  
                print('TIMEOUT')  
                return 0
                      
    # def test_gui(self):
    #     pass

    def main(self):
        result = {
            'total': 9,
            'total_basic': 6,
            'total_advanced': 3,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0,
                'init': 0,
                'move': 0,
                'block': 0,
                'chase': 0,
                'place_bomb': 0,
                'injured': 0,
                'defeat': 0,
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
                result['test_cases']['chase'] += self.test_chase()
            except:
                print('ERROR')
            try:
                result['test_cases']['place_bomb'] += self.test_place_bomb()
            except:
                print('ERROR')
            try:
                result['test_cases']['injured'] += self.test_injured()
            except:
                print('ERROR')
            try:
                result['test_cases']['defeat'] += self.test_defeat()
            except:
                print('ERROR')
            try:
                result['test_cases']['log'] += self.test_log()
            except:
                print('ERROR')

        self.tear_down()
        result['basic'] = result['test_cases']['set_up'] + result['test_cases']['init'] + result['test_cases']['log'] + result['test_cases']['move'] + result['test_cases']['block'] + result['test_cases']['place_bomb']
        result['advanced'] = result['test_cases']['chase'] + result['test_cases']['injured'] +result['test_cases']['defeat']

        return result



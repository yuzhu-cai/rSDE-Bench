import os
import cv2
import time
import json
import subprocess

import pyautogui as pg
import sys  
import os  
sys.path.append(os.path.abspath('evaluator')) 
from utils import *

class TestBalls():

    def __init__(self, checker, py, time=2):
        if not os.path.exists('test'):
            os.makedirs('test')

        self.checker = checker
        self.time = time
        self.py = py

        self.process = None
        self.rect = None
        self.width = None
        self.height = None

        self.fixed_pos = None
        self.player_radius = None

        self.event = ["INIT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN"]
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
        if rect == -1:
            print("FAIL")
            return 0
        else:
            print("SUCCESS")
            self.rect = rect
            self.width = rect[2] - rect[0]
            self.height = rect[3] - rect[1]
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
        game_state = log_entry['game_state']
        if event != 'INIT':
            print('FAIL')
            return 0

        # player
        if game_state['player']['position'] != [0, 0]:
            print('FAIL')
            return 0
        
        player_radius = game_state['player']['radius']
        self.player_radius = player_radius
        
        self.fixed_pos = game_state['fixed_enemies'][0]['position']
        
        # enemies
        if len(game_state['active_enemies']) != 3 and len(game_state['fixed_enemies']) != 1:
            print('FAIL')
            return 0
        
        # radius check
        for enemy in game_state['active_enemies']:
            if enemy['radius'] > player_radius:
                print('FAIL')
                return 0
        if game_state['fixed_enemies'][0]['radius'] > player_radius:
            print('FAIL')
            return 0

        print('SUCCESS')
        return 1
    

    def test_ui(self):
        print("=======================Test UI=======================")
        message = "The screenshot is the interface after the initialization of the Battle of Balls game implemented by a Python program. Please determine if there are 1 player ball and 4 enemy balls, and each ball has a different colors. In addition to player balls and enemy balls, there are also several other small balls that are much smaller than player balls and enemy balls. Answer 'True' or 'False'. Reply three lines in the following format:\n<ANS> 'Your answer'\n<REASON> 'Your reason'\n<INFO> 'Describe the screenshot'"
        pg.screenshot("test/board.jpg", region=[self.rect[0], self.rect[1], self.width, self.height])
        base64_image = [encode_image("test/board.jpg")]
        res = self.checker.check(message, base64_image)
        if 'true' in res['choices'][0]['message']['content'].lower():
            print("SUCCESS")
            return 1
        else:
            print("FAIL")
            return 0
    

    def test_move(self):

        print("=======================Test move=======================")
        # pg.press('right',presses=1,interval=0)
        # pg.press('down',presses=1,interval=0)
        # pg.press('left',presses=1,interval=0)
        # pg.press('up',presses=1,interval=0)
        # time.sleep(self.time)
        move = ['right', 'up', 'down', 'left']
        for i in range(2):
            for m in move:
                pg.keyDown(m)
                time.sleep(0.25)
                pg.keyUp(m)

        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0

        previous_dis = None
        
                
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            
            event = log_entry['EVENT_TYPE']
            if previous_dis is not None:
                player_pos =  log_entry['game_state']['player']['position']
                dis = [self.fixed_pos[0] - player_pos[0], self.fixed_pos[1] - player_pos[1]]
                if event == 'MOVE_RIGHT':  
                    if dis[1] != previous_dis[1]:
                        print('FAIL')
                        return 0
                    if dis[0] >= previous_dis[0]:
                        print('FAIL')
                        return 0
                elif event == 'MOVE_DOWN':  
                    if dis[0] != previous_dis[0]:
                        print('FAIL')
                        return 0
                    if dis[1] <= previous_dis[1]:
                        print('FAIL')
                        return 0
                elif event == 'MOVE_LEFT':  
                    if dis[1] != previous_dis[1]:
                        print('FAIL')
                        return 0
                    if dis[0] <= previous_dis[0]:
                        print('FAIL')
                        return 0
                elif event == 'MOVE_UP':  
                    if dis[0] != previous_dis[0]:
                        print('FAIL')
                        return 0
                    if dis[0] >= previous_dis[0]:
                        print('FAIL')
                        return 0

                previous_dis = dis
            
        print('SUCCESS')
        return 1


    def test_relative_move(self):
        print("=======================Test relative move=======================")
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) <= 1:
            print('FAIL')
            return 0
        
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())
            if log_entry['game_state']['player'] != [0, 0]:
                print('FAIL')
                return 0
            
        print('SUCCESS')
        return 1

    def test_consume(self):
        print("=======================Test consume=======================")
        move = ['right', 'up', 'left', 'left', 'down', 'down', 'right', 'right', 'up']
        for i in range(2):
            for m in move:
                pg.keyDown(m)
                time.sleep(1)
                pg.keyUp(m)


        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            print('FAIL')
            return 0
        
        previous_radius = None

        for line in lines:
            log_entry = json.loads(line.strip())
            game_state = log_entry['game_state']
            player_radius = game_state['player']['radius']
            
            if previous_radius is not None:
                for enemy in game_state['active_enemies']:
                    if enemy['radius'] == -1:
                        if player_radius <= previous_radius:
                            print('FAIL')
                            return 0
            
            previous_radius = player_radius

        if previous_radius <= self.player_radius:
            print('FAIL')
            return 0
        
        print('SUCCESS')
        return 1
    

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
                print('FAIL')
                return 0
            if 'radius' not in player or not isinstance(player['radius'], (int, float)):  
                print('FAIL')
                return 0 

            active_enemies = log_entry['game_state'].get('active_enemies')  
            if not isinstance(active_enemies, list):  
                print('FAIL')
                return 0   
            for enemy in active_enemies:  
                if not isinstance(enemy, dict):  
                    print('FAIL')
                    return 0   
                if 'position' not in enemy or not isinstance(enemy['position'], list) or len(enemy['position']) != 2:  
                    print('FAIL')
                    return 0   
                if 'radius' not in enemy or not isinstance(enemy['radius'], (int, float)):  
                    print('FAIL')
                    return 0   
                
            fixed_enemies = log_entry['game_state'].get('fixed_enemies')  
            if not fixed_enemies or not isinstance(fixed_enemies, list) or len(fixed_enemies) != 1:
                print('FAIL')
                return 0
            if 'radius' not in fixed_enemies[0] or not isinstance(fixed_enemies[0]['radius'], (int, float)) or len(fixed_enemies[0]['position']) != 2: 
                print('FAIL')
                return 0
            
        print('SUCCESS')
        return 1
        

    def main(self):
        result = {
            'total': 7,
            'total_basic': 5,
            'total_advanced': 2,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0,
                'init': 0,
                'move': 0,
                'ui': 0,
                'relative_move': 0,
                'consume': 0,
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
                result['test_cases']['ui'] += self.test_ui()
            except:
                print('ERROR')
            try:
                result['test_cases']['move'] += self.test_move()
            except:
                print('ERROR')
            try:
                result['test_cases']['relative_move'] += self.test_relative_move()
            except:
                print('ERROR')
            try:
                result['test_cases']['consume'] += self.test_consume()
            except:
                print('ERROR')
            try:
                result['test_cases']['log'] += self.test_log()
            except:
                print('ERROR')

        self.tear_down()
        result['basic'] = result['test_cases']['set_up'] + result['test_cases']['init'] + result['test_cases']['log'] + result['test_cases']['move'] + result['test_cases']['ui']
        result['advanced'] = result['test_cases']['consume'] + result['test_cases']['relative_move']
        
        return result
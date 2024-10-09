import os
import cv2
import time
import json
import math
import subprocess

import pyautogui as pg
import sys
sys.path.append(os.path.dirname(__file__))
from utils import *
from checker import Checker

class TestGomoku():

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
        self.grid = None
        self.bias = None
        self.winner = None

        self.succ = 1
        self.total_test = 6


    def tear_down(self):
        self.process.terminate() 
    
    def check_board_update(self, previous_state, current_state, event_type, last_event_type):  
        changes = [(p, c) for p, c in zip(previous_state, current_state) if p != c]  
          
        if not changes:  
            return False 
        black_count = sum([1 for p, c in changes if c == -1])  
        white_count = sum([1 for p, c in changes if c == 1])  

        for p, c in changes:
            m = p + c
            if m == 0:
                return False
            
        if (event_type == 'BLACK' and last_event_type == 'BLACK') or (event_type == 'WHITE' and last_event_type == 'WHITE'):  
            return False
        
        if event_type == 'BLACK':  
            if black_count != 1 or white_count != 0:  
                return False 
        elif event_type == 'WHITE':  
            if white_count != 1 or black_count != 0: 
                return False
        else:
            return False  
        
        return True 

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
        self.rect = rect
        self.width = rect[2] - rect[0]
        self.height = rect[3] - rect[1]

        step_l = self.width // 5
        step_h = self.height // 5

        self.clicks = [
            (rect[0]+step_l, rect[1]+step_h),
            (int(0.5*(rect[0]+rect[2])), int(0.5*(rect[1]+rect[3]))),
            (rect[0]+step_l * 2, rect[1]+step_h * 2),
        ]
        
        print("SUCCESS")
        return 1
    
    def test_winboard(self):
        print("=======================Test win board=======================")
        message = f"This is a final screenshot of two player Gomoku game implemented by a Python program. You need to determine from the screenshot whether the chessboard state of this process matches the process of two players playing Gomoku, and whether there is text indicating that the {self.winner} has won. Answer 'True' or 'False'. Reply three lines in the following format:\n<ANS> 'Your answer'\n<REASON> 'Your reason'\n<INFO> 'Describe the screenshot'"
        base64_images = []
        img=cv2.imread(f"test/winner.png",1)
        cv2.imwrite(f"test/winner_.jpg",img,[cv2.IMWRITE_JPEG_QUALITY,1])
        base64_images.append(encode_image(f"test/winner_.jpg"))

        res = self.checker.check(message, base64_images)
        if 'true' in res['choices'][0]['message']['content'].lower():
            print('SUCCESS')
            return 1
        else:
            print('FAIL')
            return 0

    def test_init(self):
        print("=======================Test init=======================")
        with open('game.log', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            print('FAIL')
            return 0
        
        log_entry = json.loads(lines[0].strip())
        grid = math.sqrt(len(log_entry['game_board_state']))
        if grid.is_integer():
            self.grid = int(grid)
            if self.grid <= 5:
                self.grid == None
                print('FAIL')
                return 0
        else:
            print('FAIL')
            return 0
        
        message = "his is the initialization board for a two player Gomoku game. Please check if this board is a Gomoku board. Answer 'True' or 'False'. Reply three lines in the following format:\n<ANS> 'Your answer'\n<REASON> 'Your reason'\n<INFO> 'Describe the screenshot'"
        screenshot = pg.screenshot("test/board.png", region=[self.rect[0], self.rect[1], self.width, self.height])
        screenshot.save("test/board.png")

        img = cv2.imread(f"test/board.png",1)
        cv2.imwrite(f"test/board.jpg",img,[cv2.IMWRITE_JPEG_QUALITY,1])
        base64_image = [encode_image("test/board.jpg")]
        res = self.checker.check(message, base64_image)

        if 'true' not in res['choices'][0]['message']['content'].lower():
            print("FAIL")
            return 0

        print('SUCCESS')
        return 1
        
    
    def test_click(self):
        print("=======================Test Click=======================")
        if self.grid is None:
            print('FAIL')
            return 0
        
        cell = self.width // self.grid
        self.bias = self.width // 2 + cell // 5

        clicks = [  
            (  
                int(self.rect[0] + self.bias + (i % 2) * 2 * cell),
                int(self.rect[1] + self.bias + (i // 2) * cell)  
            )  
            for i in range(10)  
        ]

        for i, click in enumerate(clicks):
            time.sleep(0.1)
            pg.moveTo(click, duration=0.1)
            time.sleep(0.1)
            pg.click(x=click[0], y=click[1],clicks=1,interval=0,duration=0.1, button='left')
        
        screenshot = pg.screenshot(f"test/winner.png", region=[self.rect[0], self.rect[1], self.width, self.height])
        screenshot.save("test/winner.png")

        with open('game.log', 'r') as file:
            lines = file.readlines()
        
        if len(lines) == 0 or len(lines) != 10:
            print('FAIL')
            return 0
        
        previous_state = None
        last_event_type = None
        
        for idx, line in enumerate(lines):
            log_entry = json.loads(line.strip())  
            event_type = log_entry["EVENT_TYPE"]
            
            if idx == 0 and event_type != 'INIT':
                print('FAIL')
                return 0
            
            current_state = log_entry["game_board_state"]
            if previous_state is not None:
                if not self.check_board_update(previous_state, current_state, log_entry['EVENT_TYPE'], last_event_type):
                    print('FAIL')
                    return 0
                
            previous_state = current_state
            last_event_type = log_entry['EVENT_TYPE']

        print("SUCCESS")
        return 1
    
    def check_five_in_a_row(self, board):
        
        def check_direction(row, col, delta_row, delta_col): 
            count = 0  
            player = board[row * self.grid + col]
  
            for _ in range(5):  
                r, c = row + delta_row * _, col + delta_col * _  
                if 0 <= r < self.grid and 0 <= c < self.grid and board[r * self.grid + c] == player:  
                    count += 1  
                else:  
                    break  
            
            return count == 5   

        for row in range(self.grid):  
            for col in range(self.grid):  
                if board[row * self.grid + col] != 0: 
                    if (check_direction(row, col, 0, 1) or  
                        check_direction(row, col, 1, 0) or   
                        check_direction(row, col, 1, 1) or  
                        check_direction(row, col, 1, -1)):  
                        return 'BLACK' if board[row * self.grid + col] == -1 else 'WHITE' 
        
        return None

    def test_win(self):
        print("=======================Test Win=======================")
        with open('game.log', 'r') as file:
            lines = file.readlines()
        
        last_entry = json.loads(lines[-1].strip())  
        last_state = last_entry['game_board_state']
        winner = self.check_five_in_a_row(last_state)
        self.winner = winner
        print(winner)
        if winner == None:
            print('FAIL')
            return 0
        else:
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
            
            if 'EVENT_TYPE' not in log_entry or log_entry['EVENT_TYPE'] not in ['INIT', 'WHITE', 'BLACK']:
                print('FAIL')
                return 0
            
            if 'game_board_state' not in log_entry or not isinstance(log_entry['game_board_state'], list):  
                print('FAIL')
                return 0

        print('SUCCESS')
        return 1
    
    def main(self):
        result = {
            'total': 6,
            'total_basic': 3,
            'total_advanced': 3,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0,
                'init': 0,
                'click': 0,
                'win': 0,
                'winboard': 0,
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
                result['test_cases']['click'] += self.test_click()
            except:
                print('ERROR')
            try:
                result['test_cases']['win'] += self.test_win()
            except:
                print('ERROR')
            try:
                result['test_cases']['winboard'] += self.test_winboard()
            except:
                print('ERROR')
            try:
                result['test_cases']['log'] += self.test_log()
            except:
                print('ERROR')

        self.tear_down()
        result['basic'] = result['test_cases']['set_up'] + result['test_cases']['init'] + result['test_cases']['log']
        result['advanced'] = result['test_cases']['win'] + result['test_cases']['winboard'] + result['test_cases']['click']
        
        return result
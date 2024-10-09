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

class Test2048():

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

        self.succ = 1
        self.total_test = 9
        self.map = {
            'INIT': 0,
            'LEFT': 1,
            'RIGHT': 2,
            'UP': 3,
            'DOWN': 4
        }

    def tear_down(self):
        self.process.terminate() 
    
    def is_valid_move(self, previous_state, current_state, event_type):
        def compress(previous_state):  
            new_state = [[0] * 4 for _ in range(4)]  
            for r in range(4):  
                idx = 0  
                for c in range(4):  
                    if previous_state[r][c] != 0:  
                        new_state[r][idx] = previous_state[r][c]  
                        idx += 1  
            return new_state 

        def merge(new_state):  
            for r in range(4):  
                for c in range(4 - 1):  
                    if new_state[r][c] == new_state[r][c + 1] and new_state[r][c] != 0:  
                        new_state[r][c] *= 2  
                        new_state[r][c + 1] = 0
            return new_state
        
        def rotate_board(new_state):  
            new_state = [list(row) for row in zip(*new_state[::-1])]  
            return new_state
        
        def move_left(previous_state):
            new_state = compress(merge(compress(previous_state)))
            return new_state
        
        def compare_states(current_state, expect_state):  
            for r in range(4):  
                for c in range(4):  
                    if expect_state[r][c] != 0:  
                        if current_state[r][c] != expect_state[r][c]:  
                            return False  
            return True
        
        if event_type == 'LEFT':
            expect_state = move_left(previous_state)

        elif event_type == 'RIGHT':
            new_state = rotate_board(rotate_board(previous_state))
            new_state = move_left(new_state)
            expect_state = rotate_board(rotate_board(new_state))

        elif event_type == 'UP':
            new_state = rotate_board(rotate_board(rotate_board(previous_state)))
            new_state = move_left(new_state)
            expect_state = rotate_board(new_state)

        elif event_type == 'DOWN':
            new_state = rotate_board(previous_state)
            new_state = move_left(new_state)
            expect_state = rotate_board(rotate_board(rotate_board(new_state)))
        else:
            return False, -1

        if compare_states(current_state, expect_state):
            return True, expect_state
        else:
            return False, -1
    
    def validate_game_log(self, file_path, event, idx):  
        if not os.path.exists(file_path):
            return False
        
        with open(file_path, 'r') as log_file:  
            lines = log_file.readlines()  

        current_entry = json.loads(lines[idx].strip())
        event_type = current_entry["EVENT_TYPE"]  
        current_state = [current_entry["game_board_state"][i:i+4] for i in range(0, 16, 4)]  

        if event_type != event:
            return False

        try:
            previous_entry = json.loads(lines[idx-1].strip()) 
            previous_state = [previous_entry["game_board_state"][i:i+4] for i in range(0, 16, 4)] 
        except:
            return False
        
        if not self.is_valid_move(previous_state, current_state, event_type)[0]:  
            print(f"Invalid move detected: {event_type}, from {previous_state} to {current_state}")  
            return False
            
        return True 

    def test_set_up(self):
        print("=======================Test Set Up=======================")
        try:
            self.process = subprocess.Popen(['python', f'{self.py}'])
        except:
            return False
        
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
        
    def test_board(self):
        print("=======================Test Board=======================")
        message = "The screenshot is the interface after the initialization of the 2048 game implemented by a Python program. Please confirm whether this interface is compatible with 2048 games based on the screenshot. Answer 'True' or 'False'. Reply three lines in the following format:\n<ANS> 'Your answer'\n<REASON> 'Your reason'\n<INFO> 'Describe the screenshot'"
        sceenshoot = pg.screenshot("test/board.png", region=[self.rect[0], self.rect[1], self.width, self.height])
        sceenshoot.save("test/board.png")
        base64_image = [encode_image("test/board.png")]
        res = self.checker.check(message, base64_image)
        if 'true' in res['choices'][0]['message']['content'].lower():
            print("SUCCESS")
            return 1
        else:
            print("FAIL")
            return 0
        
    def test_interaction(self):
        print("=======================Test INTERACTION=======================")
        message = "This is a 2048 game implemented by a Python program. In order to test whether the program implements the 2048 game well, I simulated the input of the keyboard's left key messages and obtained screenshots of the 2048 game board before and after pressing the key. Based on the screenshots before and after pressing the left button, you need to determine whether the 2048 game board status has changed during this process.\nAnswer 'True' or 'False'. Reply three lines in the following format:\n<ANS> 'Your answer'\n<REASON> 'Your reason'\n<INFO> 'Describe two screenshots'"
        sceenshoot = pg.screenshot("test/left_.png", region=[self.rect[0], self.rect[1], self.width, self.height])
        sceenshoot.save("test/left_.png")
        pg.press('left',presses=1,interval=0)
        time.sleep(self.time)
        sceenshoot = pg.screenshot("test/left.png", region=[self.rect[0], self.rect[1], self.width, self.height])
        sceenshoot.save("test/left.png")
        base64_image = [encode_image("test/left_.png"), encode_image("test/left.png")]
        res = self.checker.check(message, base64_image)
        if 'true' in res['choices'][0]['message']['content'].lower():
            print('SUCCESS')
            return 1
        else:
            print('FAIL')
            return 0

      
    def test_move(self, move):
        print(f"=======================Test {move}=======================")
        # time.sleep(self.time)
        pg.press(move.lower(),presses=1,interval=0)
        time.sleep(self.time)
        if self.validate_game_log('game.log', move, self.map[move]):
            print("SUCCESS")
            return 1
        else:
            print("FAIL")
            return 0

    def test_new(self):
        print("=======================Test NEW=======================")
        if not os.path.exists('game.log'):
            return 0

        with open('game.log', 'r') as log_file:  
            lines = log_file.readlines()

        previous_state = None  
        
        for idx, line in enumerate(lines):  
            log_entry = json.loads(line.strip())  
            event_type = log_entry["EVENT_TYPE"]  

            if idx != self.map[event_type]:
                print('FAIL')
                return 0

            if len(log_entry["game_board_state"] ) != 16:
                print('FAIL')
                return 0
            
            current_state = [log_entry["game_board_state"][i:i+4] for i in range(0, 16, 4)]   

            if previous_state is not None:  
                flag, expect_state = self.is_valid_move(previous_state, current_state, event_type)
                if not flag:
                    print('FAIL')
                    return 0
                else:
                    new = 0
                    for r in range(4):  
                        for c in range(4):  
                            if current_state[r][c] != 0:  
                                if expect_state[r][c] != current_state[r][c]:
                                    new += 1
                    if new != 1:
                        print('FAIL')
                        return 0            
            # Update the previous state  
            previous_state = current_state  
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
            
            if 'EVENT_TYPE' not in log_entry or log_entry['EVENT_TYPE'] not in ['INIT', 'LEFT', 'RIGHT', 'UP', 'DOWN']:
                print('FAIL')
                return 0
            
            if 'game_board_state' not in log_entry or not isinstance(log_entry['game_board_state'], list):  
                print('FAIL')
                return 0
            
        print('SUCCESS')
        return 1
            
    def main(self):
        result = {
            'total': 9,
            'total_basic': 3,
            'total_advanced': 6,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0,
                'board': 0,
                'left': 0,
                'right': 0,
                'up': 0,
                'down': 0,
                'new': 0,
                'interaction': 0,
                'log': 0,
            }
        }
        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except:
            self.tear_down()

        if result['test_cases']['set_up'] == 1:
            try :
                result['test_cases']['board'] = self.test_board()
            except:
                print("ERROR")
            try :
                result['test_cases']['left']= self.test_move('LEFT')
            except:
                print("ERROR")
            try :
                result['test_cases']['right'] = self.test_move('RIGHT')
            except:
                print("ERROR")
            try :
                result['test_cases']['up'] = self.test_move('UP')
            except:
                print("ERROR")
            try :
                result['test_cases']['down'] = self.test_move('DOWN')
            except:
                print("ERROR")
            try :
                result['test_cases']['new'] = self.test_new()
            except:
                print("ERROR")
            try :
                result['test_cases']['interaction'] = self.test_interaction()
            except:
                print("ERROR")
            try :
                result['test_cases']['log'] = self.test_log()
            except:
                print("ERROR")
        self.tear_down()
        result['basic'] = result['test_cases']['set_up'] + result['test_cases']['board'] + result['test_cases']['log']
        result['advanced'] = result['test_cases']['left'] + result['test_cases']['right'] + result['test_cases']['up'] + result['test_cases']['down'] + result['test_cases']['new'] + result['test_cases']['interaction']
        
        return result
import os
import time
import subprocess
import json
import pyautogui as pg
import pygetwindow as gw
from pywinauto import Application, keyboard

class TestSokoban():

    def __init__(self, checker, py, time=3):
        if not os.path.exists('test'):
            os.makedirs('test')
    
        self.checker = checker
        self.time = time
        self.py = py
        self.process = None
        self.app = None
        self.win = None



    def tear_down(self):
        if self.process:
            self.process.terminate() 
        if self.win:
            self.win.close()
    def read_log(self): # Read game.log, return a list of dictionaries
        with open("game.log", 'r') as file:
            logs = [json.loads(line) for line in file.readlines()]
        return logs

    def delete_log(self):
        if os.path.exists("game.log"):
            os.remove("game.log")
    def start_game(self): # Start the game
        #self.delete_log() # Delete game.log if it exists
        self.process = subprocess.Popen(["python", f'{self.py}'])
        time.sleep(1)

        # Attempt to find the window associated with the game
        win_list = gw.getWindowsWithTitle("Sokoban Game")  # Replace with your game window title
        if win_list:
            self.win = win_list[0]
            self.win.activate()
            self.app = Application().connect(handle=self.win._hWnd)
        else:
            raise Exception("Game window not found")


    def press_key(self, key):
        if self.app and self.win:
            self.win.activate()
            keyboard.send_keys(key)
            time.sleep(0.3)  # Adding a delay to mimic the original timing

    def check_Excutablity(self):
        try:
            print("=======================Test Set Up=======================")
            self.start_game()
    
            # 检查窗口是否存在且不为空标题
            if self.win and self.win.title:
                print("程序正常启动")
                return 1  # 返回 1 表示程序正常运行
            else:
                print("程序启动失败或存在问题")
                return 0  # 返回 0 表示程序启动失败或存在问题
        except Exception as e:
            print(f"检测程序执行时发生错误: {e}")
            return 0  # 发生异常，返回 0 表示程序启动失败或存在问题


    def check_log(self):
        try:
            print("=======================Test Log=======================")

            self.start_game()
            for key in ['{RIGHT}', '{LEFT}', '{UP}', '{DOWN}', '{RIGHT}', '{LEFT}', '{UP}', '{DOWN}']:
                self.press_key(key)
            print("Key presses executed successfully.")
    
            time.sleep(1)
            logs = self.read_log()
            print(logs)
            if not logs:
                print("日志文件为空")
                return 0

            for log_entry in logs:
                required_keys = ["timestamp", "EVENT_TYPE", "player_position", "box_positions", "game_status"]
                for key in required_keys:
                    if key not in log_entry:
                        print(f"缺少字段: {key}")
                        return 0

                if log_entry["EVENT_TYPE"] not in ["MOVE_RIGHT", "MOVE_LEFT", "MOVE_UP", "MOVE_DOWN", "INVALID_MOVE"]:
                    print(f"EVENT_TYPE 值错误: {log_entry['EVENT_TYPE']}")
                    return 0

                if not (isinstance(log_entry["player_position"], list) and len(log_entry["player_position"]) == 2):
                    print(f"player_position 格式错误: {log_entry['player_position']}")
                    return 0

                if not all(isinstance(pos, list) and len(pos) == 2 for pos in log_entry["box_positions"]):
                    print(f"box_positions 格式错误: {log_entry['box_positions']}")
                    return 0

                if log_entry["game_status"] not in ["ONGOING", "COMPLETE"]:
                    print(f"game_status 值错误: {log_entry['game_status']}")
                    return 0

            print("日志文件格式正确")
            return 1
        except FileNotFoundError:
            print("日志文件未找到")
            return 0
        except Exception as e:
            print(f"发生异常: {e}")
            return 0

    def check_move_right(self):
        try:
            print("=======================Test Move Right=======================")

            self.start_game()

            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.process.terminate()
            print("terminated")
            logs = self.read_log()
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_right:
                    mario_x2 = log["player_position"][0]
                    if mario_x2 > mario_x1:
                        print("可以向右移动")
                        return 1
                if log["EVENT_TYPE"] == "MOVE_RIGHT" and not find_move_right:
                    mario_x1 = log["player_position"][0]
                    find_move_right = True
            print("无法向右移动")
            return 0
        except:
            print("向右移动时出错")
            return 0

    def check_move_left(self):
        try:
            print("=======================Test Move Left=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.process.terminate()
            print("terminated")
            logs = self.read_log()
            find_move_left = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_left:
                    mario_x2 = log["player_position"][0]
                    if mario_x2 < mario_x1:
                        print("可以向左移动")
                        return 1
                if log["EVENT_TYPE"] == "MOVE_LEFT" and not find_move_left:
                    mario_x1 = log["player_position"][0]
                    find_move_left = True
            print("无法向左移动")
            return 0
        except:
            print("向左移动时出错")
            return 0

    def check_move_box(self):
        global can_move
        try:
            print("=======================Test Move Box=======================")
            self.start_game()
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')

            self.process.terminate()
            logs = self.read_log()
            mario_x2 = logs[-1]["box_positions"][0][0]
            mario_x1 = logs[-2]["box_positions"][0][0]
            if mario_x2 > mario_x1:
                print("可以移动箱子")
                can_move = 1
                return 1
            print("无法移动箱子")
            return 0
        except:
            print("移动箱子时出错")
            return 0

    def check_move_wall(self):
        global can_move
        try:
            print("=======================Test Move Wall=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')

            self.process.terminate()
            logs = self.read_log()
            mario_x2 = logs[-1]["box_positions"][0][1]
            mario_x1 = logs[-2]["box_positions"][0][1]
            if mario_x2 == mario_x1 and can_move == 1:
                print("遵守墙壁规则")
                return 1
            print("未遵守墙壁规则")
            return 0
        except:
            print("遵守墙壁规则时出错")
            return 0

    def check_seqbox(self):
        global can_move
        try:
            print("=======================Test Seqbox=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{LEFT}')


            self.process.terminate()
            logs = self.read_log()
            mario_x2 = logs[-1]["box_positions"][0][0]
            mario_x1 = logs[-2]["box_positions"][0][0]

            mario_2 = logs[-1]["box_positions"][1][0]
            mario_1 = logs[-2]["box_positions"][1][0]
            if mario_x2 == mario_x1 and mario_1 == mario_2 and can_move == 1:
                print("遵守序列规则")
                return 1
            print("未遵守序列规则")
            return 0
        except:
            print("检查序列规则时出错")
            return 0

    def check_end(self):
        global can_win
        try:
            print("=======================Test End=======================")
            self.start_game()
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{UP}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{UP}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')

            self.process.terminate()
            logs = self.read_log()
            mario_x2 = logs[-1]["game_status"]
            if mario_x2 == "COMPLETE":
                print("游戏可以正常结束")
                can_win = 1
                return 1
            print("游戏未正常结束")
            return 0
        except:
            print("游戏结束时出错")
            return 0

    def check_wrong_end(self):
        try:
            print("=======================Test Wrong End=======================")
            self.start_game()
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{UP}')
            self.press_key('{RIGHT}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{DOWN}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')

            self.process.terminate()
            logs = self.read_log()
            mario_x2 = logs[-1]["game_status"]
            if mario_x2 == "ONGOING" and can_win == 1:
                print("可以避免错误结束")
                return 1
            print("错误结束未被避免")
            return 0
        except:
            print("检查错误结束时出错")
            return 0

    def main(self):
        result = {
            'total': 9,
            'total_basic': 5,
            'total_advanced': 4,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'excutability': 0,
                'log': 0,
                'left': 0,
                'right': 0,
                'move_box': 0,
                'move_wall': 0,
                'seqbox': 0,
                'end': 0,
                'wrong_end': 0,
            }
        }
        try:
            result['test_cases']['excutability'] = self.check_Excutablity()
        except:
            self.tear_down()
    
        if result['test_cases']['excutability'] == 1:
            try:
                result['test_cases']['log'] = self.check_log()
            except:
                print("ERROR")
            try:
                result['test_cases']['left'] = self.check_move_left()
            except:
                print("ERROR")
            try:
                result['test_cases']['right'] = self.check_move_right()
            except:
                print("ERROR")
            try:
                result['test_cases']['move_box'] = self.check_move_box()
            except:
                print("ERROR")
            try:
                result['test_cases']['move_wall'] = self.check_move_wall()
            except:
                print("ERROR")
            try:
                result['test_cases']['seqbox'] = self.check_seqbox()
            except:
                print("ERROR")
            try:
                result['test_cases']['end'] = self.check_end()
            except:
                print("ERROR")
            try:
                result['test_cases']['wrong_end'] = self.check_wrong_end()
            except:
                print("ERROR")
            
        result['basic'] = result['test_cases']['excutability'] + result['test_cases']['log'] + result['test_cases']['left'] + result['test_cases']['right'] + result['test_cases']['move_box']
        result['advanced'] = result['test_cases']['move_wall'] + result['test_cases']['seqbox'] + result['test_cases']['end'] + result['test_cases']['wrong_end']
    
        return result
    
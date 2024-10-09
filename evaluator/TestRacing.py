import os
import time
import subprocess
import json
import pyautogui as pg
import pygetwindow as gw
from pywinauto import Application, keyboard

class TestRacing():

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

    def delete_log(self): # Delete game.log
        if os.path.exists("game.log"):
            os.remove("game.log")

    def start_game(self): # Start the game
        #self.delete_log() # Delete game.log if it exists
        self.process = subprocess.Popen(["python", f'{self.py}'])
        time.sleep(1)

        # Attempt to find the window associated with the game
        win_list = gw.getWindowsWithTitle("Racing Game")  # Replace with your game window title
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
        """
        检查日志文件的格式是否符合规定。
        :return: int, 1 表示所有日志条目都符合格式，0 表示不符合或日志文件为空
        """
        try:
            # 执行一些操作，例如模拟按键（这里假设有一个 start_game 函数）
            print("=======================Test log=======================")
            self.start_game()

            # Execute some key presses
            for key in ['{RIGHT}', '{LEFT}', '{UP}', '{DOWN}', '{RIGHT}', '{LEFT}', '{UP}', '{DOWN}']:
                self.press_key(key)

            time.sleep(1)  # Wait for log to be written

            # Read and check log
            logs = self.read_log()
            # 检查日志是否为空
            if not logs:
                print("日志文件为空")
                return 0

            for log_entry in logs:
                try:
                    # 替换单引号为双引号，解析为 JSON 对象
                    

                    # 检查必要的字段是否存在
                    required_keys = ["timestamp", "EVENT_TYPE", "car_speed", "car_position"]
                    for key in required_keys:
                        if key not in log_entry:
                            print(f"缺少字段: {key}")
                            return 0

                    # 检查 EVENT_TYPE 是否在允许的值中
                    valid_event_types = ["speed_up", "speed_down", "move_left", "move_right", "stop", "collide_fatal_obstacles", "collide_slow_down_obstacles"]
                    if log_entry["EVENT_TYPE"] not in valid_event_types:
                        print(f"EVENT_TYPE 值错误: {log_entry['EVENT_TYPE']}")
                        return 0

                    # 检查 car_speed 是否为数值
                    if not isinstance(log_entry["car_speed"], (int, float)):
                        print(f"car_speed 格式错误: {log_entry['car_speed']}")
                        return 0

                    # 检查 car_position 是否为 [x, y] 格式
                    if not (isinstance(log_entry["car_position"], list) and len(log_entry["car_position"]) == 2):
                        print(f"car_position 格式错误: {log_entry['car_position']}")
                        return 0

                except json.JSONDecodeError:
                    print("JSON 解析错误")
                    return 0

            # 如果所有日志条目都符合格式
            print("日志文件格式正确")
            return 1
        except FileNotFoundError:
            print("日志文件未找到")
            return 0
        except Exception as e:
            print(f"发生异常: {e}")
            return 0
    
    def check_move_left(self): # Check if Mario can move right
        try:
            print("=======================Test left=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.process.terminate()
            print("terminated")
            

            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_right:
                    mario_x2 = log["car_position"][0]
                    if mario_x2 < mario_x1:
                        print(" can move left\n\n")
                        return 1    # Mario can move right+1
                if log["EVENT_TYPE"] == "move_left" and find_move_right == False:
                    mario_x1 = log["car_position"][0]
                    find_move_right = True
            print(" can't move left\n\n")
            return 0    # Mario can't move right



        except:
            print("Move left error")
            return 0
    def check_move_right(self): # Check if Mario can move right
        try:
            print("=======================Test right=======================")
            self.start_game()

            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.process.terminate()
            print("terminated")
            

            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_right:
                    mario_x2 = log["car_position"][0]
                    if mario_x2 > mario_x1:
                        print(" can move right\n\n")
                        return 1    # Mario can move right+1
                if log["EVENT_TYPE"] == "move_right" and find_move_right == False:
                    mario_x1 = log["car_position"][0]
                    find_move_right = True
            print(" can't move right\n\n")
            return 0    # Mario can't move right

        except:
            print("Move right error")
            return 0
    def check_speed_up(self):
        try:
            print("=======================Test speed up=======================")
            self.start_game()

            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.process.terminate()
            print("terminated")
            

            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_right:
                    mario_x2 = log["car_speed"]
                    if mario_x2 > mario_x1:
                        print("Mario can check_speed_up\n\n")
                        return 1    # Mario can move right+1
                if log["EVENT_TYPE"] == "speed_up" and find_move_right == False:
                    mario_x1 = log["car_speed"]
                    find_move_right = True
            print("Mario can't check_speed_up\n\n")
            return 0    # Mario can't move right
        except:
            print("speed up error\n\n")
            return 0

    def check_speed_down(self):
        try:
            print("=======================Test speed down=======================")
            self.start_game()
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.press_key('{DOWN}')
            self.process.terminate()
            print("terminated")
            

            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_right:
                    mario_x2 = log["car_speed"]
                    if mario_x2 < mario_x1:
                        print("Mario can check_speed_down\n\n")
                        return 1    # Mario can move right+1
                if log["EVENT_TYPE"] == "speed_down" and find_move_right == False:
                    mario_x1 = log["car_speed"]
                    find_move_right = True
            print("Mario can't check_speed_down\n\n")
            return 0    # Mario can't move right
        except:
            print("speed down error")
            return 0
        

    
    def check_move_overright(self): # Check if Mario can move right
        try:
            print("=======================Test check_move_overright=======================")
            self.start_game()

            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.press_key('{RIGHT}')
            self.process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            mario_x2 = logs[-1]["car_position"][0]
            
            if(mario_x2 == 3):
                print(" obey over right\n\n")
                return 1
            
            
            print(mario_x2)
            
            print(" can't obey over right\n\n")
            return 0    # Mario can't move left
        except:
            print("over right error\n\n")
            return 0
    def check_move_overleft(self): # Check if Mario can move right
        try:
            print("=======================Test check_move_overleft=======================")
            self.start_game()
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.press_key('{LEFT}')
            self.process.terminate()
            print("terminated")
            
            # Read the log
            logs = self.read_log()
            print(logs)
            mario_x2 = logs[-1]["car_position"][0]
            
            if(mario_x2 == 1):
                print(" obey over left\n\n")
                return 1
            
            
            print(mario_x2)
            
            print(" can't obey over left\n\n")
            return 0    # Mario can't move left
        except:
            print("over left error")
            return 0
    def check_stop(self):
        try:
            print("=======================Test check_stop=======================")
            self.start_game()
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('s')
            self.press_key('s')
            self.press_key('s')
            self.press_key('s')
            self.press_key('s')
            self.process.terminate()
            print("terminated")

            # Read the log
            logs = self.read_log()
            print(logs)
            mario_x2 = logs[-1]["car_speed"]
            type = logs[-1]["EVENT_TYPE"]
            if(mario_x2 == 0 and type == "stop"):
                print(" can stop")
                return 1
            
            print(" can't stop")
            print(mario_x2)
            return 0    # Mario can't move left
        except:
            print("check_stop error")
            return 0
    def check_slow_down_mid(self):
        try:
            print("=======================Test check_slow_down=======================")
            self.start_game()
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.process.terminate()
            print("terminated")

            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_slow_down_obstacles" :
                    if previous_log:
                        mario_x2 = log["car_speed"]
                        mario_x1 = previous_log["car_speed"]
                        if mario_x2 < mario_x1:
                            print(" can slow down")
                            return 1
                    
                previous_log = log
            print(" can't slow down\n\n")
            print(logs)
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_slow_down error")
            return 0
        

    def check_slow_down_left(self):
        try:
            print("=======================Test check_slow_down=======================")
            self.start_game()
            self.press_key('{LEFT}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.process.terminate()
            print("terminated")

            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_slow_down_obstacles" :
                    if previous_log:
                        mario_x2 = log["car_speed"]
                        mario_x1 = previous_log["car_speed"]
                        if mario_x2 < mario_x1:
                            print(" can slow down")
                            return 1
                    
                previous_log = log
            print(" can't slow down\n\n")
            print(logs)
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_slow_down error")
            return 0
        

    def check_slow_down_left(self):
        try:
            print("=======================Test check_slow_down=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.process.terminate()
            print("terminated")

            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_slow_down_obstacles" :
                    if previous_log:
                        mario_x2 = log["car_speed"]
                        mario_x1 = previous_log["car_speed"]
                        if mario_x2 < mario_x1:
                            print(" can slow down")
                            return 1
                    
                previous_log = log
            print(" can't slow down\n\n")
            print(logs)
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_slow_down error")
            return 0
            
    def check_collide_mid(self): # Check if Mario can move right
        try:
            print("=======================Test check_collide_mid=======================")
            self.start_game()
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            time.sleep(5)
            self.process.terminate()
            print("terminated")


            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_fatal_obstacles" :
                    print(" can collide")
                    return 1
            print(" can't collide")
            
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_collide_mid error")
            return 0
    def check_collide_left(self): # Check if Mario can move right
        try:
            print("=======================Test check_collide_left=======================")
            self.start_game()
            self.press_key('{LEFT}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            time.sleep(5)

            self.process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_fatal_obstacles" :
                    print(" can collide")
                    return 1
            print(" can't collide")
            
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_collide_left error")
            return 0
    def check_collide_right(self): # Check if Mario can move right
        try:
            print("=======================Test check_collide_right=======================")
            self.start_game()
            self.press_key('{RIGHT}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            self.press_key('{UP}')
            time.sleep(5)
            self.process.terminate()
            print("terminated")

            # Read the log
            logs = self.read_log()
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if log["EVENT_TYPE"] == "collide_fatal_obstacles" :
                    print(" can collide")
                    return 1
            print(" can't collide")
            
            print(mario_x2)
            print(mario_x1)
            return 0    # Mario can't move left
        except:
            print("check_collide_right error")
            return 0

    
    def main(self):
        result = {
            'total': 11,
            'total_basic': 6,
            'total_advanced': 5,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'excutability': 0,
                'log': 0,
                'left': 0,
                'right': 0,
                'speed_up': 0,
                'speed_down': 0,
                'over_right': 0,
                'over_left': 0,
                'stop': 0,
                'slow_down': 0,
                'collide': 0,
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
                result['test_cases']['speed_up'] = self.check_speed_up()
            except:
                print("ERROR")
            try:
                result['test_cases']['speed_down'] = self.check_speed_down()
            except:
                print("ERROR")
            try:
                result['test_cases']['over_right'] = self.check_move_overright()
            except:
                print("ERROR")
            try:
                result['test_cases']['over_left'] = self.check_move_overleft()
            except:
                print("ERROR")
            try:
                result['test_cases']['stop'] = self.check_stop()
            except:
                print("ERROR")
            try:
                result['test_cases']['slow_down'] = self.check_slow_down_left()|self.check_slow_down_mid()|self.check_slow_down_right()
            except:
                print("ERROR")
            try:
                result['test_cases']['collide'] = self.check_collide_mid()|self.check_collide_left()|self.check_collide_right()
            except:
                print("ERROR")

        result['basic'] = (
            result['test_cases']['excutability'] +
            result['test_cases']['log'] +
            result['test_cases']['left'] +
            result['test_cases']['right'] +
            result['test_cases']['speed_up'] +
            result['test_cases']['speed_down']
        )
        result['advanced'] = (
            result['test_cases']['over_right'] +
            result['test_cases']['over_left'] +
            result['test_cases']['stop'] +
            result['test_cases']['slow_down'] +
            result['test_cases']['collide']
        )

        return result

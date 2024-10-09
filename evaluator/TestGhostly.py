import os
import time
import subprocess
import json
import pyautogui as pg
import sys


class TestGhostly():

    def __init__(self, checker, py, time=3):
        if not os.path.exists('test'):
            os.makedirs('test')

        self.checker = checker
        self.time = time
        self.py = py

    def tear_down(self):
        self.process.terminate() 

    def read_log(self): # Read game.log, return a list of dictionaries
        with open("game.log", 'r') as file:
            logs = [json.loads(line) for line in file.readlines()]
        return logs

    def clean_log(self): 
        if os.path.exists('game.log'):
            with open("game.log", 'r') as file:
                pass

    # def delete_log(self): # Delete game.log
    #     if os.path.exists("game.log"):
    #         os.remove("game.log")

    def start_game(self): # Start the game
        # self.delete_log() # Delete game.log if it exists
        process = subprocess.Popen(["python", f'{self.py}'])
        time.sleep(0.5)
        return process

    
    def check_Excutablity(self):
        try:
            print("=======================Test Set Up=======================")
            # 启动游戏进程
            process = self.start_game()
            
            # 检查进程是否仍然存活
            if process.poll() is None:
                print("程序正常启动")
                process.terminate()  # 终止进程
                print('check_Excutablity ends process')
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
            print("=======================Test log=======================")
            # 执行一些操作，例如模拟按键（这里假设有一个 start_game 函数）
            process = self.start_game() # 运行游戏
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(1)  # 等待日志记录
            process.terminate()
            # 打开日志文件
            log_file_path = "game.log"
            with open(log_file_path, 'r') as file:
                logs = file.readlines()
            # 检查日志是否为空
            if not logs:
                print("日志文件为空")
                return 0
            for line in logs:
                try:
                    # 替换单引号为双引号，解析为 JSON 对象
                    log_entry = json.loads(line.replace("'", '"'))
                    # 检查必要的字段是否存在
                    required_keys = ["timestamp", "event_type", "move_direction", "ghost_position", "monster_position", "game_status"]
                    for key in required_keys:
                        if key not in log_entry:
                            print(f"缺少字段: {key}")
                            return 0
                    # 检查 event_type 是否在允许的值中
                    valid_event_types = ["eat_pellet", "invalid_move", "eat_other_ghost", "eat_superpellet", "monster_eat_ghost", "ordinary_move"]
                    if log_entry["event_type"] not in valid_event_types:
                        print(f"event_type 值错误: {log_entry['event_type']}")
                        return 0
                    # 检查 move_direction 是否在允许的值中
                    valid_move_directions = ["right", "left", "up", "down"]
                    if log_entry["move_direction"] not in valid_move_directions:
                        print(f"move_direction 值错误: {log_entry['move_direction']}")
                        return 0
                    # 检查 ghost_position 和 monster_position 是否为 [x, y] 格式
                    if not (isinstance(log_entry["ghost_position"], list) and len(log_entry["ghost_position"]) == 2):
                        print(f"ghost_position 格式错误: {log_entry['ghost_position']}")
                        return 0
                    if not (isinstance(log_entry["monster_position"], list) and len(log_entry["monster_position"]) == 2):
                        print(f"monster_position 格式错误: {log_entry['monster_position']}")
                        return 0
                    # 检查 game_status 是否在允许的值中
                    valid_game_statuses = ["ongoing", "win", "lose"]
                    if log_entry["game_status"] not in valid_game_statuses:
                        print(f"game_status 值错误: {log_entry['game_status']}")
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
        
    def check_move_up(self): # Check if Character can move up
        try:
            print("=======================Test up=======================")
            process = self.start_game()
            time.sleep(0.3)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_up = False
            character_y1 = None
            character_y2 = None
            for log in logs:
                if find_move_up:
                    character_y2 = log["ghost_position"][1]
                    if character_y2 < character_y1:
                        print("Character can move up\n\n")
                        return 1    # Character can move up
                # if log["move_direction"] == "up" and find_move_right == False:
                if  find_move_up == False:
                    character_y1 = log["ghost_position"][1]
                    find_move_up = True
            print("Character can't move up\n\n")
            return 0    # Character can't move up
        except:
            print("Move up error")
            return 0
        
    def check_move_down(self): # Check if Character can move down
        try:
            print("=======================Test down=======================")
            process = self.start_game()
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.3)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_down = False
            character_y1 = None
            character_y2 = None
            for log in logs:
                if find_move_down:
                    character_y2 = log["ghost_position"][1]
                    if character_y2 > character_y1:
                        print("Character can move up\n\n")
                        return 1    # Character can move down
                # if log["move_direction"] == "down" and find_move_down == False:
                if find_move_down == False:
                    character_y1 = log["ghost_position"][1]
                    find_move_down = True
            print("Character can't move down\n\n")
            return 0    # Character can't move down
        except:
            print("Move down error")
            return 0
        
    def check_move_left(self): # Check if Character can move left
        try:
            print("=======================Test left=======================")
            process = self.start_game()
            time.sleep(0.3)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('left',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_left = False
            character_x1 = None
            character_x2 = None
            for log in logs:
                if find_move_left:
                    character_x2 = log["ghost_position"][0]
                    if character_x2 < character_x1:
                        print("Character can move left\n\n")
                        return 1    # Character can move right+1
                # if log["move_direction"] == "left" and find_move_left == False:
                if find_move_left == False:
                    character_x1 = log["ghost_position"][0]
                    find_move_left = True
            print("Character can't move left\n\n")
            return 0    # Character can't move right
        except:
            print("Move left error")
            return 0
        
    def check_move_right(self): # Check if Character can move right
        try:
            print("=======================Test right=======================")
            process = self.start_game()
            time.sleep(0.3)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.3)
            pg.press('right',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            find_move_right = False
            character_x1 = None
            character_x2 = None
            for log in logs:
                if find_move_right:
                    character_x2 = log["ghost_position"][0]
                    if character_x2 > character_x1:
                        print("Character can move right\n\n")
                        return 1    # Character can move right
                # if log["move_direction"] == "right" and find_move_right == False:
                if  find_move_right == False:
                    character_x1 = log["ghost_position"][0]
                    find_move_right = True
            print("Character can't move right\n\n")
            return 0    # Character can't move right
        except:
            print("Move right error")
            return 0

    def check_activate(self): # Check if Character can move right
        try:
            print("=======================Test activate=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            monster_pos=logs[-1]["monster_position"]
            if monster_pos[0]!=-1:
                print("Monster can activate\n\n")
                return 1
            print("Monster can not activate\n\n")
            return 0   
        except:
            print("Monster activate error")
            return 0
        
    def check_wall(self): # Check if Character can move through wall
        try:
            print("=======================Test wall=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            event=logs[-1]["event_type"]
            if event=="invalid_move":
                print("Character can not walk through wall\n\n")
                return 1
            print("Character can walk through wall\n\n")
            return 0    
        except:
            print("walk through wall error")
            return 0
        
    def check_invalid_eat(self):
        try:
            print("=======================Test invalid_eat=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            monster_pos=logs[-1]["event_type"]
            if monster_pos=="invalid_move":
                print("Character can not eat because no superpellet\n\n")
                return 1
            print("Character can eat without superpellet\n\n")
            return 0    
        except:
            print("Invalid_eat error")
            return 0
        
    def check_eat_other(self): # Check if Character can eat others with superpellet
        try:
            print("=======================Test eat other=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            # pg.press('left',presses=1,interval=0)
            # time.sleep(0.1)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            cnt=0
            for log in logs:
                if log["event_type"]=="eat_other_ghost":
                    cnt+=1
            if cnt==2:
                print("Character can eat other wiht superpellet\n\n")
                return 1
            print("Character can eat other wiht superpellet\n\n")
            return 0    
        except:
            print("eat_other error")
            return 0
        
    def check_monster_eat_ghost(self):
        try:
            print("=======================Test monster eat ghost=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('up',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.5)
            pg.press('up',presses=1,interval=0)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            monster_pos=logs[-1]["game_status"]
            if monster_pos=="lose":
                print("Character can be eaten by monster\n\n")
                return 1
            print("Character can not be eaten by monster\n\n")
            return 0    
        except:
            print("check_monster_eat_ghost")
            return 0
    def check_win_eat_pellet(self): # Check if Character can win by eating all pellet
        try:
            print("=======================Test eat pellet=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            state=logs[-1]["game_status"]
            if state=="win":
                print("can win by eating all pellets")
                return 1
            print("can not win by eating all pellets")
            return 0
        except:
            print("win_eat_pellet error")
            return 0
    def check_win_eat_other(self): # Check if Character can win by eating all ghosts
        try:
            print("=======================Test eat other=======================")
            process = self.start_game()
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('right',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('down',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            pg.press('left',presses=1,interval=0)
            time.sleep(0.1)
            process.terminate()
            print("terminated")
            # Read the log
            logs = self.read_log()
            print(logs)
            state=logs[-1]["game_status"]
            if state=="win":
                print("Character can win by eat all other ghosts")
                return 1
            print("Character can not win by eat all other ghosts")
            return 0
        except:
            print("win_eat_other error")
            return 0


    def main(self):
        result = {
            'total': 13,
            'total_basic': 6,
            'total_advanced': 7,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'excutability': 0,
                'log': 0,
                'left': 0,
                'right': 0,
                'up': 0,
                'down': 0,
                'activate': 0,
                'wall': 0,
                'invalid_eat': 0,
                'eat_other': 0,
                'monster_eat_ghost': 0,
                'win_eat_pellet': 0,
                'win_eat_other': 0, 
            }
        }
        try:
            result['test_cases']['excutability'] = self.check_Excutablity()
            # result['test_cases']['excutability'] = self.test_set_up()
            self.clean_log()
        except:
            self.tear_down()

        if result['test_cases']['excutability'] == 1:
            try :
                result['test_cases']['log'] = self.check_log()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['up'] = self.check_move_up()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['down'] = self.check_move_down()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['left'] = self.check_move_left()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['right'] = self.check_move_right()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['activate'] = self.check_activate()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['wall'] = self.check_wall()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['invalid_eat'] = self.check_invalid_eat()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['eat_other'] = self.check_eat_other()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['monster_eat_ghost'] = self.check_monster_eat_ghost()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['win_eat_pellet'] = self.check_win_eat_pellet()
                self.clean_log()
            except:
                print("ERROR")
            try :
                result['test_cases']['win_eat_other'] = self.check_win_eat_other()
                self.clean_log()
            except:
                print("ERROR")
        result['basic'] = result['test_cases']['excutability'] + result['test_cases']['log'] + result['test_cases']['up'] + result['test_cases']['down'] + result['test_cases']['left'] + result['test_cases']['right']
        result['advanced'] = result['test_cases']['activate'] + result['test_cases']['wall'] + result['test_cases']['invalid_eat'] + result['test_cases']['eat_other'] + result['test_cases']['monster_eat_ghost'] + result['test_cases']['win_eat_pellet'] + result['test_cases']['win_eat_other']
        
        return result
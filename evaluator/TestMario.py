import os
import time
import subprocess
import json
import pyautogui as pg
import pygetwindow as gw

def read_log(): # Read game.log, return a list of dictionaries
    retry_count = 2
    while retry_count > 0:
        try:
            with open("game.log", 'r') as file:
                logs = [json.loads(line.replace("'", "\"")) for line in file.readlines()]
            return logs
        except IOError as e:
            retry_count -= 1
            time.sleep(0.5)
            if retry_count == 0:
                raise e

def delete_log(): # Delete game.log
    retry_count = 2
    while retry_count > 0:
        try:
            if os.path.exists("game.log"):
                os.remove("game.log")
            break
        except IOError as e:
            retry_count -= 1
            time.sleep(0.5)
            if retry_count == 0:
                raise e

def is_game_over(process): # Check if the game is over
    return process.poll() != None

def get_new_window(old_windows):
    new_windows = gw.getAllWindows()
    for window in new_windows:
        if window not in old_windows and window.title:
            return window
    return None

class TestMario():  

    def __init__(self, checker, py, time=3):
        if not os.path.exists("test"):
            os.makedirs("test")
        
        self.checker = checker
        self.time = time
        self.py = py
        
        self.total_test = 18

    def start_game(self): # Start the game
        delete_log() # Delete game.log if it exists
        process = subprocess.Popen(["python", f"{self.py}"])
        time.sleep(0)
        old_windows = gw.getAllWindows()
        game_window = None
        while game_window == None:
            game_window = get_new_window(old_windows)
            if game_window != None:
                print(f"Game window activated: {game_window.title}")
            else:
                time.sleep(0.1)
        return process
    
    def key_press(self,key):
        pg.press(key, interval=0)
        
    def check_excutability(self):
        try:
            process = self.start_game()
            if is_game_over(process):
                return 0
            else:
                return 1
        except Exception as e:
            print("Check excutability error:", e)
            return 0
    
    def check_move_left(self): # Check if Mario can move right
        print("=======================Test Move Left=======================")
        try:
            process = self.start_game()
            left_move_count = 0
            while True:
                self.key_press('left')
                time.sleep(0.05)
                left_move_count += 1   
                if left_move_count > 10:
                    break
            self.key_press('right')
            time.sleep(0.05)
        except Exception as e:
            print("EXECUTE ERROR:", e)
            pass

        process.terminate()
        time.sleep(1)

        try:
            # Read the log
            logs = read_log()
            find_move_left = False
            mario_x1 = None
            mario_x2 = None
            for log in logs:
                if find_move_left:
                    mario_x2 = log["mario_position"][0]
                    if mario_x2 < mario_x1:
                        print("1")
                        return 1    # Mario can move left
                    print("0")
                    return 0
                if log["EVENT_TYPE"] == "MOVE_LEFT" and find_move_left == False:
                    mario_x1 = log["mario_position"][0]
                    find_move_left = True
            print("0")
            return 0    # Mario can't move left
        except Exception as e:
            print("ERROR:", e)
            return 0

    def check_move_right(self, score_move_left): # Check if Mario can move right. If move_left is not working, check move_left again
        print("=======================Test Move Right=======================")
        try:
            process = self.start_game() # Run the game
            right_move_count = 0
            while True:
                self.key_press('right')
                time.sleep(0.05)
                right_move_count += 1
                if right_move_count > 10:
                    break
            try:
                if score_move_left == 0:
                    left_move_count = 0
                    while True:     # Check move left if check_move_left is not working
                        self.key_press('left')
                        time.sleep(0.05)
                        left_move_count += 1
                        if left_move_count > 8:
                            break
                    try:
                        self.key_press('right')
                    except:
                        pass
                else:
                    self.key_press('left')
            except Exception as e:
                print("EXECUTE ERROR:", e)
        except Exception as e:
            print("EXECUTE ERROR:", e)
        
        try:
            process.terminate()
            time.sleep(1)

            # Read the log
            logs = read_log()
            find_move_right = False
            mario_x1 = None
            mario_x2 = None
            score = [0,0]
            for log in logs: # Check if Mario can move right
                if find_move_right:
                    mario_x2 = log["mario_position"][0]
                    if mario_x2 > mario_x1:
                        score[0] = 1    # Mario can move right
                        break
                if log["EVENT_TYPE"] == "MOVE_RIGHT" and find_move_right == False:
                    mario_x1 = log["mario_position"][0]
                    find_move_right = True
            if score_move_left == 0:
                find_move_left = False
                mario_x1 = None
                mario_x2 = None
                for log in logs: # Check if Mario can move left
                    if find_move_left:
                        mario_x2 = log["mario_position"][0]
                        if mario_x2 < mario_x1:
                            print("Move Left: SUCCESS")
                            score[1] = 1    # Mario can move left
                            break
                    if log["EVENT_TYPE"] == "MOVE_LEFT" and find_move_left == False:
                        mario_x1 = log["mario_position"][0]
                        find_move_left = True
            print("Move Right: ", score[0])
            print("Move Left:", score[1]) 
            return score
        except Exception as e:
            print("ERROR:", e)
            return [0,0]
    
    def check_case1(self):
        def check_block_position(logs):
            print("=======================Test Block Position=======================")
            try:
                first_log = logs[0]
                brick_position = first_log["block_position"]
                mario_position = first_log["mario_position"]
                if mario_position[0] <= brick_position[0]+10 and mario_position[0] >= brick_position[0]-10 and mario_position[1] > brick_position[1]+10:
                    pass
                else:
                    print("0")
                    return 0
                for log in logs:
                    if log["block_position"] != brick_position:
                        print("0")
                        return 0
                print("1")
                return 1
            except Exception as e:
                print("ERROR:", e)
                return 0
        def check_block_hit(logs):
            print("=======================Test Block Hit=======================")
            try:
                result = [1,0,0]
                find_block = False
                for i in range(len(logs)):
                    if find_block == False:
                        if logs[i]["EVENT_TYPE"] == "HIT_BLOCK":
                            find_block = True
                            try:
                                first_log = logs[i-1]
                            except:
                                first_log = logs[i]
                            third_log = logs[i+1]
                            if first_log["score"] +100 <= third_log["score"]:
                                result[1] = 1 # 2. Check score increase after block hit
                            if result[0] == 1:
                                if logs[i+2]["block_position"] != [None, None] and logs[i+2]["block_position"] != ["null","null"]:
                                    result[2] = 1 # 3. Check mushroom appear after block hit
                            break
                        else:
                            if logs[i]["mushroom_position"] != [None, None] and logs[i]["mushroom_position"] != ["null","null"]:
                                result[0] = 0 # 1. Check mushroom initial state
                print("Mushroom initial position: ", result[0])
                print("Block collision score: ", result[1])
                print("Mushroom appear after block hit: ", result[2])
                return result
            except Exception as e:
                print("ERROR:", e)
                return [0,0,0]
            
        def check_mushroom(logs):
            print(print("=======================Test Mushroom======================="))
            try:
                result = [0,0,0,0,0]
                ground_count = 0
                right_move_count = 0
                left_move_count = 0
                right_move = True
                left_move = False
                last_position = None
                find_mushroom = False
                for i in range(len(logs)):
                    if logs[i]["mushroom_position"] != [None, None] and logs[i]["mushroom_position"] != ["null","null"]:
                        try: # 1. Check mushroom move on the ground
                            if ground_count < 6 and logs[i]["mushroom_position"][1] == logs[i]["mario_position"][1]:
                                ground_count += 1
                            if ground_count >= 5:
                                result[0] = 1
                        except Exception as e:
                            print("Check Mushroom move on ground error:", e)
                            result[0] = 0
                        try: # 2. Check mushroom move
                            try:
                                if right_move:
                                    if last_position == None:
                                        last_position = logs[i]["mushroom_position"][0]
                                        right_move_count += 1
                                    else:
                                        if logs[i]["mushroom_position"][0] < last_position:
                                            right_move = False
                                            left_move = True
                                        else:
                                            last_position = logs[i]["mushroom_position"][0]
                                            right_move_count += 1
                                    if right_move_count >= 5:
                                        result[1] = 1
                            except Exception as e:
                                print("Check Mushroom move right error:", e)
                            try:
                                if left_move:
                                    if logs[i]["mushroom_position"][0] <= last_position:
                                        last_position = logs[i]["mushroom_position"][0]
                                        left_move_count += 1
                                    if left_move_count >= 5:
                                        result[2] = 1
                            except Exception as e:
                                print("Check Mushroom bounce back:", e)
                        except Exception as e:
                            print("Check Mushroom move error:", e)
                            result[1] = 0
                            result[2] = 0
                    try: # 3. Check mushroom states after hit by Mario
                        if find_mushroom:
                            if logs[i]["mushroom_position"] == [None, None] or logs[i]["mushroom_position"] == ["null","null"]:
                                result[3] = 1
                        if logs[i]["EVENT_TYPE"] == "TOUCH_MUSHROOM":
                            find_mushroom = True
                            first_score = logs[i-1]["score"]
                            third_score = logs[i+1]["score"]
                            if first_score + 1000 <= third_score:
                                result[4] = 1
                    except Exception as e:
                        print("Check Mushroom touched and states after it error:", e)
                        result[3] = 0
                        result[4] = 0
                if result[1] == 1 and result[2] == 1:
                    mushroom_movement = 1
                else:
                    mushroom_movement = 0
                print("Mushroom move on ground: ", result[0])
                print("Mushroom movement pattern: ",mushroom_movement)
                print("Mushroom disappear after hit by Mario: ", result[3])
                print("Mushroom collision score: ", result[4])
                return result
            except Exception as e:
                print("ERROR:", e)
                return [0,0,0,0,0] 

        print("=======================Test Case 1=======================")
        try:
            try:
                process = self.start_game()  
                count = 0
                time.sleep(0.05)
                self.key_press('up')
                self.key_press('up')
                while True:
                    self.key_press('right')
                    time.sleep(0.05)
                    count+=1
                    self.key_press('left')
                    time.sleep(0.05)
                    count+=1
                    if count > 200 or is_game_over(process):
                        break   
            except Exception as e:
                print("EXECUTE ERROR:", e)
                pass

            process.terminate()
            time.sleep(1)
            logs = read_log()

            score_block_position = check_block_position(logs)
            result_block_hit = check_block_hit(logs)
            score_mushroom_initial_state = result_block_hit[0]
            score_block_score = result_block_hit[1]
            score_mushroom_apear = result_block_hit[2]
            result_mushroom = check_mushroom(logs)
            score_mushroom_move_ground = result_mushroom[0]
            score_mushroom_move_right = result_mushroom[1]
            score_mushroom_move_left = result_mushroom[2]
            score_mushroom_touched = result_mushroom[3]
            score_mushroom_score = result_mushroom[4]
            return score_block_position, score_mushroom_initial_state, score_block_score, score_mushroom_apear, score_mushroom_move_ground, score_mushroom_move_right, score_mushroom_move_left, score_mushroom_touched, score_mushroom_score
        except Exception as e:
            print("ERROR:", e)
            return 0,0,0,0,0,0,0,0,0
            

        
    def check_jump(self): # Check if Mario can jump and land on ground
        print("=======================Test Jump=======================")
        try: 
            try:
                process = self.start_game()
                count = 0
                while True:
                    self.key_press('right')
                    count += 1
                    time.sleep(0.005)
                    if count > 35:
                        break
                count = 0
                while True:
                    self.key_press('up')
                    count +=1
                    time.sleep(0.001)
                    if count > 20:
                        break
                count = 0
                while True:
                    self.key_press('right')
                    count += 1
                    time.sleep(0.5)
                    if count > 20 or is_game_over(process):
                        break
            except Exception as e:
                print("EXECUTE ERROR:", e)
                pass

            process.terminate()
            time.sleep(1)

            # Read the log
            logs = read_log()
            score = [0,0]
            find_jump = False
            mario_y1 = None
            mario_y2 = None
            mario_y3 = None
            for log in logs:
                if find_jump:
                    mario_y2 = log["mario_position"][1]
                    if mario_y2 < mario_y1:
                        score[0] = 1    # Mario can jump
                        break
                if log["EVENT_TYPE"] == "JUMP" and find_jump == False:
                    mario_y1 = log["mario_position"][1]
                    find_jump = True
            if score[0] == 1:
                mario_y3 = logs[-1]["mario_position"][1]
                if mario_y3 == mario_y1:
                    score[1] = 1    # Mario can land on ground
            print("Mario Jump: ", score[0])
            print("Mario Land on Ground after Jump: ", score[1])
            return score
        except Exception as e:
            print("ERROR:", e)
            return [0,0]

    def check_enemy(self):
        def check_enemy_random_move(logs):
            print("=======================Test Enemy Random Move=======================")
            try:
                count = 0
                initial_position = logs[0]["enemy_position"]
                for log in logs:
                    if log["enemy_position"] != initial_position:
                        count +=1
                if count >=5:
                    print("SUCCESS")
                    return 1
                else:
                    print("FAIL")
                    return 0
            except Exception as e:
                print("ERROR:", e)
                return 0
        
        def check_y(logs):
            print("=======================Test Move on Ground=======================")
            try:
                score = [1,1,1]
                mario_y = logs[0]["mario_position"][1]
                enemy_y = logs[0]["enemy_position"][1]
                if mario_y <= 0:
                    score[0] = 0
                if enemy_y <= 0:
                    score[1] = 0 
                for log in logs:
                    if log["enemy_position"][1] != enemy_y:
                        score[1] = 0
                    if log["enemy_position"][1] != mario_y:
                        score[2] = 0
                    enemy_y = log["enemy_position"][1]
                
                if score == [1,1,1]:
                    print("1")
                else:
                    print("0")
                return score
            except Exception as e:
                print("ERROR:", e)
                return [0,0,0]
        
        def check_enemy_collision(logs):
            print("=======================Test Enemy Collision=======================")
            try:
                if logs[-1]["EVENT_TYPE"] == "COLLIDE_ENEMY":
                    print("1")
                    return 1
                print("0")
                return 0
            except Exception as e:
                print("ERROR:", e)
                return 0

        print("=======================Test Case 2=======================")
        try:   
            process = self.start_game()
            # go left until game ends
            count_time = 0
            while True:
                self.key_press('right')
                count_time += 1
                time.sleep(0.05)
                self.key_press('left')
                count_time +=1
                time.sleep(0.05)
                self.key_press('right')
                count_time +=1
                time.sleep(0.05)
                if count_time > 200 or is_game_over(process):
                    break
        except Exception as e:
            print("EXECUTE ERROR:", e)
            pass

        process.terminate()
        time.sleep(1)
        logs = read_log()
        
        y_list = check_y(logs)
        if y_list == [1,1,1]:
            ys= 1
        else:
            ys= 0

        return [check_enemy_random_move(logs), ys, check_enemy_collision(logs)]
    
    def check_flag(self):
        print("=======================Test Flag=======================")
        try:
            process = self.start_game()
            count = 0
            while True:
                self.key_press('down')
                count += 1
                time.sleep(0.1)
                if count > 5 or is_game_over(process):
                    break
            count = 0
            while True:
                self.key_press('right')
                time.sleep(0.05)
                count += 1
                if count > 10 or is_game_over(process):
                    break
            # go right until game ends
            count_time = 0
            while True:
                for i in range(6):
                    self.key_press('right')
                    time.sleep(0.01)
                    count_time += 1
                self.key_press('left')
                time.sleep(0.01)
                count_time +=1
                if count_time > 1000 or is_game_over(process):
                    break
        except Exception as e:
            print("EXECUTE ERROR:", e)
            pass

        process.terminate()
        time.sleep(1)
        logs = read_log()
        enemy_eliminated = False
        score = [0,0]
        for log in logs:
            if enemy_eliminated:
                if log["enemy_position"] == [None, None] or log["enemy_position"] == ["null", "null"]:
                    score[0] = 1
                    break
            if log["EVENT_TYPE"] == "ELIMINATE_ENEMY":
                enemy_eliminated = True
        if logs[-1]["EVENT_TYPE"] == "REACH_FLAG":
            score[1] = 1
        print("Enemy Eliminated: ", score[0])
        print("Mario Reach Flag: ", score[1])
        return score
    
    def check_score(self):
        print("=======================Test Score Counts=======================")
        try:
            try:
                process = self.start_game()
                count_time = 0
                while True:
                    self.key_press('right')
                    count_time += 1
                    time.sleep(0.05)
                    self.key_press('left')
                    count_time += 1
                    if count_time > 100 or is_game_over(process):
                        break
                process.terminate()
                time.sleep(1)
            except Exception as e:
                print("EXECUTE ERROR:", e)

            logs = read_log()
            for i in range(len(logs)):
                if logs[i]["EVENT_TYPE"] == "MOVE_RIGHT":
                    if logs[i+1]["EVENT_TYPE"] == "MOVE_LEFT" and logs[i+1]["score"] == logs[i]["score"] + 1:
                        print("1")
                        return 1
                elif logs[i]["EVENT_TYPE"] == "MOVE_LEFT":
                    if logs[i+1]["EVENT_TYPE"] == "MOVE_RIGHT" and logs[i+1]["score"] == logs[i]["score"] + 1:
                        print("1")
                        return 1
                elif logs[i+1]["score"] == logs[i]["score"] + 1:
                    print("1")
                    return 1
            print("0")
            return 0
        except Exception as e:
            print("ERROR:", e)
            return 0
            
    def main(self):
        result = {
            'total': 18,
            'total_basic': 9,
            'total_advanced': 9,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'move_left': 0,
                'move_right': 0,
                'jump': 0,
                'land_on_ground': 0,
                'move_on_ground': 0,
                'enemy_random_move': 0,
                'block_position': 0,
                'score_counts_time': 0,
                'mushroom_initial_state': 0,
                'enemy_collision': 0,
                'enemy_eliminate': 0,
                'reach_flag': 0,
                'block_score': 0,
                'mushroom_appear': 0,
                'mushroom_move_ground': 0,
                'mushroom_movement': 0,
                'mushroom_disappear': 0,
                'mushroom_score': 0
            }
        } 

        score_move_left = self.check_move_left() # window 1
        movement = self.check_move_right(score_move_left) # window 2
        if score_move_left == 0:
            score_move_left = movement[1]
        score_move_right = movement[0]
        score_jump = self.check_jump() # window 3
        score_enemy = self.check_enemy() # window 4
        flag = self.check_flag() # window 5
        score_enemy_eliminate = flag[0]
        score_reach_flag = flag[1]
        score_block_position, score_mushroom_initial_state, score_block_score, score_mushroom_apear, score_mushroom_move_ground, score_mushroom_move_right, score_mushroom_move_left, score_mushroom_touched, score_mushroom_score = self.check_case1() # window 6
        score_score_counts = self.check_score() # window 7

        if score_mushroom_move_right == 1 and score_mushroom_move_left == 1:
            score_mushroom_movement = 1
        else:
            score_mushroom_movement = 0

        result['test_cases']['move_left'] = score_move_left
        result['test_cases']['move_right'] = score_move_right
        result['test_cases']['jump'] = score_jump[0]
        result['test_cases']['land_on_ground'] = score_jump[1]
        result['test_cases']['move_on_ground'] = score_enemy[1]
        result['test_cases']['enemy_random_move'] = score_enemy[0]
        result['test_cases']['block_position'] = score_block_position
        result['test_cases']['score_counts_time'] = score_score_counts
        result['test_cases']['mushroom_initial_state'] = score_mushroom_initial_state
        result['test_cases']['enemy_collision'] = score_enemy[2]
        result['test_cases']['enemy_eliminate'] = score_enemy_eliminate
        result['test_cases']['reach_flag'] = score_reach_flag
        result['test_cases']['block_score'] = score_block_score
        result['test_cases']['mushroom_appear'] = score_mushroom_apear
        result['test_cases']['mushroom_move_ground'] = score_mushroom_move_ground
        result['test_cases']['mushroom_movement'] = score_mushroom_movement
        result['test_cases']['mushroom_disappear'] = score_mushroom_touched
        result['test_cases']['mushroom_score'] = score_mushroom_score
        
        result['basic'] = result['test_cases']['move_left'] + result['test_cases']['move_right'] + result['test_cases']['jump'] + result['test_cases']['land_on_ground'] + result['test_cases']['move_on_ground'] + result['test_cases']['enemy_random_move'] + result['test_cases']['block_position'] + result['test_cases']['score_counts_time'] + result['test_cases']['mushroom_initial_state']
        result['advanced'] = result['test_cases']['enemy_collision'] + result['test_cases']['enemy_eliminate'] + result['test_cases']['reach_flag'] + result['test_cases']['block_score'] + result['test_cases']['mushroom_appear'] + result['test_cases']['mushroom_move_ground'] + result['test_cases']['mushroom_movement'] + result['test_cases']['mushroom_disappear'] + result['test_cases']['mushroom_score']
        
        return result


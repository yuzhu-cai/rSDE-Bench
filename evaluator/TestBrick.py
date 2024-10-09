import os
import time
import subprocess
import json
import pyautogui as pg
import pygetwindow as gw

def read_log(): # Read game.log, return a list of dictionaries
    with open("game.log", 'r') as file:
        logs = [json.loads(line.replace("'", "\"")) for line in file.readlines()]
    return logs

def delete_log(): # Delete game.log
    if os.path.exists("game.log"):
        os.remove("game.log")

def is_game_over(process): # Check if the game is over
    return process.poll() != None

def get_new_window(old_windows):
    new_windows = gw.getAllWindows()
    for window in new_windows:
        if window not in old_windows and window.title:
            return window
    return None

class TestBrick():

    def __init__(self, checker, py, time = 3):
        if not os.path.exists("test"):
            os.makedirs("test")
        
        self.checker = checker
        self.time = time
        self.py = py
        
        self.total_test = 14

    def start_game(self, n): # Start the game
        delete_log() # Delete game.log if it exists
        process = subprocess.Popen(["python", f"{self.py}"])
        time.sleep(0)
        old_windows = gw.getAllWindows()
        game_window = None
        while game_window is None:
            game_window = get_new_window(old_windows)
            if game_window is not None:
                print(f"Game window activated: {game_window.title}")
            else:
                time.sleep(0.1)
        return process
    
    def key_press(self, key):
        pg.press(key, interval=0)
    
    def check_executable(self): # check whether the game is executable
        try: 
            process = self.start_game(0)
            process_running = process.poll() is None
            process.terminate()
            if process_running:
                return True
            else:
                return False
        except:
            return False
    
    def check_move_left(self): # check whether the paddle can move left, and whether the paddle does not move up or down
        print("=======================Test Move Left=======================")
        try:
            process = self.start_game(0.5)
            left_move_count = 0
            while True:
                self.key_press('left')
                left_move_count += 1
                if left_move_count > 10:
                    break
            self.key_press('right')
            time.sleep(0.5)
        except Exception as e:
            print("EXECUTE ERROR:", e)
        finally:
            if process is not None:
                process.terminate()
        time.sleep(1)

        try:
            # Read the log
            logs = read_log()
            result = [0,0]
            find_move_left = False
            paddle_x1 = None
            paddle_x2 = None
            paddle_y1 = None
            paddle_y2 = None
            for log in logs:
                if find_move_left:
                    paddle_x2 = log["paddle_position"][0]
                    paddle_y2 = log["paddle_position"][1]
                    if paddle_x2 < paddle_x1:
                        result[0] = 1 # The paddle can move left
                    if paddle_y2 == paddle_y1:
                        result[1] = 1 # The paddle does not move up or down
                    return result
                if log["EVENT_TYPE"] == "PADDLE_MOVE_LEFT":
                    find_move_left = True
                    paddle_x1 = log["paddle_position"][0]
                    paddle_y1 = log["paddle_position"][1]
            print("Move left:", result[0])
            print("Vertically stable:", result[1])
            return result
        except Exception as e:
            print("ERROR:", e)
            return [0,0]
    
    def check_move_right(self,result_move_left): # Check if paddle can move right. If move_left is not working, check move_left again
        print("=======================Test Move Right=======================")
        result = [0]
        result.append(result_move_left[0])
        result.append(result_move_left[1])
        try:
            process = self.start_game(1) # Run the game
            right_move_count = 0
            while True:
                self.key_press('right')
                right_move_count += 1
                if right_move_count > 10:
                    break
            try: 
                if result[1] == 0: # If move left is not working
                    left_move_count = 0 
                    while True:     # Check move left if check_move_left is not working
                        self.key_press('left')
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
                print(f"An error occurred while checking move left again: {e}")
        except:
            pass

        time.sleep(0.5)
        process.terminate()
        time.sleep(1)

        # Read the log
        try:
            logs = read_log()
            find_move_right = False
            paddle_x1 = None
            paddle_x2 = None
            paddle_y1 = None
            paddle_y2 = None
            for log in logs: # Check if Paddle can move right
                if find_move_right:
                    paddle_x2 = log["paddle_position"][0]
                    paddle_y2 = log["paddle_position"][1]
                    if paddle_x2 > paddle_x1:
                        result[0] = 1    # Paddle can move right
                    if paddle_y2 != paddle_y1 and result[2] == 1:
                        result[2] = 0  # Paddle move up or down
                    break
                if log["EVENT_TYPE"] == "PADDLE_MOVE_RIGHT" and find_move_right == False:
                    paddle_x1 = log["paddle_position"][0]
                    paddle_y1 = log["paddle_position"][1]
                    find_move_right = True
            if  result[1] == 0:
                find_move_left = False
                paddle_x1 = None
                paddle_x2 = None
                for log in logs: # Check if Paddle can move left
                    if find_move_left:
                        paddle_x2 = log["paddle_position"][0]
                        if paddle_x2 < paddle_x1:
                            result[1] = 1    # Paddle can move left
                            break
                    if log["EVENT_TYPE"] == "PADDLE_MOVE_LEFT" and find_move_left == False:
                        paddle_x1 = log["paddle_position"][0]
                        find_move_left = True
            print("Move right:", result[0])
            print("Move left:", result[1])
            print("Vertically stable:", result[2])
            return result
        except Exception as e:
            print("ERROR:", e)
            return [0,0,0]
    
    def test_velocity(self):
        def check_velocity(key): # Check the velocity for a specific key press
            try:
                process = self.start_game(1)
                self.key_press(key)
                time.sleep(0.05)  # Allow some time for the log to capture the event
                self.key_press(key)
                time.sleep(0.05)
            except:
                pass

            process.terminate()
            time.sleep(1)

            try:
                logs = read_log()
                initial_position = None
                final_position = None
                distance = None
                for log in logs:
                    if initial_position is None and log["EVENT_TYPE"] == f"PADDLE_MOVE_{key.upper()}":
                        initial_position = log["paddle_position"][0]
                    elif initial_position is not None and log["EVENT_TYPE"] == f"PADDLE_MOVE_{key.upper()}":
                        final_position = log["paddle_position"][0]
                        break

                if initial_position is not None and final_position is not None:
                    distance = abs(final_position - initial_position)
                elif final_position is None:
                    final_position = logs[-1]["paddle_position"][0]
                    if final_position != initial_position:
                        distance = abs(final_position - initial_position)
                else:
                    distance = None
                return distance
            except:
                return None

        velocity = check_velocity("Right")
        if velocity is None:
            velocity = check_velocity("Left")
        return velocity


    def check_case1(self):
        score_brick_bounce = 0
        score_brick_split_success = 0
        score_brick_split_height = 0
        score_brick_life = 0
        score_brick_split_fit = 0
        score_wall_bounce = 0
        score_paddle_bounce = 0

        def check_ball_initial_state(logs):
            print("=======================Test Ball Initial State=======================")
            try:
                result = [0,0]
                first_log = logs[0]
                ball_y1 = first_log["ball_position"][1]
                paddle_y = first_log["paddle_position"][1]
                brick_y = first_log["bricks_info"][0][1]
                for i in range(len(first_log["bricks_info"])):
                    if first_log["bricks_info"][i][1] > brick_y:
                        brick_y = first_log["bricks_info"][i][1]

                if ball_y1 < paddle_y and ball_y1 > brick_y:
                    result[0] = 1 # Ball is in the middle of the paddle and bricks
                
                second_log = logs[1]
                ball_y2 = second_log["ball_position"][1]
                third_log = logs[2]
                ball_y3 = third_log["ball_position"][1]
                if ball_y1 > ball_y2 or ball_y1 > ball_y3:
                    result[1] = 1 # Ball is moving Up
                print("Ball initial position:", result[0])
                print("Ball initial move:", result[1])
                return result
            except Exception as e:
                print("ERROR:", e)
                return [0,0]
        
        def check_ball_in_range(logs):
            print("=======================Test Ball In Range=======================")
            result = 1
            for log in logs:
                if log["ball_position"][1] <= -5:
                    result = 0
                    break
            print(result)
            return result
        
        def check_ball_lost(logs):
            print("=======================Test Ball Lost=======================")
            last_log = logs[-1]
            if last_log["EVENT_TYPE"] == "BALL_LOST" and last_log["ball_position"][1] > logs[-2]["ball_position"][1]:
                print("1")
                return 1
            else:
                print("0")
                return 0
        
        def check_paddle_bounce(logs):
            def test_bounce_paddle(index):
                try:
                    log1 = logs[index-1]
                    log2 = logs[index]
                    log3 = logs[index+1]
                    if log1["ball_position"][1] < log2["ball_position"][1] and log3["ball_position"][1] < log2["ball_position"][1]:
                        if log2["ball_position"][0] >= log1["ball_position"][0] and log2["ball_position"][0] <= log3["ball_position"][0]:
                            return True
                        elif log2["ball_position"][0] <= log1["ball_position"][0] and log2["ball_position"][0] >= log3["ball_position"][0]:
                            return True
                    return False
                except:
                    return False

            print("=======================Test Paddle Bounce=======================")
            try:
                result = 0
                find_paddle = False
                for i in range(len(logs)):
                    log = logs[i]
                    if log["EVENT_TYPE"] == "BOUNCE_PADDLE":
                        find_paddle = True
                        if test_bounce_paddle(i):
                            result = 1
                            break
                print(result)
                print("Find paddle:", find_paddle)
                return result, find_paddle
            except Exception as e:
                print("ERROR:",e)
                return 0, False
                    
        def check_ball_bounce(logs):
            print("=======================Test Ball Bounce=======================")
            try:
                result = [0,0,0,0,0,0,0,0]
                find_brick = False
                find_wall = False
                first_log = logs[0]
                brick_log = None
                for index in range(len(logs)):
                    log = logs[index]
                    if find_brick:
                        if brick_log["ball_position"][0] >= first_log["ball_position"][0] and log["ball_position"][0] >= brick_log["ball_position"][0]:
                            if (brick_log["ball_position"][1] >= first_log["ball_position"][1] and log["ball_position"][1] <= brick_log["ball_position"][1]) or (brick_log["ball_position"][1] <= first_log["ball_position"][1] and log["ball_position"][1] >= brick_log["ball_position"][1]):
                                result[0] = 1 # Ball is bouncing on the brick
                        elif brick_log["ball_position"][0] <= first_log["ball_position"][0] and log["ball_position"][0] <= brick_log["ball_position"][0]:
                            if (brick_log["ball_position"][1] >= first_log["ball_position"][1] and log["ball_position"][1] <= brick_log["ball_position"][1]) or (brick_log["ball_position"][1] <= first_log["ball_position"][1] and log["ball_position"][1] >= brick_log["ball_position"][1]):
                                result[0] = 1 # Ball is bouncing on the brick

                        for i in range(len(first_log["bricks_info"])):
                            try:
                                if first_log["bricks_info"][i] != brick_log["bricks_info"][i]:
                                    b1 = first_log["bricks_info"][i]
                                    b2 = brick_log["bricks_info"][i]
                                    if len(b2) == 2:
                                        result[1] = 1 # Brick split into two
                                        if b2[0][1] == b2[1][1] and b2[0][1] == b1[1]:
                                            result[2] = 1 # Two bricks are at the same level of the original brick
                                        if b2[0][2] == b2[1][2] and b2[0][2] == b1[2] - 1:
                                            result[3] = 1 # Two bricks's life is one less than the original brick
                                        if b2[0][0] + b2[1][0] == 2*b1[0]:
                                            result[4] = 1 # Two bricks fit the original brick
                                        
                                    elif len(b2) == 3 and b2[2] == b1[2] - 1:
                                        result[3] = 1 # Brick life is one less than the original brick
                                    break
                            except:
                                pass
                        find_brick = False

                    if find_wall:
                        if brick_log["ball_position"][0] >= first_log["ball_position"][0] and log["ball_position"][0] <= brick_log["ball_position"][0]:
                            result[5] = 1 # Ball is bouncing on the wall
                        elif brick_log["ball_position"][0] <= first_log["ball_position"][0] and log["ball_position"][0] >= brick_log["ball_position"][0]:
                            result[5] = 1 # Ball is bouncing on the wall
                        find_wall = False

                    if log["EVENT_TYPE"] == "BOUNCE_BRICK" or log["EVENT_TYPE"] == "BOUNCE_WALL":
                        if log["EVENT_TYPE"] == "BOUNCE_BRICK":
                            find_brick = True
                            result[6] = 1
                        else:
                            find_wall = True
                            result[7] = 1
                        first_log = logs[index-1]
                        brick_log = log

                print("Brick bounce:", result[0])
                print("Brick split success:", result[1])
                print("Brick split height:", result[2])
                print("Brick reduce life:", result[3])
                print("Brick split fit:", result[4])
                print("Wall bounce:", result[5])
                return result   
            except Exception as e:
                print("ERROR:",e)
                return [0,0,0,0,0,0,0,0]

        def check_case2(logs): # Move the paddle to the position where the ball should originally lose
            def run_move(move_count, direction):
                try:
                    pg.press(direction.lower(), move_count, 0.001)
                except:
                    pass
            
            def analyze_move(logs):
                try:
                    velocity = self.test_velocity() 
                    if velocity is not None:
                        paddle_y = logs[0]["paddle_position"][1]
                        paddle_x = logs[0]["paddle_position"][0]
                        log_length = len(logs)
                        for i in range(log_length):
                            index = log_length - i - 1
                            log = logs[index] # start from the last log
                            if log["ball_position"][1] >= paddle_y and logs[index-1]["ball_position"][1] <= paddle_y:
                                ball_x = log["ball_position"][0]
                                move_count = int(abs(ball_x - paddle_x) / velocity)
                                if ball_x < paddle_x:
                                    direction = "Left"
                                else:
                                    direction = "Right"
                                return move_count, direction
                    return None, None
                except Exception as e:
                    print("ERROR:", e)
                    return None, None
            try:
                move_count, direction = analyze_move(logs)
                if move_count == None and direction == None:
                    return None
                try:
                    process = self.start_game(1)
                    run_move(move_count, direction)
                    count = 0
                    while True:
                        self.key_press('right')
                        time.sleep(0.05)
                        count +=1
                        self.key_press('left')
                        time.sleep(0.05)
                        count +=1
                        if count > 300 or is_game_over(process):
                            break
                except:
                    pass
                process.terminate()
                time.sleep(1)
                new_logs = read_log()
                return new_logs
            except Exception as e:
                print("ERROR:", e)
                return None
  

        try:
            process = self.start_game(1)
            count = 0
            while True:
                self.key_press('right')
                time.sleep(0.05)
                count +=1
                self.key_press('left')
                time.sleep(0.05)
                count +=1
                if count > 600 or is_game_over(process):
                    break
        except:
            pass

        print("=======================Test Case=======================")
        process.terminate()
        time.sleep(1)
        try:
            print("Read log")
            logs = read_log()
        except Exception as e:
            print("ERROR:", e)
            score_initial_pos = 0
            score_initial_move = 0
            score_ball_in_range = 0
            score_ball_lost = 0
            score_brick_bounce = 0
            score_brick_split_success = 0
            score_brick_split_height = 0
            score_brick_life = 0
            score_brick_split_fit = 0
            score_wall_bounce = 0
            score_paddle_bounce = 0
            
        try:
            ball_initial_state = check_ball_initial_state(logs)
            score_initial_pos = ball_initial_state[0]
            score_initial_move = ball_initial_state[1]

            score_ball_in_range = check_ball_in_range(logs)
            score_ball_lost = check_ball_lost(logs)

            ball_bounce = check_ball_bounce(logs)
            find_brick = ball_bounce[6]
            find_wall = ball_bounce[7]
            
            score_paddle_bounce, find_paddle = check_paddle_bounce(logs)

            if find_paddle:
                score_brick_bounce = ball_bounce[0]
                score_brick_split_success = ball_bounce[1]
                score_brick_split_height = ball_bounce[2]
                score_brick_life = ball_bounce[3]
                score_brick_split_fit = ball_bounce[4]
                score_wall_bounce = ball_bounce[5]
            else:
                new_log = check_case2(logs)
                if new_log is not None:
                    new_ball_bounce = check_ball_bounce(new_log)
                    if find_brick == 0:
                        score_brick_bounce = new_ball_bounce[0]
                        score_brick_split_success = new_ball_bounce[1]
                        score_brick_split_height = new_ball_bounce[2]
                        score_brick_life = new_ball_bounce[3]
                        score_brick_split_fit = new_ball_bounce[4]
                    else:
                        score_brick_bounce = ball_bounce[0]
                        score_brick_split_success = ball_bounce[1]
                        score_brick_split_height = ball_bounce[2]
                        score_brick_life = ball_bounce[3]
                        score_brick_split_fit = ball_bounce[4]
                    if find_wall == 0:
                        score_wall_bounce = new_ball_bounce[5]
                    else:
                        score_wall_bounce = ball_bounce[5]
                    score_paddle_bounce, find_paddle = check_paddle_bounce(new_log)
                else:
                    score_brick_bounce = ball_bounce[0]
                    score_brick_split_success = ball_bounce[1]
                    score_brick_split_height = ball_bounce[2]
                    score_brick_life = ball_bounce[3]
                    score_brick_split_fit = ball_bounce[4]
                    score_wall_bounce = ball_bounce[5]
                    score_paddle_bounce = 0
        except Exception as e:
            print("ERROR:", e)
        return score_initial_pos, score_initial_move, score_ball_in_range, score_ball_lost, score_brick_bounce, score_brick_split_success, score_brick_split_height, score_brick_life, score_brick_split_fit, score_wall_bounce, score_paddle_bounce
                            

    def main(self):
        result = {
            'total': 14,
            'total_basic': 6,
            'total_advanced': 8,
            'basic' : 0,
            'advanced': 0,
            'test_cases': {
                'move_left': 0,
                'move_right': 0,
                'vertically_stable': 0,
                'initial_pos': 0,
                'initial_move': 0,
                'ball_in_range': 0,
                'ball_lost': 0,
                'wall_bounce': 0,
                'paddle_bounce': 0,
                'brick_bounce': 0,
                'brick_split_success': 0,
                'brick_split_height': 0,
                'brick_split_fit': 0,
                'brick_life': 0
            }
        }

        result_move_left = self.check_move_left()
        result_move_right = self.check_move_right(result_move_left)
        score_move_left = result_move_right[1]  # Check if the paddle can move left
        score_move_right = result_move_right[0] # Check if the paddle can move right
        score_vertically_stable = result_move_right[2] # Check if the paddle doesn't move up or down

        score_initial_pos, score_initial_move, score_ball_in_range, score_ball_lost, score_bbounce, score_brick_split_success, score_brick_split_height, score_brick_life, score_brick_split_fit, score_wall_bounce, score_paddle_bounce = self.check_case1()

        result['test_cases']['move_left'] = score_move_left
        result['test_cases']['move_right'] = score_move_right
        result['test_cases']['vertically_stable'] = score_vertically_stable
        result['test_cases']['initial_pos'] = score_initial_pos
        result['test_cases']['initial_move'] = score_initial_move
        result['test_cases']['ball_in_range'] = score_ball_in_range
        result['test_cases']['ball_lost'] = score_ball_lost
        result['test_cases']['wall_bounce'] = score_wall_bounce
        result['test_cases']['paddle_bounce'] = score_paddle_bounce
        result['test_cases']['brick_bounce'] = score_bbounce
        result['test_cases']['brick_split_success'] = score_brick_split_success
        result['test_cases']['brick_split_height'] = score_brick_split_height
        result['test_cases']['brick_split_fit'] = score_brick_split_fit
        result['test_cases']['brick_life'] = score_brick_life

        result['basic'] = result['test_cases']['move_left'] + result['test_cases']['move_right'] + result['test_cases']['vertically_stable'] + result['test_cases']['initial_pos'] + result['test_cases']['initial_move'] + result['test_cases']['ball_in_range']
        result['advanced'] = result['test_cases']['ball_lost'] + result['test_cases']['wall_bounce'] + result['test_cases']['paddle_bounce'] + result['test_cases']['brick_bounce'] + result['test_cases']['brick_split_success'] + result['test_cases']['brick_split_height'] + result['test_cases']['brick_split_fit'] + result['test_cases']['brick_life']

        return result


    


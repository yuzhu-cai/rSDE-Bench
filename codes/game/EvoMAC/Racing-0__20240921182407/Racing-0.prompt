
Task: Develop a racing game.
Requirements:
1. The game interface features a three-lane route, with a few obstacles on each lane ,but not all three lanes will have obstacles simultaneously.The three lanes at the starting point are free of obstacles.Display the vehicle's speed and the distance traveled in the top right corner of the interface.
2. Car should be controllable by the player using the arrow keys (up, down, left, right), to speed up, speed down and shifts to an adjacent lane.
3. In the game interface, the vehicle remains stationary while the obstacles move backward, simulating the vehicle's forward movement.
4. When the "s" is pressed the car should stop (set the speed to 0) .
5. There are two types of obstacles. One causes the vehicle to slow down upon contact, while the other immediately ends the game.
6. As the game starts, a log file named 'game.log' should be created to record the game's progress. The content of the game.log file should be appended with a new entry after each player action.The content of the game.log file should be cleared (if any) at the start of each game session.
Each log entry should follow this format:
{
    "timestamp": timestamp,
    "EVENT_TYPE": "speed_up" | "speed_down" | "move_left" | "move_right" |"stop" | "collide_fatal_obstacles" | "collide_slow_down_obstacles",
    "car_speed": speed,
    "car_position": [x, y]
}
    The x-coordinate of car_position represents the lane number, with lanes numbered from left to right as 1, 2, 3; the y-coordinate represents the distance traveled by the car.
    Note: Each evnet will create a new log entry, so for each log entry, Event_TYPE cannot be empty

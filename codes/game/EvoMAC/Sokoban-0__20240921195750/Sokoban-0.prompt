
Task: Develop a simple Sokoban game. You must design a GUI.
Requirements:
1. The game board should be divided into grid squares.
2. Players will control the game using the arrow keys on the keyboard.
3. As the game starts, a log file named 'game.log' should be created to record the game's progress. The content of the game.log file should be appended with a new entry after each player action.The content of the game.log file should be cleared (if any) at the start of each game session.
Each log entry should follow this format:
{
"timestamp": timestamp,
"EVENT_TYPE": "MOVE_RIGHT" | "MOVE_LEFT" | "MOVE_UP" | "MOVE_DOWN" | "INVALID_MOVE",
"player_position": [x, y],
"box_positions": [[x1, y1], [x2, y2], ...],
"game_status": "ONGOING" | "COMPLETE"
}
4. The victory conditions for the game is: All boxes are pushed onto their corresponding coordinate point.
5. The initial positions of each element are required as follows:
player_position = [1, 1]
box_positions = [[3, 3], [4, 2]]
goal_positions = [[5, 5], [6, 3]]
([3, 3] is the initial position of the first box whose target position is [5, 5].  [4, 2] is the initial position of the second box whose target position is [6, 3].)
wall_positions = [[0, 4], [1, 4], [2, 4],[3, 4],[4, 4]]
(the first numnber in each pair is the x-coordinate and the second number is the y-coordinate)


Task: Design a Single-Player Tank Battle Game
Requirements:
1. The interface should be divided into a 20x20 grid, though grid lines are not necessary. Each tank occupies one grid space, while obstacles may occupy multiple grid spaces. The background should be black, obstacles should be brown, enemy tanks should be silver, and the player's tank should be yellow.
2. The player can control the tank's movement using the arrow keys on the keyboard, allowing for movement one grid space at a time. The 'enter' key is used to fire bullets.
3. In the game, there are two enemies fixed at a certain position on the game interface, constantly firing bullets in four directions: up, down, left, and right. Two enemies and players cannot be initialized in the same row.
4. Both the player and the enemies have their own health points, which are initialized to 200. When hit by a bullet, the player's health decreases by 10 and the enemy's health decreases by 100. When health points drop to zero, the corresponding tank is destroyed. But the log still records information about the destroyed tank, with health points of 0.
5. Destroying an enemy tank earns the player 200 points. The game ends when the player's tank is destroyed or all enemy tanks are destroyed, at which point the player's score will be displayed on the screen.
6. As the game start, a new log file named 'game.log' should be created to record the game's progress. The first log entry should capture the initial state of the game. Each time a new event occurs to the player, a new log entry should be written in real-time. The logs should follow the format below. The EVENT_TYPE can only be one of the following: "INIT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "FIRE" or "INJURED". The game_state should capture the current state of the game. In this setup, the position coordinates are defined with the top-left grid as [0, 0], where the x-coordinate increases by one unit for each grid space moved to the right, and the y-coordinate increases by one unit for each grid space moved downward. The player is initialized at position [0,0].
{
    "timestamp": timestamp,
    "EVENT_TYPE": "INIT" | "MOVE_LEFT" | "MOVE_RIGHT" | "MOVE_UP" | "MOVE_DOWN" | "FIRE" | "INJURED",
    "game_state": {
        "player": {
            "position": [xp, yp],
            "health": health_player,
            "score": score
        },
        "enemies": [
            {
                "position": [xe1, ye1],  
                "health": health_enemy1
            },
            {  
                "position": [xe2, ye2],  
                "health": health_enemy2  
            } 
        ],
        "obstacle_position": [(xo1, yo1), ..., (xon, yon)]
    },
}

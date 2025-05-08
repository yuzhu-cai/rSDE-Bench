
Task: Develop a Super Mario game.
Requirements:
1. Mario should be controllable by the player using up arrow key to jump, left arrow key to walk left, right arrow key to walk right, and down arrow key to eliminate enemies. There's gravity so Mario will fall down to ground if he doesn't stand on a block. 
2. Mario should interact with various game elements:
    Blocks: Mario can hit the blocks by jumping from below. After the block is hit, a mushroom will appear on top of the block. There's one block on top of Mario's initial position where Mario can jump to hit. Once Mario touches the block, the score will increase by 100.
    Mushrooms: Once mushroom appears, it will move left and fall to the ground. If it hit the border of the game window, it will change direction until it hits Mario. Once Mario touches the muchroom, the score will increase by 1000, and the mushroom will disappear.
    Enemies: Enemies will move left and right randomly on the ground. There's one enemy on the ground.
    Flagpole: Mario aims to reach the flagpole at the rightmost position of the game to win. If Mario touches the flagpole, the score will increase by 10000 and the game will end.
3. Game setting:
    The game should have a ground (represened by a brown surface on the bottom of the game window) from left to right where Mario, enemies, and mushroom can stand and walk on, and a flagpole can place. 
    There's only one block on top of Mario's initial position where Mario can jump to hit .
    Mario should stand at the left side, on the ground. He aims to reach the flagpole at the rightmost position of the game.
    The score should be initialized as 0. It automatically increases by 1 every seconds. If Mario hits the block, the score will increase by 100. If Mario touches the mushroom, the score will increase by 1000. If Mario touches the flagpole, the score will increase by 10000.
4. The game starts immediately upon running the program. As the game starts, a log file named 'game.log' should be created to record the game's progress. Each log entry should follow this format:
{
    "timestamp": timestamp,
    "EVENT_TYPE": "MOVE_LEFT" | "MOVE_RIGHT" | "JUMP" | "HIT_BLOCK" | "TOUCH_MUSHROOM" | "ELIMINATE_ENEMY" | "REACH_FLAG" | "COLLIDE_ENEMY",
    "mario_position": [x, y],
    "enemy_position": [x, y],
    "block_position": [x, y],
    "mushroom_position": [None, None] | [x,y]
    "score": score
}
    Note: a. Each evnet will create a new log entry, so for each log entry, EVENT_TYPE cannot be empty
          b. Before the block is hit, mushroom_position should be [None, None]; Once mushroom appears, mushroom_position will show its position. When Mario touch the mushroom, mushroom_position should be [None, None] again.
          c. When player press left or right arrow key, the EVENT_TYPE should be "MOVE_LEFT" or "MOVE_RIGHT", and the mario_position should be updated to the new position.
5. Player can eliminate enemy by pressing the down arrow key. If Mario eliminates the enemy, enemy will disappear, the EVENT_TYPE should be "ELIMINATE_ENEMY", and the enemy_position should be [None, None].
6. The game should end when Mario completes touch the flagpole or Mario collides with an enemy, so last EVENT_TYPE of log entry must be "REACH_FLAG" or "COLLIDE_ENEMY".


Task: Develop a Ghostly game. You must design a GUI.
Requirements:
1. The interface should have elements like a ghost controlled by the player, other ghosts, pellets and superpellets(the big pellets) that the ghost can eat, and walls that the ghost cannot pass through.
2. Players will control the ghost using the arrow keys on the keyboard.
3. If the ghost controlled by the player eats a superpellet (the big pellets), it gains the ability to eat other ghosts .
4. If the ghost controlled by the player eat another ghost (i. e. collide with it when the player has the superpellet powerup), the ghost disappears.
5. If the ghost controlled by the player collides with another ghost when the player doesn't have the superpellet powerup, it will cause an invalid move , just like hit the wall.
6. If a game isn't over after 50 game ticks have elapsed, a monster is activated(initial position:[1,1]), which will chase the player's ghost.When the monster collide with the player's ghost, the game is over(lose). You should output the corresponding information.
7. There are some walls in the map, and ghosts cannot pass through them.
8. As the game starts, a log file named 'game.log' should be created to record the game's progress. The content of the game.log file should be appended with a new entry after each player action.The content of the game.log file should be cleared (if any) at the start of each game session.
Each log entry should follow this format:
{
"timestamp": timestamp,
"event_type": "eat_pellet" | "invalid_move" | "eat_other_ghost" | "eat_superpellet" |"monster_eat_ghost" | "ordinary_move" ,
"move_direction": "right" | "left" | "up" | "down" ,
"ghost_position": [x, y],
"monster_position": [x, y],
"game_status": "ongoing" | "win" | "lose"
}
    Before the monster is activated, the monster_position should be [-1, -1]. 
7. The victory conditions for the game is: The ghost eats all the pellets or the ghost eats all the other ghosts. When the game ends, you should output the corresponding information.
8. The initial positions of each element are required as follows:
ghost_position = [1, 1]
pellet_positions = [[3, 3], [4, 2]]
superpellet_positions = [[5, 5], [6, 3]]
other_ghost_positions = [[0, 5], [3, 5]]
walls_position = [[0,4],[1,4],[2,4],[3,4]]
    [x, y], where x is the horizontal coordinate and y is the vertical coordinate.

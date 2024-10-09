      
softwares = [
    {   'type': 'Game',
        'name': 'Ghostly',
        'task': """
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
"""
    },
    {   'type': 'Game',
        'name': 'Racing',
        'task': """
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
"""
    },
    {
        'type': 'Game',
        'name': 'Balls',
        'task': """
Task: Develop a Battle of Balls Game
Requirements:
1. Different balls will be distinguished by their colors.
2. The player moves using the up, down, left, and right arrow keys, but with the player's ball as a reference frame, other balls move relative to the player's ball, and the player's ball always remains in the center of the game interface.
3. When two balls collide, the smaller ball (with a smaller radius) will be consumed by the larger ball (with a larger radius), causing the larger ball to grow in size proportionately to the radius of the consumed ball. Player ball can also consume smaller enemy balls. When the ball is consumed, the corresponding radius should be recorded as -1 in the log.
4. The game ends if the player's ball is consumed.
5. In addition to the player's ball, initialize four enemy balls that have the same radius but are slightly smaller than the player's ball. One fixed enemy ball and three active enemy balls.
6. Small, non-player, and enemy balls will continuously spawn on the map (much smaller than the initial sizes of the player and enemy balls). When consumed, they will increase in size.
7. When the game starts, a new log file named "game.log" should be created to record the game's progress. The first log entry should capture the initial state of the game. Whenever a new event occurs involving the player, a new log entry should be written in real-time. The log should adhere to the following format. The EVENT_TYPE can only be one of the following: "INIT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN". The center of the game interface will serve as the origin(0, 0), with the positive x-direction pointing right and the positive y-direction pointing upwards.
{
    "timestamp": timestamp,
    "EVENT_TYPE": "INIT" | "MOVE_LEFT" | "MOVE_RIGHT" | "MOVE_UP" | "MOVE_DOWN",
    "game_state": {
        "player": {
            "position": [xp, yp],
            "radius": radius,
        },
        "active_enemies": [
            {
                "position": [xe1, ye1],  
                "radius": radius1
            },
            {  
                "position": [xe2, ye2],  
                "radius": radius2
            },
            {  
                "position": [xe3, ye3],  
                "radius": radius3
            }
        ],
        "fixed_enemies": [
            {
                "position": [xe4, ye4],  
                "radius": radius4
            },
        ]
}
"""},

    {
        'type': 'Game',
        'name': 'Bomberman',
        'task': """
Task: Develop a Bomberman Game
Requirements:
1. The game should feature a black background with a 13x13 grid, placing white obstacles in all even-numbered rows and columns, totaling 6x6 obstacles. There will be one player, represented in green, and two enemies, represented in red. The bombs placed by the player will be gray, and the fire will be orange.
2. The player and enemies can move on the black squares of the grid, but cannot pass through obstacles. The player’s movement will be controlled using the arrow keys, while the enemies will automatically move towards the player. The player can place bombs using the space bar, which will explode after a short delay.
3. After an explosion, fire will spread from the bomb's center in all four cardinal directions (up, down, left, right) for three squares. However, the fire can be blocked by obstacles.
4. The player starts with a health value of 100, while each enemy starts with a health value of 10. Additionally, the player initializes with a score of 0. When an enemy encounters the player, the enemy's health drops to 0, and the player's health decreases by 10. If the player or an enemy is at the center of an explosion or in a fire zone, their health decreases by 10. When an enemy's health reaches 0, it disappears. If the player's health reaches 0, the player loses the game. Each time an enemy disappears, the player's score increases by 100.
5. If all enemies are defeated, the player wins, and the game interface should display a victory message along with the player's score.
6. When the game starts, a new log file named “game.log” should be created to record the game progress. The frst log entry should capture the initial state of the game. Whenever a new event occurs with the player, a new log entry should be written in real-time. The log should adhere to the following format. The EVENT_TYPE can only be one of the following: “INIT”, “MOVE_LEFT”, “MOVE_RIGHT”, “MOVE_UP”, “MOVE_DOWN”, “PLACE_BOMB”, "BOOM" or “INJURED”. The game_board_state should reflect the current state of the board in a list format consisting of 16 elements. These elements should record the value of each grid position in a left-to-right, top-to-bottom order. Blank positions are represented by 0, the player's position by 1, the enemies' positions by 2, bomb positions by 3, explosion fire positions by 4, and obstracts positions by -1. Players initialize at the top left corner of the game interface, while enemies randomly initialize at different locations. If not an impassable object, then objects at the same location will only record the largest object number for that position (for instance, if the player and an enemy are at the same location, it will be recorded as 2).
{  
    "timestamp": "timestamp"  ,  
    "EVENT_TYPE": "INIT" | "MOVE_LEFT" | "MOVE_RIGHT" | "MOVE_UP" | "MOVE_DOWN" | "PLACE_BOMB" | "BOOM" | "INJURED",  
    "game_board_state": [],
     "player": {
         "health": health_player,
         "score": score
     },
    "enemies": [
        { 
            "health": health_enemy1
        },
        {  
            "health": health_enemy2  
        } 
    ]
}
"""},

    {
        'type': 'Game',
        'name': 'Mario',
        'task':"""
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
"""},

    {
        'type': 'Game',
        'name': 'Brick',
        'task': """
Task: Develop a Brick Breaker game.
Requirements:
1. The objective of the game is to break all the bricks by bouncing the ball off the paddle and hitting the bricks.
2. The paddle is controllable by the player using the left and right arrow keys to move left and right.
3. As the paddle hits the ball, or the ball hits the walls (including the top and sides of the game window) or bricks, the ball will bounce off.
4. Each brick starts with 3 lifes. Each time the ball hits a brick, the hit brick will split into two smaller bricks:
    - The size of the new bricks is half the size of the original brick and they together fit into the original position (one left and one right).
    - The new bricks will have a life value reduced by 1 from the original brick.
5. When a brick has 0 life, it will disappear. 
6. Game start setting: Once left or right arrow key is pressed, the game starts. Bricks are arranged on the top of the game window, and the paddle is placed at the bottom of the game window.
7. As the game starts, the ball will be launched from the center of the game window and move upwards to the bricks.
7. As the game starts, a log file named 'game.log' should be created to record the game's progress. Each log entry should follow this format:
{
    "timestamp": timestamp,
    "EVENT_TYPE": "PADDLE_MOVE_LEFT" | "PADDLE_MOVE_RIGHT" | "BOUNCE_WALL" | "BOUNCE_PADDLE" | "BOUNCE_BRICK" | "BALL_LOST",
    "paddle_position": [x,y],
    "ball_position": [x,y],
    "bricks_info": [[brick1_x, brick1_y, brick1_life], [brick2_x, brick2_y, brick2_life], [brick3_x, brick3_y, brick3_life], ...]
}
    Note: - bricks_info contains the x coordinate, y coordinate, and remaining life for all bricks. If the brick has 0 life, it's info should be [null, null, 0]
          - If a brick splits, it's bricks_info should change from [brickn_x, brickn_y, brickn_life] to [[brickn1_x, brickn1_y, brickn1_life], [brickn2_x, brickn2_y, brickn2_life]] where brickn represents the original brick.
8. The game ends when the ball falls off the screen.
"""},

    {
        'type': 'Game',
        'name': 'Gomoku',
        'task': """
Task: Develop a basic two-player Gomoku game.
Requirements:
1. The board is divided into grid squares by black intersecting vertical and horizontal lines. The board is orange yellow in color.
2. Players will be assigned either black or white pieces for the game.
3. Both players must use the left mouse button to place their pieces on the board.
4. The game concludes when one player achieves victory, preventing further piece placements on the board, and displaying the winning player's information on the board.
5. As the game start, a log file named 'game.log' should be created to record the game's progress. The first log entry should capture the initial state of the game. Each time a new event occurs, a new log entry should be written. The logs should follow the format below. The EVENT_TYPE can only be one of the following: "BLACK," "WHITE," or "INIT.". The game_board_state should capture the current state of the board in a list format, containing 16 elements. These elements should record the values in each grid position in order from left to right and top to bottom. Empty positions are represented as 0, black pieces are represented as -1, and white pieces are represented as 1.
{
    "timestamp": timestamp,
    "EVENT_TYPE": "INIT" | "BLACK" | "WHITE",
    "game_borad_state": []
}
"""}, 

    {
        'type': 'Game',
        'name': '2048',
        'task': """
Task: Design a simple 2048 game.
Requirements:
1. The game board should be divided into 4x4 grid.
2. Players can control the game using the arrow keys on the keyboard.
3. As the game start, a log file named 'game.log' should be created to record the game's progress. The first log entry should capture the initial state of the game. Each time a new event occurs, a new log entry should be written. The logs should follow the format below. The EVENT_TYPE can only be one of the following: "LEFT," "RIGHT," "UP," "DOWN," or "INIT.". The game_board_state should capture the current state of the board in a list format, containing 16 elements. These elements should record the values in each grid position in order from left to right and top to bottom, with empty positions represented as 0.
{
    "timestamp": timestamp,
    "EVENT_TYPE": "LEFT" | "RIGHT" | "UP" | "DOWN",
    "game_board_state": []
}
"""}, 

    {
        'type': 'Game',
        'name': 'Tank',
        'task': """
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
"""}, 
 {   'type': 'Game',
        'name': 'Sokoban',
        'task': """
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
"""
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineShoppingCenter',
        'data':{
                'users.txt': ['johndoe,secret123,johndoe@example.com', 'janesmith,pass456,janesmith@example.com'],
                'products.txt': ['001,Wireless Mouse,25.99', '002,Mechanical Keyboard,99.99'],
                'shopping_cart.txt': ['johndoe,001,2', 'janesmith,002,1']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'PersonalBlog',
        'data':{
                'users.txt': ['john_doe,password123', 'jane_smith,securepass'],
                'posts.txt': ['My First Blog Post|This is the content of my very first blog post.', 'Exploring Python|Python is an amazing programming language that is versatile and easy to learn.'],
                'logs.txt': ['2023-10-01 10:00:00|User john_doe logged in.', "2023-10-01 10:05:00|User john_doe created a new post titled 'My First Blog Post'."]
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineLibraryManagementSystem',
        'data':{
                'books.txt': ['1984|George Orwell|9780451524935', 'The Great Gatsby|F. Scott Fitzgerald|9780743273565', 'To Kill a Mockingbird|Harper Lee|9780061120084'],
                'users.txt': ['johndoe|password123', 'janesmith|securepass456']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'MovieRecommendationSystem',
        'data':{
                'users.txt': ['user1,secret123', 'user2,moviebuff'],
                'movies.txt': ['1,Inception,A thief who steals corporate secrets through dreams.,8.8', '2,Titanic,A love story that unfolds on the ill-fated Titanic.,7.8'],
                'favorites.txt': ['user2,1', 'user2,2'],
            }
    }
        ,
    {
        'type': 'Website',
        'name': 'NoteTakingApp',
        'data':{
                'users.txt': ['john_doe:abcd1234', 'jane_smith:xyz9876'],
                'notes.txt': ['1|Grocery List|Eggs, Milk, Bread', '2|Meeting Notes|Discussed project milestones and deadlines.'],
            }
    }    
    ,

    {
        'type': 'Website',
        'name': 'EventPlanner',
        'data':{
                'users.txt': [    'john_doe:abcd1234', 'jane_smith:xyz9876'],
                'events.txt': [    '1|Team Meeting|2024-08-30|Conference Room A|Discuss project updates.', '2|Annual Conference|2024-09-15|Grand Hall|Networking sessions.'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'ExpenseTracker',
        'data':{
                'users.txt': ['user1:pass123', 'user2:password456'],
                'expenses.txt': ['2024-10-01|Groceries|50.00|Food', '2024-10-02|Transport|15.00|Travel'],
                'income.txt': ['2024-10-01|50.00|Salary'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'FreelancerMarketplace',
        'data':{
                'users.txt': ['john_doe,securePassword123'],
                'freelancers.txt': ['Jane Smith,jane@example.com,www.janesportfolio.com'],
                'projects.txt': ['Website Development,A project to create a small business website,1'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'GreenLivingGuide',
        'data':{
                'users.txt': ['user1,password123', 'user2,securepassword'],
                'tips.txt': ['Reduce Plastic Use:Switch to reusable bags for shopping.', 'Compost Organic Waste:Create a compost pile to reduce waste.'],
                'articles.txt': ['The Benefits of Solar Energy:Solar energy is a clean and renewable energy source...', 'How to Start a Vegetable Garden:Gardening can significantly reduce your carbon footprint...'],
                'community_posts.txt': ['Tips for Shopping Sustainably:Always carry your reusable bags...', 'How to Reduce Water Usage:Limit your shower time to 5 minutes...'],
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'PortfolioSite',
        'data':{
                'users.txt': ['username1,password1,email1@gmail.com', 'username2,password2,email2@gmail.com'],
                'projects.txt': ['username1,http://example.com/project_link1.com,project_description1', 'username1,http://example.com/project_link2.com,project_description2'],
                'blogs.txt': ['username1,blog_title1,blog_content1', 'username1,blog_title2,blog_content2'],
                'contacts.txt': ['contact_name1,contact_email1@gmail.com,message_content1', 'contact_name2,contact_email2@gmail.com,message_content2'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'RecipeHub',
        'data':{
                'users.txt': ['user1:password123', 'user2:mySecurePassword'],
                'recipes.txt': ['0;Pancakes;flour,eggs,milk;Mix ingredients;Cook on skillet until golden', '1;Spaghetti;spaghetti,tomato sauce;Boil spaghetti;Serve with sauce']
            }
    }
    ,    
     {
        'type': 'Website',
        'name': 'SkillShare',
        'data':{
                'users.txt': ['johnDoe,securePassword123'],
                'skills.txt': ['johnDoe:Python,JavaScript,HTML', 'hhh:abc,edf,mmm'],
                'profiles.txt': ['johnDoe'],
                'about.txt': ['This is a ...|abc@def.com'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'TaskManager',
        'data':{
                'tasks.txt': ['1|Finish project report|2023-10-31', '2|Grocery shopping|2023-10-15'],
                'users.txt': ['johndoe|password123', 'janesmith|securepass456']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'FitnessChallenges',
        'data':{
                'users.txt': ['johnsmith:password123', 'janedoe:supersecurepass'],
                'challenges.txt': ['30-Day Yoga Challenge: A month-long yoga journey to improve flexibility and mindfulness: 30 days', '10K Run Challenge: Train to run 10 kilometers in a month: 30 days'],
                'current_challenges.txt': ["johnsmith:30-Day Yoga Challenge", "janedoe:10K Run Challenge"],
                'progress.txt': ['johnsmith:30-Day Yoga Challenge:15 days:Feeling great! Need to improve on morning sessions.', 'janedoe:10K Run Challenge:5 days:Completed 2K today. Happy with progress!'],
                'activityLog.txt': ["2023-10-01 10:00:00:johnsmith:Joined '30-Day Yoga Challenge'", "2023-10-02 11:30:00:janedoe:Updated progress for '10K Run Challenge'"],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'ElderCareResources',
        'data':{
                'users.txt': ['john_doe,password123', 'jane_smith,securepass456'],
                'resources.txt': ['1,Home Care Services,Comprehensive services for in-home assistance.', '2,Nutrition for Seniors,A guide on maintaining a healthy diet in older age.'],
                'inquiries.txt': ["Alice Johnson,alice@example.com,How can I find a caregiver?", "Bob White,bob@example.com,Great resource, very helpful!"],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'VolunteerMatch',
        'data':{
                'users.txt': ['username1,password1', 'username2,password2'],
                'opportunities.txt': ['1,Opportunity Title 1,Description of opportunity 1', '2,Opportunity Title 2,Description of opportunity 2'],
                'applications.txt': ["alice,alice@example.com,1"],
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'DigitalStorytellingPlatform',
        'data':{
                'stories.txt': ['johndoe|My First Adventure|Once upon a time in a land far away', 'janedoe|The Mysterious Forest|In a dark and enchanted forest'],
                'users.txt': ['johndoe|password123', 'janedoe|securepass456']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'DailyJournalApp',
        'data':{
                'journal_entries.txt': ['My First Day|Today was a great day. I started my new job!', 'Weekend Adventures|Went hiking with friends this weekend. Beautiful weather!'],
                'user_credentials.txt': ['user1|password123', 'user2|mypassword']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'HealthConsultationPlatform',
        'data':{
                'feedback.txt': ['username1,Great service', 'username2,Really helpful consultation'],
                'consultations.txt': ['username1,2023-10-15,10:00,scheduled', 'username2,2023-10-16,11:00,scheduled'],
                'users.txt': ['username1,password1', 'username2,password2']
            }
    }
     ,
    {
        'type': 'Website',
        'name': 'RemoteJobBoard',
        'data':{
                'users.txt': ['john_doe,password123,john@example.com', 'jane_smith,password456,jane@example.com'],
                'jobs.txt': ['Software Developer,Tech Company,Remote software development position for various projects.', 'Project Manager,Business Solutions,Lead and manage teams on remote projects.'],
                'applied_jobs.txt': ['john_doe:Software Developer,Tech Company,Remote software development position for various projects.', 'jane_smith:Project Manager,Business Solutions,Lead and manage teams on remote projects.'],
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'MusicFestivalDirectory',
        'data':{
                'festivals.txt': ['Coachella|California|2023-04-14|Artist1, Artist2, Artist3', 'Lollapalooza|Chicago|2023-08-03|ArtistA, ArtistB, ArtistC'],
                'users.txt': ['user1|123', 'user2|456']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'GardeningForBeginners',
        'data':{
                'users.txt': ['user1,password1,user1@example.com', 'user2,password2,user2@example.com'],
                'tips.txt': ['Water your plants in the early morning for best results.', 'Use compost to nourish your garden soil.'],
                'forum_posts.txt': ["user1,What is the best type of soil for indoor plants?,1", "user2,I recommend using premium potting soil for better growth.,2"],
                'comments.txt': ["1,user1,Great advice, thanks!", "2,user2,I appreciate the suggestions."],
            }
    }    
    ,
    {
        'type': 'Website',
        'name': 'DigitalArtworkGallery',
        'data':{
        'users.txt': [ 'john_doe:abcd1234', 'jane_smith:xyz9876'],
        'artworks.txt': ['1|Sunset Over the Hills|A beautiful sunset painting.', '2|Abstract Shapes|A collection of abstract shapes.'],
        }
    }    
    ,
    {
        'type': 'Website',
        'name': 'PetCareCommunity',
        'data':{
                'users.txt': ['john_doe,password123', 'jane_smith,mysecretpassword'],
                'posts.txt': ['1,john_doe,2023-10-01 12:00:00,I love my golden retriever!', '2,jane_smith,2023-10-02 09:30:00,Just adopted a kitten!'],
                'resources.txt': ['Dog Training Tips,Everything you need to know about training your dog.,http://dogtraining.com/', 'Pet Nutrition,Learn about the best food for your pets.,http://petnutrition.com/'],
                'profiles.txt': ['john_doe,Max,3', 'jane_smith,Luna,1'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'NutritionInformationHub',
        'data':{
                'recipes.txt': ['Spaghetti Bolognese|spaghetti, ground beef, tomato sauce|Boil spaghetti, cook beef, mix with sauce', 'Pancakes|flour, milk, eggs|Mix ingredients, cook on griddle'],
                'nutrition_info.txt': ['apple,52 calories,0.2g fat,14g carbs,0.3g protein', 'banana,89 calories,0.3g fat,23g carbs,1.1g protein'],
                'users.txt': ['username1,password1', 'username2,password2']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineCulturalFestivals',
        'data':{
                'user_experiences.txt': ['john_doe;Attended the Diwali Festival; it was unforgettable!', 'jane_smith;The Holi Celebration brought back so many memories.'],
                'comments.txt': ['Diwali Festival;john_doe;The festival was mesmerizing!', 'Holi Celebration;jane_smith;I loved the vibrant colors and music.'],
                'festival_data.txt': ['Diwali Festival;An annual celebration of lights;2023-11-12;Cultural;Various Artists', 'Holi Celebration;Festival of colors;2023-03-08;Religious;Local Dancers'],
                'user_data.txt': ['john_doe,password123', 'jane_smith,securepass456']
            }
    }
    ,
        {
        'type': 'Website',
        'name': 'DailyHealthTips',
        'data':{
                'users.txt': ['john_doe,securepassword,johndoe@example.com'],
                'daily_tips.txt': ['2023-10-01,Drink at least 8 glasses of water daily.', '2023-10-02,Incorporate fruits and vegetables into every meal.'],
                'feedback.txt': ['john_doe,2023-10-01,Great tip today! Thank you!'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineVintageMarket',
        'data':{
                'users.txt': ['johndoe,password123', 'janedoe,qwerty456'],
                'listings.txt': ['Vintage Clock,Old mechanical clock from the 1960s,25.00', 'Retro Vinyl Record,Classic rock album from the 70s,15.00'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'CharitableGivingPlatform',
        'data':{
                'users.txt': ['johnDoe,password123,johndoe@example.com', 'janeSmith,password456,janesmith@example.com'],
                'contributions.txt': ['johnDoe,SaveTheWhales,50', 'janeSmith,HelpTheChildren,100'],
                'charities.txt': ['SaveTheWhales,To protect whale species and their habitats.', 'HelpTheChildren,Providing education and resources to impoverished children.'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'RemoteInternshipMarketplace',
        'data':{
                'users.txt': ['john_doe,securepassword,John,Doe,john.doe@example.com'],
                'internships.txt': ['1,Software Development Internship,A remote internship in software development,Software,2023-12-31', '2,Test,ABC,CDR,2024-12-31'],
                'applications.txt': ['1,john_doe,1,2023-10-01'],
            }
    }
    ,    
    {
        'type': 'Website',
        'name': 'FitnessTracker',
        'data':{
        'users.txt': [ 'john_doe:abcd1234', 'jane_smith:xyz9876'],
        'goals.txt': ['john_doe|100|80', 'jane_smith|80|90'],
        'activities.txt': ['john_doe|Running|500|95', 'john_doe|Swimming|300|93', 'jane_smith|Boxing|300|82'],
        }
    }   
    ,
    {
        'type': 'Website',
        'name': 'OnlineTherapeuticJournaling',
        'data':{
                'users.txt': ['john_doe:password1', 'jane_smith:password2'],
                'entries.txt': ['1|john_doe|My First Entry|Today I felt happy.|2023-10-01 10:00:00', '2|jane_smith|Thoughts on Life|Life has its ups and downs.|2023-10-01 11:00:00'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineCulturalExchange',
        'data':{
                'contacts.txt': ['Name 1,email1@example.com,Message from user 1', 'Name 2,email2@example.com,Message from user 2'],
                'exchanges.txt': ['Cultural Title 1,Description of cultural exchange 1', 'Cultural Title 2,Description of cultural exchange 2'],
                'users.txt': ['username1,password1', 'username2,password2']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'VirtualWellnessRetreats',
        'data':{
            'users.txt': [ 'john_doe:abcd1234', 'jane_smith:xyz9876'],
            'retreats.txt': ['1|john_doe|Morning Yoga|2024-09-01|08:00 AM|Instructor A', '2|john_doe|Mindfulness Meditation|2024-09-02|10:00 AM|Instructor B']
        }
    }    
    ,
    {
        'type': 'Website',
        'name': 'TravelDiary',
        'data':{
                'users.txt': ['john_doe,password1,john@example.com', 'jane_smith,pass213,jane@example.com'],
                'diary_entries.txt': ['1,john_doe,Trip to Paris,Had a wonderful time soaking in the sights...', '2,jane_smith,Beach Vacation,Relaxed at the beach with friends...'],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'EcoFriendlyLivingTips',
        'data':{
                'users.txt': ['johndoe,password123', 'janesmith,password456'],
                'tips.txt': ['Reduce plastic usage by carrying reusable bags.', 'Opt for energy-efficient appliances.'],
                'resources.txt': ['https://www.epa.gov/environmental-topics', 'https://www.worldwildlife.org/'],
                'forum_posts.txt': ["johndoe,I started composting and it's great!", "janesmith,What's the best way to reduce water usage?"],
                'contact_messages.txt': ["John Doe,johndoe@example.com,Love your tips! Keep it up!", "Jane Smith,janesmith@example.com,How can I help the local community?"],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'FitnessEquipmentRental',
        'data':{
                'users.txt': ['john_doe,password123,John Doe,john@example.com', 'jane_smith,password456,Jane Smith,jane@example.com'],
                'equipment.txt': ['1,Treadmill,"High-quality treadmill for home use",10,15.00', '2,Dumbbells,"Set of 5kg and 10kg dumbbells",5,10.00'],
                'rentals.txt': ['1001,john_doe,1,7,2023-10-01,inactive', '1002,jane_smith,1,2,2023-10-09,inactive', '1003,john_doe,2,3,2023-10-09,active'],
                'returns.txt': ["5001,1001,2023-10-08", "5002,1002,2023-10-11"],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'OnlineThriftStore',
        'data':{
        'users.txt': [ 'john_doe:abcd1234', 'jane_smith:xyz9876'],
        'on_sale.txt': ['cell phone|A brand new cell phone.|500.00|jane_smith', 'lamp|A vintage lamp in excellent condition.|45.00|john_doe','jacket|Stylish jacket, barely worn.|30.00|jane_smith'],
        'carts.txt': ['john_doe|jacket'],
        'sold.txt': ['john_doe|laptop|A laptop with high performance.|700.00|jane_smith']
        }
    }    
    ,
    {
        'type': 'Website',
        'name': 'PersonalFinanceBlog',
        'data':{
        'users.txt': [ 'john_doe:abcd1234:banker', 'jane_smith:xyz9876:broker'],
        'on_sale.txt': ['1|john_doe|Bank Update|2024-08-28|Banking|An update on bank account.', '2|john_doe|How to Invest|2023-09-15|Investment|A tutorial on investment.','3|jane_smith|Flight Insurance|2023-12-23|Insurance|Flight Insurance.', '4|john_doe|Life Insurance|2022-01-01|Insurance|Life Insurance.']
        }
    }   
    ,
    {
        'type': 'Website',
        'name': 'MusicCollaborator',
        'data':{
                'projects.txt': ['Summer_Song|First collaborative project for summer|john_doe,jane_smith', 'Winter_Melody|A melody for winter|jane_smith,john_doe'],
                'users.txt': ['john_doe|password123', 'jane_smith|securepassword'],
                'music.txt': ['Summer_Song|www.example_1.com', 'Winter_Melody|www.example_2.com']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'MotivationalQuotesApp',
        'data':{
                'Favorites.txt': ['user1|The best way to predict the future is to invent it.|Alan Kay'],
                'Quotes.txt': ['The only way to do great work is to love what you do.|Steve Jobs', 'Success is not the key to happiness. Happiness is the key to success.|Albert Schweitzer'],
                'Users.txt': ['user1|abc123', 'user2|def456']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'ParentingAdviceForum',
        'data':{
                'users.txt': ['john_doe,password123', 'jane_smith,securepass456'],
                'threads.txt': ['1,Best Baby Names,Looking for unique baby name ideas!,john_doe', '2,Potty Training Tips,Any tips for a smooth potty training?,jane_smith'],
                'comments.txt': ['1,1,How about the name "Sophie"?,jane_smith', '2,2,Start with a schedule!,john_doe'],
                'advice_posts.txt': ["1,Dealing with Sleep Issues,Establish a bedtime routine.,john_doe", "2,Healthy Eating Habits,Introduce vegetables early!,jane_smith"],
                'contact.txt': ["1,editor,jd@example.com,this is a test,john_doe", "2,editor,jd@example.com,this is a test too,jane_smith"],
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'VirtualBookPublishing',
        'data':{
                'books.txt': ['bookTitle1|bookAuthor1|bookContent1', 'bookTitle2|bookAuthor2|bookContent2'],
                'users.txt': ['username1|password1', 'username2|password2']
            }
    }
    ,
    {
        'type': 'Website',
        'name': 'PeerTutoringNetwork',
        'data':{
                'contacts.txt': ['John Doe:johndoe@example.com:Need help with the site.','Jane Doe:jane@example.com:Inquiry about tutoring hours.'],
                'requests.txt': ['johndoe:Math:Help with calculus problems:2023-10-01','janedoe:English:Need assistance with essay writing:2023-10-02'],
                'tutors.txt': ['Alice Smith:Math:True', 'Bob Johnson:Science:False'],
                'users.txt': ['johndoe:password123:johndoe@example.com', 'janedoe:securepass456:janedoe@example.com']
            }
    }    
    ,
    {
        'type': 'Website',
        'name': 'GourmetFoodSubscription',
        'data':{
        'users.txt': [ 'john_doe:abcd1234', 'jane_smith:xyz9876'],
        'food_boxes.txt': ['1|Vegan|A selection of fresh vegan ingredients and recipes.', '2|Meat Lovers|Premium cuts of meat with seasoning and cooking tips.','3|Cheese King|All kinds of food with cheese.'],
        'inquiries.txt': ['1|jane_smith|js@food.com|Unable to login.']
        }
    }   

]

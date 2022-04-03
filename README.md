# Reinforcement-Learning - Snake
Q-Learning and Deep-Q-Learning Implementation to play Snake from scratch using a selfmade Tkinter Environment, numpy and Keras

# Run the algorithms
The agents can be started from ```main.py```  <br>
Configurations are made in ```Config.py```  <br>
To control the statistics that are printed for every training run alter ```stats.py```  <br>

# Game Design

### Actions
move up = (1,0,0,0)  <br>
move down = (0,1,0,0)  <br>
move left = (0,0,1,0)  <br>
move right = (0,0,0,1)   <br>

### State
Hitting a wall moving right   0 or 1   <br>
Hitting a wall moving left    0 or 1   <br>
Hitting a wall moving up      0 or 1   <br>
Hitting a wall moving down    0 or 1   <br>
Hitting own tail moving right 0 or 1   <br>
Hitting own tail moving left  0 or 1   <br>
Hitting own tail moving right 0 or 1   <br>
Hitting own tail moving right 0 or 1   <br>
Head currently moving right   0 or 1   <br>
Head currently moving left    0 or 1   <br>
Head currently moving up      0 or 1   <br>
Head currently moving down    0 or 1   <br>
Direction to apple is right   0 or 1   <br>
Direction to apple is left    0 or 1   <br>
Direction to apple is down    0 or 1   <br>
Direction to apple is up      0 or 1   <br>

## Rewards
MOVE_TO_APPLE_REWARD  - Snake moves into the direction of the apple <br>
MOVE_AWAY_REWARD - Snake does not move into the direction of the apple <br>
GET_APPLE_REWARD - Snake eats an apple <br>
COLLIDE_REWARD - Snake collides with tail or wall  <br>

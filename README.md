# Reinforcement-Learning - Snake
Q-Learning and Deep-Q-Learning Implementation to play Snake in a self-written Tkinter Environment 

# Game Design
## Definition of State and Actions

### Actions
move up = (1,0,0,0)  <br>
move down = (0,1,0,0)  <br>
move left = (0,0,1,0)  <br>
move right = (0,0,0,1)   <br>

### State
Hitting a wall moving right   0 or 1
Hitting a wall moving left    0 or 1
Hitting a wall moving up      0 or 1
Hitting a wall moving down    0 or 1
Hitting own tail moving right 0 or 1
Hitting own tail moving left  0 or 1
Hitting own tail moving right 0 or 1
Hitting own tail moving right 0 or 1
Head currently moving right   0 or 1
Head currently moving left    0 or 1
Head currently moving up      0 or 1
Head currently moving down    0 or 1
Direction to food is right    0 or 1
Direction to food is left     0 or 1
Direction to food is down     0 or 1
Direction to food is up       0 or 1

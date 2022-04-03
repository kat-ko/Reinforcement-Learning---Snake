# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 21:54:36 2022

@author: korte
"""

class Config:
    
    # Board and Game Settings
    BOARD_DIM = 12
    BOARD_WIDTH = 240
    BOARD_HEIGHT = 240
    DELAY = 0
    DOT_SIZE = 20
    MAX_RAND_POS_APPLE = 10
    MAX_RAND_POS_SNAKE = 8 # otherwise is too hard to play
    IM_SIZE = 20 # set how big one image on the Canvas is
    NUM_STATES = 2**15 # state = (straight blocked, right blocked, left blocked, moveup, movedown, moveleft, moveright, up food, right food, down food, left food)
    NUM_ACTIONS = 4  # 4 directions that the snake can move
    
    # Training Settings
    NUM_EPISODES = 10001  # number of games to train for
    NUM_TEST_RUNS = 11
    TRAIN_DELAY = 0
    TEST_DELAY = 100
    STATS_EVERY_TRAIN = 100
    STATS_EVERY_TEST = 10
    
    # Epsilon Decay Variant
    EPSILON_DECAY_ONE = 1
    EPSILON_DECAY_TWO = 2
    EPSILON_STEADY = 3
    
    EPSILON_VARIATION = EPSILON_DECAY_ONE
    
    # Different Epsilon Values
    EPSILON_DECAY_ONE_VALUE = 0.999  # exploration rate in training games
    EPSILON_DECAY_TWO_VALUE = 1/(NUM_EPISODES/5)
    EPSILON_STEADY_VALUE = 0.3
    
    # Q Settings
    GAMMA = 0.7  # discount rate
    ALPHA = 0.1 # learning rate, the amount that the weights are updated during training
    
    # Rewards
    MOVE_TO_APPLE_REWARD = +1
    MOVE_AWAY_REWARD = 0
    GET_APPLE_REWARD = +10
    COLLIDE_REWARD = -10
    
    SCREENSHOT = False
    
    # Train from beginning or load existing Q Table
    TRAINING = True
    Q_TABLE = "qtable/qtable-1648141076.pickle"
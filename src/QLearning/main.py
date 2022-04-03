# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 14:21:38 2022

@author: korte
"""

import sys
import random
from PIL import Image, ImageTk, ImageGrab
from tkinter import Tk, Frame, Canvas, ALL, NW, ttk
import numpy as np
from operator import add
import matplotlib.pyplot as plt
import pickle
import time
from QValues import QValues
from Config import Config
from Board import Board
from stats import training_stats
from stats import testing_stats
from stats import plot_stats

random.seed(1)
#%%

# Initialising Statistic Scores
def init_stat():
    global scores
    scores = []
    global ep_rewards
    ep_rewards = []
    global moves
    moves = []
    global epsilons
    epsilons = []
    global epsilon 
    epsilon = 1
    global num_games
    num_games = 0

def init_scores():
    global aggr_ep_rewards 
    aggr_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}
    global aggr_scores
    aggr_scores = {'ep': [], 'avg': [], 'max': [], 'min': []}
    global aggr_moves
    aggr_moves= {'ep': [], 'avg': [], 'max': [], 'min': []}
    
    global test_ep_rewards
    test_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}
    global test_scores
    test_scores = {'ep': [], 'avg': [], 'max': [], 'min': []}
    global test_moves
    test_moves = {'ep': [], 'avg': [], 'max': [], 'min': []}
    
    global cumm_rewards
    cumm_rewards = []
    global average_snake_length
    average_snake_length = []
    global Q_t
    Q_t = QValues()

#%%
            
class Snake(Frame):

    def __init__(self):
        super().__init__()
        self.master.title('Snake')
        
        self.board = Board(Q_t, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, num_games, cumm_rewards, root)
        self.pack()

def runGame():
    global root
    root = Tk()
    nib = Snake()
    root.mainloop()
    root.destroy()
    return nib.board.getStats()

def setTestMode():
    print("Start Testing")
    Config.DELAY = Config.TEST_DELAY
    Config.TRAINING = False
    Config.STATS_EVERY = Config.STATS_EVERY_TEST
    init_stat()

def setTrainingMode():
    print("Start Training")
    Config.DELAY = Config.TRAIN_DELAY
    Config.TRAINING = True
    Config.STATS_EVERY = Config.STATS_EVERY_TRAIN
    init_stat()
    init_scores()
    
def loadQTable():
    # Can be used to load an existing Qtable from folder
    name = Config.Q_TABLE
    with open(name, "rb") as f:
        Q_values = pickle.load(f)
    return Q_values

def dumpQTable(Q):
    latestQ = np.copy(Q)
    with open(f"qtable/qtable-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(latestQ, f)

def playARound():
    
    # use global variables to access values over all games
    global Q_t
    global scores
    global ep_rewards
    global cumm_rewards
    global moves
    global epsilon 
    global epsilons
    global num_games
    global average_snake_length
        
    setTrainingMode()
    
    for episode in range(Config.NUM_EPISODES):
        Q, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, num_games, cumm_rewards = runGame()
        Q_t = Q
        
        if episode % Config.STATS_EVERY == 0 and episode != 0:
            training_stats(aggr_ep_rewards, aggr_scores, aggr_moves, episode, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, cumm_rewards)
            
    # save latest Q table
    dumpQTable(Q_t.values)
        
    # After training is finished we shift to testing mode
    setTestMode()
        
    # Run Test runs without exploration
    for run in range(Config.NUM_TEST_RUNS):
        runGame() 
        if run % Config.STATS_EVERY == 0 and run != 0:
            testing_stats(test_ep_rewards, test_scores, test_moves, run, scores, ep_rewards, moves)

    # After testing is finished plot stats 
    plot_stats(aggr_ep_rewards, aggr_scores, aggr_moves, cumm_rewards, average_snake_length, test_ep_rewards, test_scores, test_moves)
    return aggr_ep_rewards, aggr_scores, aggr_moves, cumm_rewards, average_snake_length, test_ep_rewards, test_scores, test_moves

def main():
    # Change different variables and compare performance
    
    #############################
    ## first parameter setting ##
    #############################
    
    #Config.GAMMA = 0.6
    #Config.ALPHA = 0.0001
    Config.SCREENSHOT = True
    Config.MOVE_AWAY_REWARD = -1
    first_ep_rewards, first_scores, first_moves, first_cumm_rewards, first_snake_length, first_t_ep_rewards, first_t_scores, first_t_moves = playARound()
    
    ##############################
    ## second parameter setting ##
    ##############################
    

    #Config.GAMMA = 0.7
    #Config.ALPHA = 0.001
    Config.SCREENSHOT = False
    Config.MOVE_AWAY_REWARD = 0
    second_ep_rewards, second_scores, second_moves, second_cumm_rewards, second_snake_length, second_t_ep_rewards, second_t_scores, second_t_moves = playARound()
    
    #############################
    ## third parameter setting ##
    #############################

    #Config.GAMMA = 0.8
    #Config.ALPHA = 0.01
    Config.MOVE_AWAY_REWARD = +1
    third_ep_rewards, third_scores, third_moves, third_cumm_rewards, third_snake_length, third_t_ep_rewards, third_t_scores, third_t_moves = playARound()
    
    ##############################
    ## fourth parameter setting ##
    ##############################
    
    #Config.GAMMA = 0.9
    #Config.ALPHA = 0.1
    #fourth_ep_rewards, fourth_scores, fourth_moves, fourth_cumm_rewards, fourth_snake_length, fourth_t_ep_rewards, fourth_t_scores, fourth_t_moves = playARound()
    
    
    # Print plots to compare the different settings
    # label="gamma = 0.6"
    plt.plot(first_ep_rewards['ep'], first_cumm_rewards, label="reward -1")
    plt.plot(second_ep_rewards['ep'], second_cumm_rewards, label="reward 0")
    plt.plot(third_ep_rewards['ep'], third_cumm_rewards, label="reward +1")
    #plt.plot(fourth_ep_rewards['ep'], fourth_cumm_rewards, label="alpha = 0.1")
    plt.legend(loc=4)
    plt.xlabel("Episode")
    plt.ylabel("Average Cummulated Reward")
    plt.show()
    
    plt.plot(first_scores['ep'], first_scores['avg'], label="reward -1")
    plt.plot(second_scores['ep'], second_scores['avg'], label="reward 0")
    plt.plot(third_scores['ep'], third_scores['avg'], label="reward +1")
    #plt.plot(fourth_scores['ep'], fourth_scores['avg'], label="alpha = 0.1")
    plt.legend(loc=4)
    plt.xlabel("Episode")
    plt.ylabel("Average Scores")
    plt.show()
    
    plt.plot(first_ep_rewards['ep'], first_snake_length, label="reward -1")
    plt.plot(second_ep_rewards['ep'], second_snake_length, label="reward 0")
    plt.plot(third_ep_rewards['ep'], third_snake_length, label="reward +1")
    #plt.plot(fourth_ep_rewards['ep'], fourth_snake_length, label="alpha = 0.1")
    plt.legend(loc=4)
    plt.xlabel("Episode")
    plt.ylabel("Average Cummulated Snake Length")
    plt.show()
    
    print("Variation reward with move to apple +1")
    
if __name__ == '__main__':
    main()
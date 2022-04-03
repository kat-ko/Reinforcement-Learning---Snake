# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 23:58:02 2022

@author: korte
"""

import sys
import random
from random import randint
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
import numpy as np
from operator import add
import matplotlib.pyplot as plt
import pickle
import time
import collections
import pandas as pd


from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.layers.core import Dense, Dropout

from Config import Config

class DQNAgent(object):
    def __init__(self):
        self.reward = 0
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0      
        self.actual = []
        self.first_layer = Config.FIRST_LAYER_SIZE
        self.second_layer = Config.SECOND_LAYER_SIZE
        self.third_layer = Config.THIRD_LAYER_SIZE
        self.replay_memory = collections.deque(maxlen=Config.MEMORY_SIZE)
        self.weights = Config.WEIGHTS_PATH
        self.load_weights = Config.LOAD_WEIGHTS
        self.step = 1
        self.target_update_counter = 0
        
        # Main Model: the model that gets trained every step
        self.model = self.network()
        # Target Model: what we predict against every step
        self.target_model = self.network()
        self.target_model.set_weights(self.model.get_weights())

    def network(self):
        model = Sequential()
        model.add(Dense(self.first_layer, activation='relu', input_dim=15))
        model.add(Dense(self.second_layer, activation='relu'))
        model.add(Dense(self.third_layer, activation='relu'))
        #model.add(Conv2D(self.first_layer, kernel_size=3, activation=’relu’, input_shape=(28,28,1)))
        #model.add(Conv2D(self.second_layer, kernel_size=3, activation=’relu’))
        #model.add(Flatten())

        model.add(Dense(4, activation='softmax'))
        # Adam is a stochastic gradient descent method based on adaptive estimation of mean and variance
        opt = Adam(Config.ALPHA)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            model.load_weights(self.weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))

    # Trains Main Network every step
    def train(self):
        if len(self.replay_memory) < Config.BATCH_SIZE:
            return
        else:
            minibatch = random.sample(self.replay_memory, Config.BATCH_SIZE)
        
        # current states in index 0 of the memory
        current_states = np.array([transition[0] for transition in minibatch]) # size 32 x 15
        current_qs_list = self.model.predict(current_states) # size 32 x 4
        
        
        # new states in index 3 of the memory
        new_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_states)
        
        X = np.ndarray((Config.BATCH_SIZE, 15))
        Y = np.ndarray((Config.BATCH_SIZE, 4))
        
        # Iterate trough minibatch
        for index, (current_state, action, reward, next_state, done) in enumerate(minibatch):
            # if state is not terminal, get q from future states
            if not done:
                max_future_q = np.amax(future_qs_list[index])
                new_q = reward + Config.GAMMA * max_future_q
            else: 
                # if we are done there is no future q so we set reward as target
                new_q = reward
                
            current_qs = current_qs_list[index] # self.model.predict(current_states)[]
            current_qs[np.argmax(action)] = new_q
            
            X[index][:] = current_state
            Y[index][:] = current_qs

        #y = np.reshape()
        # fit on all samples in one batch to improve training
        self.model.fit(np.array(X), Y, epochs=1, verbose=0, shuffle=False)

        # if counter reaches the set value we update the target network with weights from the main network
        if self.target_update_counter > Config.UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
    
    def epsilon_decay_one(self, epsilon, EPSILON_DECAY):
        epsilon_new = epsilon * EPSILON_DECAY
        if epsilon_new < 0.1:
            epsilon_new = 0.1
        return epsilon_new

    def epsilon_decay_two(self, num_games, EPSILON_DECAY):
        epsilon_new = 1 - (num_games * EPSILON_DECAY)
        if epsilon_new < 0.1:
            epsilon_new = 0.1
        return epsilon_new
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 14:23:20 2022

@author: korte
"""
import numpy as np 

class QValues(object):
    
    def __init__(self):
        '''Initialize with empty lookup table.'''
        self.values = {}
    
    def assign_loaded_values(self, values):
        self.values = self.values
        
    def get_value(self, state, action):
        '''Return stored q value for (state, action) pair or a random number if unknown.'''
        if not state in self.values:
            self.values[state] = {}
        if not action in self.values[state]:
            self.values[state][action] = abs(np.random.randn()) + 1
        return self.values[state][action]
    
    def set_value(self, state, action, value):
        '''Stored q value for (state, action) pair.'''
        if not state in self.values:
            self.values[state] = {}
        if not action in self.values[state]:
            self.values[state][action] = 0
        
        self.values[state][action] = value
    
    def max_action(self, state, actions, learning=True):
        '''Return the action with highest q value for given state and action list.'''
        if not learning and not state in self.values:
            return actions[0] if actions else None
        
        max_value = -np.inf
        max_action = actions[0] if actions else None
        for action in actions:
            if not learning and not action in self.values[state]:
                continue

            value = self.get_value(state, action)
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value and learning:
                max_action = np.random.choice([max_action, action])
        return max_action
    
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
    

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 21:42:58 2022

@author: korte
"""

import sys
import random
from random import randint
from PIL import Image, ImageTk, ImageGrab
from tkinter import Tk, Frame, Canvas, ALL, NW, ttk
import numpy as np
from operator import add
import matplotlib.pyplot as plt
import pickle
import time
import collections
import pandas as pd
from QValues import QValues
from Config import Config
from pyscreenshot import grab

class Board(Canvas):

    def __init__(self, Q, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, num_games, cumm_rewards, root):
        super().__init__(width=Config.BOARD_WIDTH, height=Config.BOARD_HEIGHT,
            background="beige", highlightthickness=0)
        self.initGame(Q, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, num_games, cumm_rewards, root)
        self.pack()


    def initGame(self, Q, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, num_games, cumm_rewards, root):
        '''initializes game'''
        self.root = root
        self.inGame = True
        self.dots = 3
        self.score = 0
        self.reward = 0
        self.action = 0
        self.Q = Q
        self.episode_reward = 0
        self.epsilon = epsilon

        self.training = Config.TRAINING
        # variables used to move snake object
        self.moveX = Config.DOT_SIZE # set initial movement to oright direction
        self.moveY = 0
        # define how much moves max per episode to not get stuck
        self.moveCounter = 0
        self.cutoff = 100
        
        self.loadImages()

        self.createObjects()
        
        #statistics scores
        self.scores = scores
        self.ep_rewards = ep_rewards
        self.moves = moves
        self.epsilons = epsilons
        self.average_snake_length = average_snake_length
        self.num_games = num_games
        self.cumm_rewards = cumm_rewards
        
        self.placeApple()
        self.after(Config.DELAY, self.onTimer)

    def get_actions(self):
        # return all possible actions
        return (0,1,2,3)
    
    def loadImages(self):
        '''loads images from the disk'''

        try:

            self.idot = Image.open("../../Images/dot20.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("../../Images/head20.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("../../Images/apple20.png")
            self.apple = ImageTk.PhotoImage(self.iapple)

        except IOError as e:

            print(e)
            sys.exit(1)


    def createObjects(self):
        '''creates objects on Canvas'''
        
        # set random starting position for head
        r = random.randint((Config.BOARD_WIDTH/Config.DOT_SIZE - Config.MAX_RAND_POS_SNAKE), Config.MAX_RAND_POS_SNAKE)
        self.headX = r * Config.DOT_SIZE
        r = random.randint((Config.BOARD_HEIGHT/Config.DOT_SIZE - Config.MAX_RAND_POS_SNAKE), Config.MAX_RAND_POS_SNAKE)
        self.headY = r * Config.DOT_SIZE
        
        # head is on the rightmost position
        self.create_image(self.headX, self.headY, image=self.head, anchor=NW,  tag="head")
        self.create_image(self.headX - 2*Config.DOT_SIZE, self.headY, image=self.dot, anchor=NW, tag="dot")
        self.create_image(self.headX - Config.DOT_SIZE, self.headY, image=self.dot, anchor=NW, tag="dot")
        
        # starting apple coordinates (have to be different from snake)
        # emulation of a do while loop
        while(True):
            r = random.randint(0, Config.MAX_RAND_POS_APPLE)
            self.appleX = r * Config.DOT_SIZE
            r = random.randint(0, Config.MAX_RAND_POS_APPLE)
            self.appleY = r * Config.DOT_SIZE
            if(self.appleX != self.headX and self.appleY != self.headY):
                break
        
        self.create_text(40, 20, text="Score: {0}".format(self.score),
                         tag="score", fill="black")
        self.create_image(self.appleX, self.appleY, image=self.apple,
            anchor=NW, tag="apple")
        
    def makeScreenshot(self):
        x1 = self.root.winfo_x() + 8
        y1 = self.root.winfo_y() + 30
        x2 = x1 + Config.BOARD_WIDTH
        y2 = y1 + Config.BOARD_HEIGHT
        im = grab(bbox=(x1, y1, x2, y2))
        im.save(f"screenshots2/screen{int(time.time())}.png")

    def checkAppleCollision(self):
        '''checks if head of snake collides with apple'''

        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if apple[0] == ovr:

                self.score += 1
                x, y = self.coords(apple)
                # Add one dot to the snake
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                # relocate the apple
                self.placeApple()
        
        self.reward = Config.GET_APPLE_REWARD # agent won the round


    def moveSnake(self):
        '''moves the Snake object'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        items = dots + head
        
        ("Num of items: ", len(items))
        
        z = 0
        # iterate through all snake items and move them
        while z < len(items)-1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1
            
        self.move(head, self.moveX, self.moveY)
        
        
        if self.moveX == -Config.DOT_SIZE and self.appleX < self.headX: # food left and move left
            self.reward = Config.MOVE_TO_APPLE_REWARD
        elif self.moveX == Config.DOT_SIZE and self.appleX > self.headX: # food right
            self.reward = Config.MOVE_TO_APPLE_REWARD
        elif self.moveY == -Config.DOT_SIZE and self.appleY < self.headY: # food up
            self.reward = Config.MOVE_TO_APPLE_REWARD
        elif self.moveY == Config.DOT_SIZE and self.appleY > self.headY:  # food down
            self.reward = Config.MOVE_TO_APPLE_REWARD
        else:
            self.reward = Config.MOVE_AWAY_REWARD # we want the fastest way so every move decreases reward
            
        self.moveCounter +=1


    def checkCollisions(self):
        '''checks for snake collisions with tail and wall'''

        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for over in overlap:
                if over == dot:
                  self.inGame = False

        if x1 < 0:
            self.inGame = False

        if x1 > Config.BOARD_WIDTH - Config.DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > Config.BOARD_HEIGHT - Config.DOT_SIZE:
            self.inGame = False
        
        self.reward = Config.COLLIDE_REWARD


    def placeApple(self):
        ''' places the apple object on Canvas
            may not be placed where it touches the snake
        '''
        
        dots = self.find_withtag("dot")
        apple = self.find_withtag("apple")
        
        quit_loop = False
        
        # loop to make sure the apple is not placed on the snake
        while(not quit_loop):
            
            self.delete(apple[0])
            
            r = random.randint(0, Config.MAX_RAND_POS_APPLE)
            self.appleX = r * Config.DOT_SIZE
            r = random.randint(0, Config.MAX_RAND_POS_APPLE)
            self.appleY = r * Config.DOT_SIZE
            
            self.create_image(self.appleX, self.appleY, anchor=NW,
            image=self.apple, tag="apple")
            apple = self.find_withtag("apple")
            
            quit_loop = True
            
            x1, y1, x2, y2 = self.bbox(apple)
            overlap = self.find_overlapping(x1, y1, x2, y2)
            
            for dot in dots:
                for over in overlap:
                    if over == dot:
                        quit_loop = False
                        

    def getState(self):
        
        head = self.find_withtag("head")
        dots = self.find_withtag("dot")
        
        self.headX, self.headY = self.coords(head)

        coords = []
        
        items = dots + head
        
        for item in items:
            coords.append(self.coords(item))

        # To check for self collision in all directions compute head position after movements
        head_plus_x = list(map(add, self.coords(head), [Config.IM_SIZE, 0]))
        head_minus_x = list(map(add, self.coords(head), [-Config.IM_SIZE, 0]))
        head_plus_y = list(map(add, self.coords(head), [0, Config.IM_SIZE]))
        head_minus_y = list(map(add, self.coords(head), [0, -Config.IM_SIZE]))
        
        x1, y1, x2, y2 = head_plus_x + list(map(add, head_plus_x, [Config.IM_SIZE, Config.IM_SIZE]))
        right_overlap = self.find_overlapping(x1, y1, x2, y2)
        
        x1, y1, x2, y2 = head_minus_x + list(map(add, head_minus_x, [Config.IM_SIZE, Config.IM_SIZE]))
        left_overlap = self.find_overlapping(x1, y1, x2, y2)
        
        x1, y1, x2, y2 = head_plus_y + list(map(add, head_plus_y, [Config.IM_SIZE, Config.IM_SIZE]))
        down_overlap = self.find_overlapping(x1, y1, x2, y2)
        
        x1, y1, x2, y2 = head_minus_y + list(map(add, head_minus_y, [Config.IM_SIZE, Config.IM_SIZE]))
        up_overlap = self.find_overlapping(x1, y1, x2, y2)
        
        # Initially state variables are False
        self_collision_right = False
        self_collision_left = False
        self_collision_down = False
        self_collision_up = False
                
        # check for collisions with positions after movement
        for dot in dots:
            for over in right_overlap:
                if over == dot:
                    self_collision_right = True
            for over in left_overlap:
                if over == dot:
                    self_collision_left = True
            for over in down_overlap:
                if over == dot:
                    self_collision_down= True
            for over in up_overlap:
                if over == dot:
                    self_collision_up= True
                  
        # 3 possible directions to move (snake can't go backwards)
        # states include: - danger of hitting a wall in the current direction
        #                 - current direction of movement
        #                 - chance of getting food when moving in one direction
        state = [
            (self.moveX == Config.IM_SIZE and self.moveY == 0 and 
                    ((head_plus_x in coords) or
            self.headX + Config.IM_SIZE >= (Config.BOARD_WIDTH - Config.IM_SIZE))) or 
                    (self.moveX == -Config.IM_SIZE and self.moveY == 0 and 
                    ((head_minus_x in coords) or
            self.headX - Config.IM_SIZE < Config.IM_SIZE)) or (self.moveX == 0 
                    and self.moveY == -Config.IM_SIZE and 
                    ((head_minus_y in coords) or
            self.headY - Config.IM_SIZE < Config.IM_SIZE)) or (self.moveX == 0 and 
                    self.moveY == Config.IM_SIZE and 
                    ((head_plus_y in coords) or
            self.headY + Config.IM_SIZE >= (Config.BOARD_HEIGHT-Config.IM_SIZE))),  # danger straight

            (self.moveX == 0 and self.moveY == -Config.IM_SIZE and 
                     ((list(map(add,self.coords(head),[Config.IM_SIZE, 0])) in coords) or
            self.headX + Config.IM_SIZE > (Config.BOARD_WIDTH-Config.IM_SIZE))) or 
                    (self.moveX == 0 and self.moveY == Config.IM_SIZE and ((list(map(add,self.coords(head), 
                    [-Config.IM_SIZE,0])) in coords) or self.headX - Config.IM_SIZE < Config.IM_SIZE)) or 
                    (self.moveX == -Config.IM_SIZE and self.moveY == 0 and 
                     ((list(map(add,self.coords(head),[0,-Config.IM_SIZE])) in coords) or 
                      self.headY - Config.IM_SIZE < Config.IM_SIZE)) or (self.moveX == Config.IM_SIZE and self.moveY == 0 and 
                    ((list(map(add,self.coords(head),[0,Config.IM_SIZE])) in coords) or self.coords(head)[
             -1] + Config.IM_SIZE >= (Config.BOARD_HEIGHT-Config.IM_SIZE))),  # danger right

             (self.moveX == 0 and self.moveY == Config.IM_SIZE and 
                  ((list(map(add,self.coords(head),[Config.IM_SIZE,0])) in coords) or
             self.headX + Config.IM_SIZE > (Config.BOARD_WIDTH-Config.IM_SIZE))) or (self.moveX == 0 and self.moveY == -Config.IM_SIZE and ((list(map(
             add, self.coords(head),[-Config.IM_SIZE,0])) in coords) or 
                 self.headX - Config.IM_SIZE < Config.IM_SIZE)) or 
                 (self.moveX == Config.IM_SIZE and self.moveY == 0 and
                 ((list(map(add,self.coords(head),[0,-Config.IM_SIZE])) in coords) or 
                self.headY - Config.IM_SIZE < Config.IM_SIZE)) or (self.moveX == -Config.IM_SIZE and self.moveY == 0 and 
                ((list(map(add,self.coords(head),[0,Config.IM_SIZE])) in coords) or
            self.headY + Config.IM_SIZE >= (Config.BOARD_HEIGHT-Config.IM_SIZE))), #danger left

            self_collision_right,
            self_collision_left,
            self_collision_down, 
            self_collision_up,
            self.moveX == -Config.IM_SIZE,  # move left
            self.moveX == Config.IM_SIZE,  # move right
            self.moveY == -Config.IM_SIZE,  # move up
            self.moveY == Config.IM_SIZE,  # move down
            self.appleX < self.headX,  # food left
            self.appleX > self.headX,  # food right
            self.appleY < self.headY,  # food up
            self.appleY > self.headY  # food down
            ]

        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0

        return str(np.asarray(state))


    def setAction(self):
        '''controls direction variables'''
        # if chosen direction is not possible it will stay the same
                
        # epsilon-greedy action selection if in training mode
        if random.uniform(0, 1) < self.epsilon and self.training == True:
            # if number < ε: randomly choose one of four actions
            self.action = random.randint(0, 3) 
        else:
            # if number > ε: perform action for which the Q value is max
            self.action = self.Q.max_action(self.state, self.get_actions())
        
        if self.action == 0 and self.moveX <= 0: # left cursor key
            self.moveX = -Config.DOT_SIZE
            self.moveY = 0

        
        if self.action == 1 and self.moveX >= 0: # up cursor key
            self.moveX = Config.DOT_SIZE
            self.moveY = 0

        
        if self.action == 2 and self.moveY <= 0: # right cursor key
            self.moveX = 0
            self.moveY = -Config.DOT_SIZE

        
        if self.action == 3 and self.moveY >= 0: # down cursor key
            self.moveX = 0
            self.moveY = Config.DOT_SIZE


    def onTimer(self):
        '''creates a game cycle each timer event'''
        
        self.state = self.getState()
        # calculate q value for current state
        q_old = self.Q.get_value(self.state, self.action)
        self.drawScore()
        self.checkCollisions()
        
        # cumulate reward for the episode    
        self.episode_reward += self.reward

        if self.inGame:
            
            # perform action
            self.checkAppleCollision()
            self.setAction()
            self.moveSnake()
            
            if self.training:
                # get new state after moving
                new_state = self.getState()
                
                # calculate action for which the q function for new state is max
                next_max_action = self.Q.max_action(new_state, self.get_actions())
                
                # get the q value for the max action 
                q_next = self.Q.get_value(new_state, next_max_action)
                
                # assign q value from new state after performing action to action state 
                q_new = q_old + Config.ALPHA * (self.reward + Config.GAMMA * q_next - q_old)
                self.Q.set_value(self.state, self.action, q_new)
                
            else:
                # To make an animation of test run
                if Config.SCREENSHOT:
                    self.makeScreenshot()
            
            # check if critical number of actions is reached to not get stuck
            if self.moveCounter >= self.cutoff and self.score < 5: # only for small scores
                self.inGame = False
                
            self.after(Config.DELAY, self.onTimer)
        else:
            self.gameOver()
            global Q_t
            Q_t = self.Q # Q table of this episode is saved in global for next
        
    def drawScore(self):
        '''draws score'''
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))


    def gameOver(self):
        '''deletes all objects and draws game over message'''

        self.delete(ALL)
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,
            text="Game Over with score {0}".format(self.score), fill="black")
        
        # decayed-epsilon-greedy method
        if Config.EPSILON_VARIATION == 1:
            self.epsilon = self.Q.epsilon_decay_one(self.epsilon, Config.EPSILON_DECAY_ONE_VALUE)
        if Config.EPSILON_VARIATION == 2:
            self.epsilon = self.Q.epsilon_decay_two(self.num_games, Config.EPSILON_DECAY_TWO_VALUE)
        if Config.EPSILON_VARIATION == 3:
            self.epsilon = Config.EPSILON_STEADY_VALUE
            
        # save stats
        self.scores.append(self.score)
        self.ep_rewards.append(self.episode_reward)
        self.moves.append(self.moveCounter)
        self.epsilons.append(self.epsilon)

        # quit tkinter window
        self.quit()
   
    def getStats(self):
        return self.Q, self.scores, self.ep_rewards, self.moves, self.epsilon, self.epsilons, self.average_snake_length, self.num_games, self.cumm_rewards

#%%
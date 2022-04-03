# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:50:20 2022

@author: korte
"""

import matplotlib.pyplot as plt
from Config import Config
import numpy as np

def training_stats(aggr_ep_rewards, aggr_scores, aggr_moves, episode, scores, ep_rewards, moves, epsilon, epsilons, average_snake_length, cumm_rewards):
    average_scores = sum(scores[-Config.STATS_EVERY:])/Config.STATS_EVERY
    average_snake_length.append(np.average(scores) + 3)
    aggr_scores['ep'].append(episode)
    aggr_scores['avg'].append(average_scores)
    aggr_scores['max'].append(max(scores[-Config.STATS_EVERY:]))
    aggr_scores['min'].append(min(scores[-Config.STATS_EVERY:]))
    print(f'Episode {episode:>5d} Average score {average_scores:>4.2f} with ε {epsilon:>4.4f}')
    
    average_moves = sum(moves[-Config.STATS_EVERY:])/Config.STATS_EVERY
    aggr_moves['ep'].append(episode)
    aggr_moves['avg'].append(average_moves)
    aggr_moves['max'].append(max(moves[-Config.STATS_EVERY:]))
    aggr_moves['min'].append(min(moves[-Config.STATS_EVERY:]))
    # print("Episode", episode, "Average moves:", average_moves)
    
    average_reward = sum(ep_rewards[-Config.STATS_EVERY:])/Config.STATS_EVERY
    cumm_rewards.append(np.average(ep_rewards))
    aggr_ep_rewards['ep'].append(episode)
    aggr_ep_rewards['avg'].append(average_reward)
    aggr_ep_rewards['max'].append(max(ep_rewards[-Config.STATS_EVERY:]))
    aggr_ep_rewards['min'].append(min(ep_rewards[-Config.STATS_EVERY:]))
    # print(f'Episode: {episode:>5d}, Average reward: {average_reward:>4.1f}')
    
def testing_stats(test_ep_rewards, test_scores, test_moves, run, scores, ep_rewards, moves):
    average_scores = sum(scores[-Config.STATS_EVERY:])/Config.STATS_EVERY
    test_scores['ep'].append(run)
    test_scores['avg'].append(average_scores)
    test_scores['max'].append(max(scores[-Config.STATS_EVERY:]))
    test_scores['min'].append(min(scores[-Config.STATS_EVERY:]))
    print("Run", run, "Average score:", average_scores)
    
    average_moves = sum(moves[-Config.STATS_EVERY:])/Config.STATS_EVERY
    test_moves['ep'].append(run)
    test_moves['avg'].append(average_moves)
    test_moves['max'].append(max(moves[-Config.STATS_EVERY:]))
    test_moves['min'].append(min(moves[-Config.STATS_EVERY:]))
    
    average_reward = sum(ep_rewards[-Config.STATS_EVERY:])/Config.STATS_EVERY
    test_ep_rewards['ep'].append(run)
    test_ep_rewards['avg'].append(average_reward)
    test_ep_rewards['max'].append(max(ep_rewards[-Config.STATS_EVERY:]))
    test_ep_rewards['min'].append(min(ep_rewards[-Config.STATS_EVERY:]))
    
def plot_stats(aggr_ep_rewards, aggr_scores, aggr_moves, cumm_rewards, average_snake_length, test_ep_rewards, test_scores, test_moves):
    ## TRAINING STATS
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min rewards")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(aggr_scores['ep'], aggr_scores['avg'], label="average scores")
    plt.plot(aggr_scores['ep'], aggr_scores['max'], label="max scores")
    plt.plot(aggr_scores['ep'], aggr_scores['min'], label="min scores")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(aggr_moves['ep'], aggr_moves['avg'], label="average moves")
    plt.plot(aggr_moves['ep'], aggr_moves['max'], label="max moves")
    plt.plot(aggr_moves['ep'], aggr_moves['min'], label="min moves")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
    plt.plot(aggr_scores['ep'], aggr_scores['avg'], label="average scores")
    plt.plot(aggr_moves['ep'], aggr_moves['avg'], label="average moves")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(aggr_ep_rewards['ep'], cumm_rewards, label="average cummulated rewards")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(aggr_scores['ep'], average_snake_length, label="average snake length")
    plt.legend(loc=4)
    plt.show()
    
    ## TESTING STATS
    plt.plot(test_ep_rewards['ep'], test_ep_rewards['avg'], label="average test rewards")
    plt.plot(test_ep_rewards['ep'], test_ep_rewards['max'], label="max test rewards")
    plt.plot(test_ep_rewards['ep'], test_ep_rewards['min'], label="min test rewards")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(test_scores['ep'], test_scores['avg'], label="average test scores")
    plt.plot(test_scores['ep'], test_scores['max'], label="max test scores")
    plt.plot(test_scores['ep'], test_scores['min'], label="min test scores")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(test_moves['ep'], test_moves['avg'], label="average test moves")
    plt.plot(test_moves['ep'], test_moves['max'], label="max test moves")
    plt.plot(test_moves['ep'], test_moves['min'], label="min test moves")
    plt.legend(loc=4)
    plt.show()
    
    plt.plot(test_ep_rewards['ep'], test_ep_rewards['avg'], label="average test rewards")
    plt.plot(test_scores['ep'], test_scores['avg'], label="average test scores")
    plt.plot(test_moves['ep'], test_moves['avg'], label="average test moves")
    plt.legend(loc=4)
    plt.show()
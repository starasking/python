'''
Auther: Xuemei Wang
'''

import numpy as np
import random

GAMMA = 1.0
EPSILON = 1.0E-5
Lake = np.array([['S', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
                 ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
                 ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'F'],
                 ['F', 'F', 'F', 'F', 'F', 'H', 'F', 'F'],
                 ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'F'],
                 ['F', 'H', 'H', 'F', 'F', 'F', 'H', 'F'],
                 ['F', 'H', 'F', 'F', 'H', 'F', 'H', 'F'],
                 ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'G']])
ROWS = Lake.shape[0]
COLS = Lake.shape[1]
ACTIONS = ['up', 'down', 'left', 'right']
PROB = 0.7
random.seed(0)

def sample_action():
    return np.array([[random.choice(ACTIONS) for i in range(ROWS)] for j in range(COLS)])

def get_next_location(location, action):
    row = location[0]
    col = location[1]
    if action == 'up':
        return (max(row - 1, 0), col)
    if action == 'down':
        return (min(row + 1, ROWS - 1), col)
    if action == 'left':
        return (row, max(col - 1, 0))
    if action == 'right':
        return (row, min(col + 1, COLS - 1))

def get_next_prob_location(location, action):
    row = location[0]
    col = location[1]
    prob = (1.0 - PROB)/3.0

    result = {(max(row - 1, 0), col): prob, \
              (min(row + 1, ROWS -1), col): prob, \
              (row, max(col - 1, 0)): prob, \
              (row, min(col + 1, COLS - 1)): prob}
    next_location = get_next_location(location, action)
    result[next_location] = PROB
    return result

def get_prob_reward(location):
    row = location[0]
    col = location[1]
    result = {(max(row - 1, 0), col): get_reward((max(row - 1, 0), col)), \
              (min(row + 1, ROWS -1), col): get_reward((min(row + 1, ROWS -1), col)), \
              (row, max(col - 1, 0)): get_reward((row, max(col - 1, 0))), \
              (row, min(col + 1, COLS - 1)): get_reward((row, min(col + 1, COLS - 1)))}
    return result

def get_prob_value(location, V_input):
    row = location[0]
    col = location[1]
    result = 0.0
    result = {(max(row - 1, 0), col): V_input[(max(row - 1, 0), col)], \
              (min(row + 1, ROWS -1), col):  V_input[(min(row + 1, ROWS -1), col)], \
              (row, max(col - 1, 0)): V_input[(row, max(col - 1, 0))], \
              (row, min(col + 1, COLS - 1)): V_input[(row, min(col + 1, COLS - 1))]}
    return result

def get_reward(location):
    row = location[0]
    col = location[1]
    if Lake[row][col] == 'H':
        return -1
    elif Lake[row][col] == 'G':
        return 1
    return 0


def get_action_reward(location, action):
    row = location[0]
    col = location[1]
    if Lake[row][col] == 'H':
        return -1
    if Lake[row][col] == 'G':
        return 1
    if row == 0 and action == 'up':
        return -1
    if row == (ROWS -1) and action == 'down':
        return -1
    if col == 0 and action == 'left':
        return -1
    if col == (COLS -1) and action == 'right':
        return -1
    return 0


def policy_evaluate(pi, V):
    dis_max = 1.0
    result = V.copy()
    while(dis_max > EPSILON):
        dis_max = 0.0
        for row in range(V.shape[0]):
            for col in range(V.shape[1]):
                location = (row, col)
                action = pi[location]
                next_prob_locations = get_next_prob_location(location, action)
                reward = get_action_reward(location, action)
                result[location] = reward
                for next_location in next_prob_locations.keys():
                    prob = next_prob_locations[next_location]
                    value = V[next_location]
                    result[location] += prob * GAMMA * value
                if abs(result[location] - V[location]) > dis_max:
                    dis_max = abs(result[location] - V[location])
                #print(dis_max)
        V = result.copy()
    return result

def policy_improve(pi, V):
    V_update = V.copy()
    pi_update = pi.copy()
    for row in range(ROWS):
        for col in range(COLS):
            location = (row, col)
            pi_star = pi[location]
            reward = -100.0
            for action in ACTIONS:
                next_prob_locations = get_next_prob_location(location, action)
                Q =get_action_reward(location, action)
                for next_location in next_prob_locations.keys():
                    prob = next_prob_locations[next_location]
                    value = V[next_location]
                    Q += prob * GAMMA * value
                #print(reward, Q)
                #print(pi_update)
                if reward < Q:
                    reward = Q
                    pi_star = action
            V_update[location] = reward
            pi_update[location] = pi_star
   
            #print(pi_update)
            #input("pause")
    return(V_update, pi_update)

def policy_iterate():
    #initialize
    V = np.array([[0 for i in range(ROWS)] for j in range(COLS)], dtype = np.float64)
    pi = sample_action()

    # iterate
    threshold = 5000
    i = 0
    while i < threshold:
        i += 1
        # policy valuation
        V_new = policy_evaluate(pi, V)
        print("======================")
        print(i)
        print(pi)
        print(V)

        # update policy
        (V_update, pi_update) = policy_improve(pi, V_new)
        print(Lake)
        print(pi_update)
        print(V_update)
        #input("pause")
        if np.array_equal(pi_update, pi):
            return (V, pi)
        else:
            V = V_update.copy()
            pi = pi_update.copy()
    return (V, pi)
policy_iterate()

'''
Auther: Xuemei Wang
'''

import numpy as np
import random

GAMMA = 0.5
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
    if Lake[row][col] == 'G':
        return 1
    return 0
'''

def get_reward(location, action):
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
'''

#def get_return(location, action):
    #next_location = get_next_location(location, action)
    #value = get_reward(location, action)[1]
    #return (next_location, value)

def policy_evaluate(pi, V):
    dis_max = 1.0
    result = V.copy()
    print(V)
    print(pi)
    while(dis_max > EPSILON):
        dis_max = 0.0
        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                action = pi[i][j]
                next_prob_locations = get_next_prob_location((i, j), action)
                next_prob_rewards = get_prob_reward((i, j))
                for location in next_prob_locations.keys():
                    prob = next_prob_locations[location]
                    r = next_prob_rewards[location]
                    value = V[location]
                    result[i][j] += prob * ( r + GAMMA * value)
                    print(action, prob, r, value)
                if (result[i][j] - V[i][j]) > dis_max:
                    dis_max = abs(result[i][j] - V[i][j])
                print(Lake)
                print(pi)
                print(result)
        input("pause")
        V = result.copy()
    return result

def policy_improve(pi, V):
    V_update = V.copy()
    pi_update = pi.copy()
    for row in range(ROWS):
        for col in range(COLS):
            location = (row, col)
            value_star = V[location]
            pi_star = pi[location]
            for action in ACTIONS:
                next_prob_locations = get_next_prob_location(location, action)
                next_prob_rewards = get_prob_reward(location)
                Q = 0
                for next_location in next_prob_locations.keys():
                    prob = next_prob_locations[next_location]
                    r = next_prob_rewards[next_location]
                    value = V[next_location]
                    Q += prob * (r + GAMMA * value)
                #Q = R + GAMMA * v
                if value_star < Q:
                    value_star = Q
                    pi_star = action
            print(pi)
            V_update[location] = value_star
            pi[location] = pi_star
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
        V = V_new
        print(i)
        print(V)

        # update policy
        (V_update, pi_update) = policy_improve(pi, V)
        print("======================")
        print(pi_update)
        print(pi)
        if np.array_equal(pi_update, pi):
            return (V, pi)
        else:
            V = V_update
            pi = pi_update
    return (V, pi)
policy_iterate()

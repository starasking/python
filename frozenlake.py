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

def get_prob_return(location):
    row = location[0]
    col = location[1]
    result = {(max(row - 1, 0), col): is_terminated(location, 'up')[1], \
              (min(row + 1, ROWS -1), col): is_terminated(location, 'down')[1], \
              (row, max(col - 1, 0)): is_terminated(location, 'left')[1], \
              (row, min(col + 1, COLS - 1)): is_terminated(location, 'right')[1]}
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

def is_terminated(location, action):
    row = location[0]
    col = location[1]
    if Lake[row][col] == 'H':
        return (1, -1)
    if Lake[row][col] == 'G':
        return (1, 1)
    if row == 0 and action == 'up':
        return (1, -1)
    if row == (ROWS -1) and action == 'down':
        return (1, -1)
    if col == 0 and action == 'left':
        return (1, -1)
    if col == (COLS -1) and action == 'right':
        return (1, -1)
    return (0, 0)

def get_return(location, action):
    next_location = get_next_location(location, action)
    value = is_terminated(location, action)[1] 
    return (next_location, value)

def policy_evaluate(pi, V):
    dis_max = 1.0
    result = V.copy()
    while(dis_max > EPSILON):
        dis_max = 0.0
        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                action = pi[i][j]
                prob_locations = get_next_prob_location((i, j), action)
                prob_returns = get_prob_return((i, j))
                for next_location in prob_locations.keys():
                    prob = prob_locations[next_location]
                    r = prob_returns[next_location]
                    value = V[next_location]
                    result[i][j] = prob * ( r + GAMMA * value)
                    if (result[i][j] - V[i][j]) > dis_max:
                        dis_max = abs(result[i][j] - V[i][j])
                print(i, j, dis_max)
                #input("pause")
        V = result.copy()
    return result

def policy_improve(pi, V):
    V_update = V
    pi_update = pi
    for row in range(ROWS):
        for col in range(COLS):
            value = V[location]
            pi_star = pi[location]
            for action in ACTIONS:
                location = (row, col)
                next_prob_locations = get_next_prob_location(location, action)
                next_prob_returns = get_prob_return(location)
                next_prob_values = get_prob_value(location, V)
                Q = 0
                for location in next_prob_locations.keys():
                    Q += next_prob_locations[location] * (next_prob_returns[location] + \
                            GAMMA * next_prob_values[location])
                #Q = R + GAMMA * v
                if value < Q:
                    value = Q
                    pi_star = action
            print(pi)
            V_update[location] = value
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
        if pi_update == pi:
            return (V, pi)
        else:
            V = V_update
            pi = pi_update
    return (V, pi)
policy_iterate()

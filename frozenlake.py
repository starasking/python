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

def policy_evaluate(pi, V):
    dis_max = 1.0
    result = V.copy()
    while(dis_max > EPSILON):
        dis_max = 0.0
        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                action = pi[i][j]
                prob_location = get_next_prob_location((i, j), action)
                R = get_return((i, j), action)
                for next_location in prob_location.keys():
                    prob = prob_location[next_location]
                    r = R[next_location]
                    value = V(next_location)
                    retult[i][j] = prob * ( r + GAMMA * value)
                    if (result[i][j] - V[i][j]) > dis_max:
                        dis_max = abs(result[i][j] - V[i][j])
        V = result.copy()
    return result

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

def get_prob_value(location, action, V_input):
    row = location[0]
    col = location[1]
    prob = np.full(4, (1.0 - PROB)/3.0)
    prob[ACTIONS.index(action)] = PROB
    result = 0.0
    for i in range(len(ACTIONS)):
        result += prob[i] * V_input[get_next_location(location, ACTIONS[i])]
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

def policy_improve(pi, V):
    for row in range(ROWS):
        for col in range(COLS):
            for action in ACTIONS:
                location = (row, col)
                R = is_terminated(location, action)[1]
                next_location = get_location(location, action)
                Q = R + GAMMA * V[next_location]
                # TODO: change to probability expression
                #v = get_prob_value(location, action, V)
                #Q = R + GAMMA * v
                if V[location] < Q:
                    V[location] = Q
                    pi[location] = action
    print(V)
    print(pi)
    print(V)
    print(pi)
    #if np.array_equal(V, V):
    if np.array_equal(pi, pi):
        break
    V = V
    pi = pi

def policy_iterate():
    #initialize
    V = np.array([[0 for i in range(ROWS)] for j in range(COLS)], dtype = np.float64)
    pi = sample_action()
    print(V)
    print(pi)

    # iterate
    while True:
        # policy valuation
        V_new = policy_evaluate(pi, V)
        V = V_new


        while len(trajectory) > 0:
            location = trajectory.pop()
            V[location] = value * GAMMA
            value = V[location]

        # update policy
        V_next = np.copy(V)
        pi_next = np.copy(pi)

        for row in range(ROWS):
            for col in range(COLS):
                for action in ACTIONS:
                    location = (row, col)
                    R = is_terminated(location, action)[1]
                    next_location = get_next_location(location, action)
                    Q = R + GAMMA * V[next_location]
                    # TODO: change to probability expression
                    #v_next = get_prob_value(location, action, V)
                    #Q = R + GAMMA * v_next
                    if V_next[location] < Q:
                        V_next[location] = Q
                        pi_next[location] = action
        print(V)
        print(pi)
        print(V_next)
        print(pi_next)
        #if np.array_equal(V_next, V):
        if np.array_equal(pi_next, pi):
            break
        V = V_next
        pi = pi_next
    return (V, pi)
policy_iterate()

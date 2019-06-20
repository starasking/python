'''
Auther: Xuemei Wang
'''

import numpy as np
import random

GAMMA = 0.5
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

def get_prob_value(location, action, V_input):
    row = location[0]
    col = location[1]
    prob = np.full(4, (1.0 - PROB)/3.0)
    prob[ACTIONS.index(action)] = PROB
    result = 0.0
    for i in range(len(ACTIONS)):
        result += prob[i] * V_input[get_next_location(location, ACTIONS[i])]
    return result


def get_next_prob_location(location, action_intend):
    action = action_intend
    row = location[0]
    col = location[1]
    prob = np.full(4, (1.0 - PROB)/3.0)
    prob[ACTIONS.index(action_intend)] = PROB

    bias = 0.0
    random_number = random.uniform(0, 1)
    for i in range(len(prob)):
        prob[i] += bias
        bias = prob[i]
        if random_number < prob[i]:
            action = ACTIONS[i]
            break

    if action == 'up':
        return (max(row - 1, 0), col)
    if action == 'down':
        return (min(row + 1, ROWS - 1), col)
    if action == 'left':
        return (row, max(col - 1, 0))
    if action == 'right':
        return (row, min(col + 1, COLS - 1))

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

def policy_iterate():
    #initialize
    V = np.array([[0 for i in range(ROWS)] for j in range(COLS)], dtype = np.float64)
    pi = sample_action()
    print(V)
    print(pi)

    # iterate
    while True:
        # update value
        trajectory = []
        start = (0, 0)
        current = start
        terminated = (is_terminated(current, pi[current])[0] == 1)

        while not terminated:
            # break inner loop
            if current in set(trajectory):
                value = -1.0
                V[current] = value
                break

            trajectory.append(current)
            print(trajectory)
            current = get_next_location(current, pi[current])
            #current = get_next_prob_location(current, pi[current])
            terminated = (is_terminated(current, pi[current])[0] == 1)

        value = is_terminated(current, pi[current])[1]
        V[current] = value

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

# Auther: Xuemei Wang
# Created date: 2019-07-04
# Copyright: Xuemei Wang

import math

def checkLine(idx, add_lines, lines, keyword):
    idx += add_lines
    line = lines[idx]
    assert(line.startswith(keyword))
    values = line.split('=')[1].split('\n')[0].split(' ')
    return(idx, values)

class Tree():
    def __init__(self, id, split_feature = "", \
            threshold = 0.0, is_leave = False, value = 0.0):
        self.id = id
        self.split_feature = split_feature
        self.threshold = threshold
        self.is_leave = is_leave
        self.value = value
        self.left = None
        self.right = None

def buildTree(split_feature, threshold, left_child, right_child, leaf_value):
    assert(len(split_feature) == len(threshold))
    assert(len(left_child) == len(threshold))
    assert(len(left_child) == len(right_child))
    assert(len(left_child) + 1 == len(leaf_value))

    root_split_feature = split_feature.pop(0)
    root_threshold = threshold.pop(0)
    root = Tree(0, root_split_feature, root_threshold)
    branches = [root]

    for i in range(len(left_child)):
        #print(i)
        left_id = left_child[i]
        left = Tree(left_id)
        if left_id < 0:
            left.is_leave = True
            left.value = leaf_value.pop(0)
        right_id = right_child[i]
        right = Tree(right_id)
        if right_id < 0:
            right.is_leave = True
            right.value = leaf_value.pop(0)

        branch = None
        while len(branches) > 0:
            branch = branches.pop(0)
            if branch.is_leave:
                branch = branches.pop(0)
            else:
                break
        if branch == None:
            assert(len(branches) == 0)
            break
        else:
            if not left.is_leave:
                branches.append(left)
                assert(len(split_feature) > 0)
                left.split_feature = split_feature.pop(0)
                left.threshold = threshold.pop(0)
            branch.left = left

            if not right.is_leave:
                branches.append(right)
                assert(len(split_feature) > 0)
                right.split_feature = split_feature.pop(0)
                right.threshold = threshold.pop(0)
            branch.right = right
    return root

    
def readLightGBM(file):
    forest = []
    with open(file) as infile:
        lines = infile.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('feature_names'):
               features = line.split('=')[1].split('\n')[0].split(' ')
               #print(features[:20])
            if line.startswith('Tree='):
                #print('\n')
                #print(line.split('\n')[0]) 
                (idx, split_feature) = checkLine(i, 3, lines, 'split_feature')
                i = idx
                split_feature = list(map(int, split_feature))
                #print(split_feature)

                (idx, threshold) = checkLine(i, 2, lines, 'threshold')
                i = idx
                threshold = list(map(float, threshold))
                #print(threshold[:5])

                (idx, left_child) = checkLine(i, 2, lines, 'left_child')
                i = idx
                left_child = list(map(int, left_child))
                #print(left_child[:5])

                (idx, right_child) = checkLine(i, 1, lines, 'right_child')
                i = idx
                right_child = list(map(int, right_child))
                #print(right_child[:5])

                (idx, leaf_value) = checkLine(i, 1, lines, 'leaf_value')
                leaf_value = list(map(float, leaf_value))
                #print(leaf_value[:5])
                #print(leaf_value)

                #print(len(split_feature), len(threshold), \
                        #len(left_child), len(right_child), \
                        #len(leaf_value))
                #input("pause")
                tree = buildTree(split_feature, threshold, \
                        left_child, right_child, leaf_value)
                forest.append(tree)
            i += 1
    return (features, forest)


(features, forest) = readLightGBM("lightgbm.txt")

def readInput(file):
    inputs = []
    with open(file) as infile:
        lines = infile.readlines()
    head = lines[0].split('\n')[0].split(',')
    head[0] = 'click'
    for i in range(1, len(lines)):
        line = lines[i].split('\n')[0].split(',')
        line = list(map(float, line))
        inputs.append(line)
    return (head, inputs)

#print(len(forest))
(head, inputs) = readInput('sample.csv')
assert(head == features)

sample = inputs[0]
tree = forest[0]

def printTree(tree):
    if not tree.is_leave:
        print(tree.id, tree.split_feature, tree.threshold, \
                tree.is_leave, tree.left.id, tree.right.id)
        printTree(tree.left)
        printTree(tree.right)
    else:
        print(tree.id, tree.split_feature, tree.threshold, \
                tree.is_leave, tree.value)

#printTree(tree)

def sigmoid(x):
    return 1.0/(1.0 + math.exp(-x))

def predict(forest, sample):
    result = 0
    for tree in forest:
        while not tree.is_leave:
            value = sample[tree.split_feature]
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result += tree.value
    return sigmoid(result)

def predict_2(forest, sample):
    result = 0
    for tree in forest:
        while not tree.is_leave:
            value = sample[tree.split_feature]
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result += sigmoid(tree.value)
    return result/300.0

def predict_all(forest, inputs):
    result = []
    for sample in inputs:
        prediction = predict(forest, sample)
        result.append(prediction)
    return result
        
prediction = predict(forest, sample)
prediction_2 = predict_2(forest, sample)
prediction_all = predict_all(forest, inputs)
#print(prediction)
#print(prediction_2)
for item in prediction_all:
    print(item)
#print(prediction_all)

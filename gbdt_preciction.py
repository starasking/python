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

    root_split_feature = split_feature[0]
    root_threshold = threshold[0]
    root = Tree(0, root_split_feature, root_threshold)

    branches = [root]
    waiting_list = [root.id]

    for i in range(len(left_child)):

        assert(len(waiting_list) > 0)
        assert(len(branches) > 0)
        #print(waiting_list)
        current_id = min(waiting_list)

        branch = None
        for item in branches:
            if item.id == current_id:
                waiting_list.remove(current_id)
                branch = item
                branches.remove(item)
                break

        #print(features[split_feature[current_id]])
        #print(current_id)
        #input("pause")
        left_id = left_child[i]
        left = Tree(left_id)
        if left_id < 0:
            left.is_leave = True
            left.value = leaf_value.pop(0)
            #print(left_child[:i])
            #input("pause")
        else:
            waiting_list.append(left.id)
            branches.append(left)

        right_id = right_child[i]
        right = Tree(right_id)
        if right_id < 0:
            right.is_leave = True
            right.value = leaf_value.pop(0)
            #print(right_child[:i])
            #input("pause")
        else:
            waiting_list.append(right.id)
            branches.append(right)
        
        # TODO
        assert(branch != None)

        if not left.is_leave:
            assert(len(split_feature) > 0)
            left.split_feature = split_feature[left.id]
            left.threshold = threshold[left.id]
            #print(left.id, left.split_feature, left.threshold, left.is_leave)
        branch.left = left

        if not right.is_leave:
            assert(len(split_feature) > 0)
            right.split_feature = split_feature[right.id]
            right.threshold = threshold[right.id]
            #print(right.id, right.split_feature, right.threshold, right.is_leave)
        branch.right = right
    return root
    
def readLightGBM(file):
    forest = []
    weight = []
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
                #print("tree =",int(line.split('\n')[0].split('=')[1]) + 1) 
                (idx, split_feature) = checkLine(i, 3, lines, 'split_feature')
                i = idx
                split_feature = list(map(int, split_feature))
                #print(split_feature[:50])
                #for j in range(len(split_feature)):
                    #print(split_feature[j], features[split_feature[j]])
                (idx, threshold) = checkLine(i, 2, lines, 'threshold')
                i = idx
                threshold = list(map(float, threshold))
                #print(threshold[:20])

                (idx, left_child) = checkLine(i, 2, lines, 'left_child')
                i = idx
                left_child = list(map(int, left_child))
                #print(left_child[64:128])
                #input("pause")

                (idx, right_child) = checkLine(i, 1, lines, 'right_child')
                i = idx
                right_child = list(map(int, right_child))
                #print(right_child[:20])

                (idx, leaf_value) = checkLine(i, 1, lines, 'leaf_value')
                leaf_value = list(map(float, leaf_value))
                #print(leaf_value[:20])

                (idx, shrinkage) = checkLine(i, 5, lines, 'shrinkage')
                weight.append(float(shrinkage[0]))
                #print(shrinkage)

                #print(len(split_feature), len(threshold), \
                        #len(left_child), len(right_child), \
                        #len(leaf_value))
                #input("pause")
                '''
                print(features[split_feature[0]], features[split_feature[2]], \
                        features[split_feature[1]], features[split_feature[3]], \
                        features[split_feature[6]], features[split_feature[4]], \
                        features[split_feature[5]], features[split_feature[9]], \
                        features[split_feature[8]], features[split_feature[14]], \
                        features[split_feature[13]], features[split_feature[7]], \
                        features[split_feature[10]], features[split_feature[21]], \
                        features[split_feature[19]])
                print(features[split_feature[0]], features[split_feature[2]], \
                        features[split_feature[1]], features[split_feature[4]], 
                        features[split_feature[5]], features[split_feature[3]], \
                        features[split_feature[6]], features[split_feature[21]], \
                        features[split_feature[19]], features[split_feature[7]], 
                        features[split_feature[10]], features[split_feature[14]], \
                        features[split_feature[13]], features[split_feature[9]], 
                        features[split_feature[8]])
                print(features[split_feature[0]], \
                        features[split_feature[2]], features[split_feature[1]], \
                        features[split_feature[4]], features[split_feature[5]], \
                        features[split_feature[3]], features[split_feature[6]], \
                        features[split_feature[14]], features[split_feature[13]], \
                        features[split_feature[7]], features[split_feature[10]], \
                        features[split_feature[9]], features[split_feature[8]], \
                        features[split_feature[21]], features[split_feature[19]], \
                        features[split_feature[84]], features[split_feature[16]], \
                        features[split_feature[15]], features[split_feature[31]], \
                        features[split_feature[28]], features[split_feature[12]], \
                        features[split_feature[70]], features[split_feature[24]], \
                        features[split_feature[56]], features[split_feature[11]], \
                        features[split_feature[17]], features[split_feature[37]], \
                        features[split_feature[49]], features[split_feature[16]], \
                        features[split_feature[29]], features[split_feature[23]])
                input("pause")
                '''
                tree = buildTree(split_feature, threshold, \
                        left_child, right_child, leaf_value)
                forest.append(tree)
            i += 1
    return (features, forest, weight)

(features, forest, weight) = readLightGBM("lightgbm.txt")

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
assert(len(sample) == len(features))
for i in range(len(sample)):
    print(sample[i], features[i])
tree = forest[0]

def printTree(tree, features):
    if not tree.is_leave:
        print(tree.id, features[tree.split_feature], tree.threshold, \
                tree.is_leave, tree.left.id, tree.right.id)
        #input("pause")
        printTree(tree.right, features)
        printTree(tree.left, features)
    else:
        print(tree.id, tree.threshold, \
                tree.is_leave, tree.value)

printTree(tree, features)

def findLeave(forest, sample, features):
    result = []
    for tree in forest:
        while not tree.is_leave:
            value = sample[tree.split_feature]
            print(features[tree.split_feature], tree.threshold, value)
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result.append(tree.id)
        print(tree.id)
        #input("pause")
    return result
leaf =  findLeave(forest, sample, features)
#print(leaf)

def sigmoid(x):
    return 1.0/(1.0 + math.exp(-x))

def logit(x):
    return math.log(x/(1.0-x))


def predict(forest, sample, weight):
    result = 0
    for i in range(len(forest)):
        tree = forest[i]
        #shrinkage = 0.116
        shrinkage = 1.0
        #shrinkage = weight[i]
        while not tree.is_leave:
            value = sample[tree.split_feature]
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result += shrinkage * tree.value
    return sigmoid(result)


"""
def predict_1(forest, sample, weight):
    result = 0
    denominator = sum(weight)
    for i in range(len(forest)):
        tree = forest[i]
        shrinkage = weight[i]
        while not tree.is_leave:
            value = sample[tree.split_feature]
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result += shrinkage * sigmoid(tree.value)
    return result/denominator

def predict_2(forest, sample, weight):
    result = 0
    for i in range(len(forest)):
        tree = forest[i]
        shrinkage = weight[i]
        while not tree.is_leave:
            value = sample[tree.split_feature]
            if value <= tree.threshold:
                tree = tree.left
            else:
                tree = tree.right
        result += shrinkage * sigmoid(tree.value)
    return result/300.0

prediction = predict(forest, sample, weight)
print(prediction)
def predict_all(forest, inputs, weight):
    result = []
    for sample in inputs:
        prediction = predict(forest, sample, weight)
        result.append(prediction)
    return result
prediction_all = predict_all(forest, inputs, weight)
print("============================")
for item in prediction_all:
    print(item)
"""
'''
prediction_2 = predict_2(forest, sample, weight)
prediction_1 = predict_1(forest, sample, weight)
#print(prediction_1)
#print(prediction_all)
'''

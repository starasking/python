# Auther: Xuemei Wang
# Created date: 2019-07-04
# Copyright: Xuemei Wang

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

    root_split_feature = split_feature.pop()
    root_threshold = threshold.pop()
    root = Tree(0, root_split_feature, root_threshold)
    branches = [root]

    for i in range(len(left_child)):
        #print(i)
        left_id = left_child[i]
        left = Tree(left_id)
        if left_id < 0:
            left.is_leave = True
            left.value = leaf_value.pop()
        right_id = right_child[i]
        right = Tree(right_id)
        if right_id < 0:
            right.is_leave = True
            right.value = leaf_value.pop()

        branch = None
        while len(branches) > 0:
            branch = branches.pop()
            if branch.is_leave:
                branch = branches.pop()
            else:
                break
        if branch == None:
            assert(len(branches) == 0)
            break
        else:
            if not left.is_leave:
                branches.append(left)
                assert(len(split_feature) > 0)
                left_split_feature = split_feature.pop()
                left_threshold = threshold.pop()
            branch.left = left

            if not right.is_leave:
                branches.append(right)
                assert(len(split_feature) > 0)
                right_split_feature = split_feature.pop()
                right_threshold = threshold.pop()
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
               feature_line = line.split('=')[1] 
               features = feature_line.split(' ')
               #print(features[:5])
            if line.startswith('Tree='):
                #print('\n')
                #print(line.split('\n')[0])
                
                (idx, split_feature) = checkLine(i, 3, lines, 'split_feature')
                i = idx
                split_feature = list(map(int, split_feature))
                #print(split_feature[:5])
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
    return forest


forest = readLightGBM("lightgbm.txt")
print(len(forest))

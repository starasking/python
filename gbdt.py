import pandas as pd
import numpy as np

input_data = np.array([['Sunny', 'Hot', 'High', 'Weak', 25.0],
                       ['Sunny', 'Hot', 'High', 'Strong', 30.0],
                       ['Overcast', 'Hot', 'High', 'Weak', 46.0],
                       ['Rain', 'Mild', 'High', 'Weak', 45.0],
                       ['Rain', 'Cool', 'Normal', 'Weak', 52.0],
                       ['Rain', 'Cool', 'Normal', 'Strong', 23.0],
                       ['Overcast', 'Cool', 'Normal', 'Strong', 43.0],
                       ['Sunny', 'Mild', 'High', 'Weak', 35.0],
                       ['Sunny', 'Cool', 'Normal', 'Weak', 38.0],
                       ['Rain', 'Mild', 'Normal', 'Weak', 46.0],
                       ['Sunny', 'Mild', 'Normal', 'Strong', 48.0],
                       ['Overcast', 'Mild', 'High', 'Strong', 52.0],
                       ['Overcast', 'Hot', 'Normal', 'Weak', 44.0],
                       ['Rain', 'Mild', 'High', 'Strong', 30.0]])

col_names = ['Outlook', 'Temp', 'Humididty', 'Wind', 'Decision']
index = [i for i in range(1, 15)]
df = pd.DataFrame(input_data, columns = col_names, index = index)
df['Decision'] = df['Decision'].astype('float')
Entropy_threshold = 3

query = pd.DataFrame(np.array([['Sunny', 'Hot', 'Normal', 'Weak']]),
                     columns = ['Outlook', 'Temp', 'Humididty', 'Wind'])

class Tree:
    def __init__(self, entropy, value, split_feature, character):
        self.entropy = entropy
        self.value = value
        self.feature = split_feature
        self.character = character
        self.branches = {}

class Node:
    def __init__(self, character, entropy, value):
        self.entropy = entropy
        self.value = value
        self.character = character

def split_branch(df, output_col):
    entropy_pre = df[output_col].std(ddof=0)
    features = list(df.columns)
    features.remove(output_col)

    # TODO: add stop condition
    if len(features) == 0 or entropy_pre < Entropy_threshold:
        return ("", None)
    split_feature = features[0]
    return_nodes = []
    gain = 0

    for col in features:
        characters = set(df[col])
        denominator = float(df.shape[0])
        entropy = 0
        nodes = []
        for c in characters:
            numerator = float(df[df[col] == c].shape[0])
            std = df[df[col] == c][output_col].std(ddof=0)
            value = df[df[col] == c][output_col].mean()
            entropy += numerator/denominator * std
            nodes.append(Node(c, std, value))

        if gain < entropy_pre - entropy :
            gain = entropy_pre - entropy
            split_feature = col
            return_nodes = nodes

    return (split_feature, return_nodes)

def grow_tree(df, split_feature, nodes, tree, leaves):
    for node in nodes:
        subtree = Tree(node.entropy, node.value, "", node.character)
        tree.branches[node.character] = subtree
        print(split_feature)
        print(tree.branches)
        subdf = df[df[split_feature] == node.character]
        del subdf[split_feature]
        leaves[subtree] = subdf
    return (tree, leaves)

def create_tree(df, output_col):
    entropy = df[output_col].std(ddof=0)
    value = df[output_col].mean()
    (split_feature, nodes) = split_branch(df, output_col)
    tree = Tree(entropy, value, split_feature, "")
    leaves = {}

    print(df)
    print(split_feature)

    for node in nodes:
        print(node.entropy, node.character)
    (new_tree, new_leaves) = grow_tree(df, split_feature, nodes, tree, leaves)
    tree = new_tree
    leaves = new_leaves

    #print("=============================")
    #print(tree.value)
    #print(tree.entropy)
    #print(tree.feature)
    #print(tree.branches)
    #print("=============================")
    while bool(leaves):
        subtree = list(leaves.keys())[0]
        df = leaves[subtree]
        (split_feature, nodes) = split_branch(df, output_col)
        subtree.feature = split_feature
        #print("=============================")
        #print(subtree.value)
        #print(subtree.entropy)
        #print(subtree.feature)
        #print(subtree.branches)
        #print("=============================")
        #input("pause")
        if split_feature == "":
            del leaves[subtree]
            continue
        print(df)
        print(split_feature)
        for node in nodes:
            print(node.entropy, node.character)
        (new_tree, new_leaves) = grow_tree(df, split_feature, nodes, subtree, leaves)
        del leaves[subtree]
        subtree = new_tree
        leaves = new_leaves
    return tree

tree = create_tree(df, "Decision")

def predict(query, tree):
    while query.shape[1] > 0:
        current_feature = tree.feature
        if query[tree.feature][0] not in tree.branches.keys():
            return tree.value
        tree = tree.branches[query[tree.feature][0]]
        del query[current_feature]
    return tree.value

#def print_tree(tree):
    #print("=============================")
    #print(tree.value)
    #print(tree.entropy)
    #print(tree.feature)
    #print(tree.branches)

#print_tree(tree)
#print_tree(tree.branches['Sunny'])
#print(df)
#print(query)

print("=============================")
print(predict(query, tree))

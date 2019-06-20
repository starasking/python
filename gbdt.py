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

class Tree:
    def __init__(self, entropy, features, character):
        self.entropy = entropy
        self.features = features
        self.character = character
        self.branches = {}

class Node:
    def __init__(self, character, entropy):
        self.entropy = entropy
        self.character = character

def split_branch(df, feature_cols, features_done, entropy_pre):
    split_feature = feature_cols[0]
    return_nodes = []
    gain = 0

    for col in feature_cols:
        characters = set(df[col])
        denominator = float(df.shape[0])
        entropy = 0
        nodes = []
        for c in characters:
            numerator = float(df[df[col] == c].shape[0])
            std = df[df[col] == c]['Decision'].std(ddof=0)
            entropy += numerator/denominator * std
            nodes.append(Node(c, std))

        if gain < entropy_pre - entropy :
            gain = entropy_pre - entropy
            split_feature = col
            return_nodes = nodes

    new_features = feature_cols
    new_features.remove(split_feature)
    features_done.append(split_feature)
    return (new_features, features_done, return_nodes)

def create_tree(df, output_col):
    entropy = df[output_col].std(ddof=0)
    features = df.columns
    features.remove(output_col)
    features_done = []
    tree = new Tree(entropy, "", "")

    # try once
    (features, features_done, nodes) = split_branch(df, features, features_done, entropy)
    for node in nodes:
        subtree = new Tree(node.entropy, features_done, node.character)
        tree.branches[node.character] = subtree

create_tree(df, "Decision")

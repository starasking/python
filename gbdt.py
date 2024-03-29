import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error



class Tree:
    def __init__(self, entropy, value, split_feature):
        self.entropy = entropy
        self.value = value
        self.feature = split_feature
        self.branches = {}


class GBDT:
    def __init__(self, df, output_col, rounds = 5, decay_ratio = 0.5, stopforest_threshold = 0.1):
        self.df = df
        self.rounds = 5
        self.stoptree_threshold = df[output_col].std(ddof=0)

def split_branch(df, output_col, threshold):
    entropy_pre = df[output_col].std(ddof=0)
    value = df[output_col].mean()
    features = list(df.columns)
    features.remove(output_col)

    if len(features) == 0 or entropy_pre < threshold:
        return Tree(entropy_pre, value, "")

    split_feature = features[0]
    return_characters = []
    gain = 0

    for col in features:
        character_set = set(df[col])
        denominator = float(df.shape[0])
        entropy = 0
        characters = []
        for c in character_set:
            numerator = float(df[df[col] == c].shape[0])
            std = df[df[col] == c][output_col].std(ddof=0)
            entropy += numerator/denominator * std
            characters.append(c)

        if gain < entropy_pre - entropy :
            gain = entropy_pre - entropy
            split_feature = col
            return_characters = characters

    tree = Tree(entropy_pre, value, split_feature)
    for character in return_characters:
        tree.branches[character] = None
    return tree

def grow_tree(df, output_col, leaves, threshold):
    tree = split_branch(df, output_col, threshold)
    if tree.feature == "":
        return (tree, leaves)
    for character in tree.branches.keys():
        subdf = df[df[tree.feature] == character]
        del subdf[tree.feature]
        subtree = split_branch(subdf, output_col, threshold)
        tree.branches[character] = subtree
        leaves[subtree] = subdf
    return (tree, leaves)

def create_tree(df, output_col, threshold):
    leaves = {}
    (tree, leaves) = grow_tree(df, output_col, leaves, threshold)

    for character in tree.branches.keys():
        subtree = tree.branches[character]
        subdf = leaves[subtree]
        newtree = create_tree(subdf, output_col, threshold)
        tree.branches[character] = newtree
    return tree

#tree = create_tree(df, "Decision", Stoptree_threshold)

def predict(query, tree):
    new_tree = tree
    while query.shape[1] > 0:
        current_feature = new_tree.feature
        if current_feature == "" or query[new_tree.feature][0] not in new_tree.branches.keys():
            return new_tree.value
        new_tree = new_tree.branches[query[new_tree.feature][0]]
        del query[current_feature]
    return new_tree.value

def predict_2(query_df, tree):
    for index in range(len(query_df)):
        new_tree = tree
        ground_truth = query_df.iloc[index]['Decision']
        query = query_df.iloc[[index]]
        del query['Decision']
        while query.shape[1] > 1:
            current_feature = new_tree.feature
            if current_feature == "" or query[new_tree.feature][index] not in new_tree.branches.keys():
                break
            new_tree = new_tree.branches[query[new_tree.feature][index]]
            del query[current_feature]
        print(new_tree.value, ground_truth)

def relabel(df, tree, output_col):
    newdf = df.copy()
    for index in range(len(newdf)):
        new_tree = tree
        ground_truth = newdf.iloc[index][output_col]
        query = newdf.iloc[[index]]
        del query[output_col]
        while query.shape[1] > 1:
            current_feature = new_tree.feature
            if current_feature == "" or query[new_tree.feature][index] not in new_tree.branches.keys():
                label = new_tree.value - ground_truth
                newdf[output_col][index] = label
                break
            new_tree = new_tree.branches[query[new_tree.feature][index]]
            del query[current_feature]
        label = new_tree.value -  ground_truth
        #print(newdf[output_col][index])
        newdf[output_col][index] = label
    return newdf

threshold = Stoptree_threshold
forest = []
df_list = []
mse_list = []

def train(df, rounds, output_col, decay_ratio, threshold, stopforest_threshold):
    for epoch in range(rounds):
        tree = create_tree(df, output_col, threshold)
        forest.append(tree)
        df_list.append(df)
        newdf = relabel(df, tree, output_col)
        df = newdf.copy()
        mse = np.sqrt((newdf[output_col] ** 2).mean())
        mse_list.append(mse)
        if mse < stopforest_threshold:
            return (forest, df_list, mse_list)
        threshold *= decay_ratio
    return (forest, df_list, mse_list)

def print_tree(tree):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(tree.value)
    print(tree.entropy)
    print(tree.feature)
    print("..............................")
    if tree.feature != "" and tree.branches != {}:
        for character in tree.branches.keys():
            print(character)
            print_tree(tree.branches[character])

(forest, df_list, mse_list) = train(df, 5, 'Decision', Decay_ratio, Stoptree_threshold, stopforest_threshold)
for i in range(len(forest)):
    print("=============================")
    print(df_list[i])
    print("-----------------------------")
    print(mse_list[i])
    print_tree(forest[i])


'''
newdf = relabel(df, tree, 'Decision')
print(df)
print("=============================")
print(newdf)
print("=============================")
predict_2(df, tree)

print(query)
print(predict(query, tree))
#print(predict(query_2, tree))
#print(predict(query_3, tree))
#print(predict_2(df, tree))
'''

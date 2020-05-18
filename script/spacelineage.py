


import numpy as np
import pandas as pd
from ete3 import Tree

def process_tree(tree_fn):

    tree_df  = pd.read_csv(tree_fn)
    source = tree_df['source'].values
    target = tree_df['target'].values

    root = set(source) - set(target)
    root = root.pop()

    t = build_tree(root, tree_df, None)
    return t



def build_tree(node, tree_df, parent_t):
    t = Tree()
    if 'distance' in tree_df.columns:
        t.dist = 1
    else:
        t.dist = 1
    if parent_t:
        t.dist_to_root = parent_t.dist_to_root + t.dist
    else:
        t.dist_to_root = 0
    t.name = node
    t.parent = parent_t
    childs = tree_df[tree_df['source'] == node]['target'].values.tolist()
    if childs:
        t.children = [build_tree(c, tree_df, t) for c in childs]
    else:
        t.children = []
    t.nodes = [t] + sum([c.nodes for c in t.children], [])
    return t






def run(prev_fn, tree_df):
    t = process_tree(tree_fn)
    node_list = sorted(t.nodes, key=lambda n: n.dist_to_root)
    node_name_list = [n.name for n in node_list]

    df = pd.read_csv(prev_fn)
    df = df.pivot(index='sample_id', columns='clone_id', values='clonal_prev')
    df = df[node_name_list]
    df[df < 0.01] = 0
    df[df >= 0.01] = 1
    df = df.sort_values(by=node_name_list)
    from matplotlib import pyplot as plt
    import seaborn as sns
    fig = plt.figure()
    dn = sns.heatmap(df)
    plt.savefig('test.png')

prev_fn = '~/Downloads/A21_clonal_prev.csv'
tree_fn = '~/Downloads/A21_tree.csv'


run(prev_fn, tree_fn)
'''
#t.write(format=1, outfile="Wang2014_TNBC_rerooted.nwk")
with open("Wang2014_TNBC_rerooted.nwk", 'w') as f:
    f.write(to_newick(t))
'''

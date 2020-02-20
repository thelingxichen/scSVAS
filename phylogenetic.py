#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd

def get_newick_aux(node, newick, parentdist, leaf_names):
    if node.is_leaf():
        return "%s:%.2f%s" % (leaf_names[node.id], parentdist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = get_newick_aux(node.get_left(), newick, node.dist, leaf_names)
        newick = get_newick_aux(node.get_right(), ",%s" % (newick), node.dist, leaf_names)
        newick = "(%s" % (newick)
        return newick


def get_newick(Z, cell_names):
    tree = hierarchy.to_tree(Z, rd=False)
    # https://github.com/scipy/scipy/issues/8274 request for to_newick
    netwick = get_newick_aux(tree, "", tree.dist, cell_names) 
    '''
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(25, 25))
    dn = hierarchy.dendrogram(Z)
    plt.savefig('test.png')
    '''
    return netwick


def get_tree(x, index, index_name, k=3):

    Z = hierarchy.linkage(x)

    # get newick 
    newick = get_newick(Z, index) 

    # get hc
    df = pd.DataFrame(hierarchy.cut_tree(Z, 7)[:,0]+1, columns=['hcluster'], index=index)
    df.index.name = index_name

    return newick, df

        

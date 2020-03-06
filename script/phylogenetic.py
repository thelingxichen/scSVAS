#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import copy
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
from ete3 import Tree
import json
import sys

sys.setrecursionlimit(100000)

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
    '''
    x = np.array([662., 877., 255., 412., 996., 295., 468., 268.,
                  400., 754., 564., 138., 219., 869., 669.])
    index = range(6)
    '''
    Z = hierarchy.linkage(x)

    # get newick 
    newick = get_newick(Z, index) 

    # get hc
    df = pd.DataFrame(hierarchy.cut_tree(Z, 7)[:,0]+1, columns=['hcluster'], index=index)
    df.index.name = index_name

    return newick, df


def get_nested_tree_json(t, k):
    res = get_nested_tree_aux(t, k)
    return json.dumps(res, indent=4)


def get_nested_tree_aux(t, k):
    cut_t = cut_tree(t, k)
    leafs = [n.name for n in t.nodes if not n.children]
    node_dict = {}
    res = {}
    res['dist_to_root'] = t.dist_to_root
    res['parent'] = t.parent.name if t.parent else 'NONE' 
    res['newick'] = cut_t.write(format=1) 
    res['leafs'] = leafs
    node_dict[t.name] = res
    if t.children:
        for c in t.children:
            n_dict = get_nested_tree_aux(c, k)
            node_dict.update(n_dict)

    return node_dict 



def node_to_dict(t):
    res = {}
    return res


def get_leafs(t):
    if not t.children:
        return [t.name]
    res = []
    for c in t.children:
        res += get_leafs(c)
    return res


def cut_tree(t, k):
    t = copy.deepcopy(t)
    if k == 1:
        return t
    nodes = set()
    leafs = set() 
    node_list = sorted(t.nodes, key=lambda n: n.dist_to_root)
    if k > len(node_list):
        k = len(node_list)
    for node in node_list:
        '''
        print('--before')
        print(node.name)
        print('nodes', [n.name for n in nodes])
        print('leafs', [n.name for n in leafs])
        print('childs', [n.name for n in node.children])
        print(k>len(leafs), len(nodes) < len(node_list))
        '''
        if k > len(leafs) and len(nodes) < len(node_list):
            nodes.add(node)
            nodes = nodes | set(node.children)
            leafs = leafs | set(node.children)
            if node in leafs:
                leafs.remove(node)
        '''
        print('--after')
        print([n.name for n in nodes])
        print([n.name for n in leafs])
        '''
    cut_tree_aux(t, leafs)
    return t


def cut_tree_aux(t, leafs):
    if not t.children:
        return

    for c in t.children:
        if c in leafs:
            c.children = []
        else:
            cut_tree_aux(c, leafs)


def get_tree_from_newick(newick):
    t = Tree(newick)
    t.parent = None
    set_tree(t, node_id=0)
    return t


def set_tree(t, node_id=0):
    if not t.children:
        t.dist_to_root = t.dist
        t.leafs = []
        t.nodes = [t]
        return

    t.name = 'n{}'.format(node_id)
    t.dist_to_root = t.dist
    t.leafs = []
    t.nodes = [t]
    current_node_id = node_id + 1
    for c in t.children:
        c.parent = t
        set_tree(c, current_node_id)
        for n in c.nodes:
            n.dist_to_root += t.dist 
            if n.children:
                current_node_id += 1 
        t.nodes += c.nodes 
    




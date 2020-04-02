#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from scipy.cluster import hierarchy
import numpy as np
from ete3 import Tree
import json
import sys
import collections

sys.setrecursionlimit(100000)


def to_newick(t):
    return '({});'.format(to_newick_aux(t))


def to_newick_aux(t):
    if not t.children:
        return '{}:{}'.format(t.name, t.dist)

    res = ','.join([to_newick_aux(c) for c in t.children])
    res = '({}){}:{}'.format(res, t.name, t.dist)
    return res


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


def build_hc_tree(df, index_name):
    '''
    x = np.array([662., 877., 255., 412., 996., 295., 468., 268.,
                  400., 754., 564., 138., 219., 869., 669.])
    index = range(6)
    '''
    Z = hierarchy.linkage(df, method='weighted')
    # weighted, centroid works for demo1, ward + single not work

    # get newick
    newick = get_newick(Z, df.index)
    '''
    # get hc
    m_df = pd.DataFrame(hierarchy.cut_tree(Z, k)[:,0]+1, columns=['hcluster'], index=df.index)
    m_df.index.name = index_name
    '''
    return newick


def get_nested_tree_json(t, k):
    set_tree_coords(t)
    res = get_nested_tree_aux(t, k)
    return json.dumps(res, indent=4)


def get_nested_tree_aux(t, k):
    cut_t, map_list = cut_tree(t, k)
    node_dict = {}
    res = {}
    res['dist_to_root'] = t.dist_to_root
    res['parent'] = t.parent.name if t.parent else 'NONE'
    res['newick'] = to_newick(cut_t)
    if map_list:
        res['leafs'] = [c for c, g in map_list]
    else:
        res['leafs'] = [t.name]

    node_dict[t.name] = res
    if t.children:
        for c in t.children:
            n_dict = get_nested_tree_aux(c, k)
            node_dict.update(n_dict)

    return node_dict


def get_evo_tree_dict(t, df, bins):
    node_list = sorted(t.nodes, key=lambda n: n.dist_to_root)
    res = {}
    res['name'] = t.name
    res['parent'] = t.parent.name if t.parent else 'NONE'
    res['newick'] = to_newick(t)
    res['lifetime'] = node_list[-1].dist_to_root/2*3
    res['dist_to_root'] = t.dist_to_root
    res['num_cells'] = len(df)
    res['leafs'] = [n.name for n in t.leafs]
    res['links'] = [(l.source.name, l.target.name, l.shift_bins) for l in t.links]
    nodes_dict = {}

    set_tree_coords(t, df)
    node_list = sorted(t.nodes, key=lambda n: n.dist_to_root)
    for n in node_list:
        c = n.closest_child.name if n.closest_child else 'NONE'
        nodes_dict[n.name] = [n.x, n.y, n.start_y, n.end_y, c,
                              {'cnv': dict(zip(bins, n.cnv))}]
    res['node_list'] = list(nodes_dict.keys())
    res['nodes'] = nodes_dict
    # res['clonal_freqs'] = clonal_freqs
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
        if k > len(leafs) and len(nodes) < len(node_list):
            nodes.add(node)
            nodes = nodes | set(node.children)
            leafs = leafs | set(node.children)
            if node in leafs:
                leafs.remove(node)
    leafs_list = sorted([n.name for n in leafs])
    map_list = cut_tree_aux(t, {n: i+1 for i, n in enumerate(leafs_list)})
    set_tree(t, prefix=None)
    return t, map_list


def cut_tree_aux(t, leafs):
    if not t.children:
        if t.name in leafs.keys():
            return [(t.name, leafs[t.name])]
        else:
            return []

    map_list = []
    for c in t.children:
        if c.name in leafs.keys():
            map_list += [(n.name, leafs[c.name]) for n in c.leafs]
            c.children = []
        else:
            map_list += cut_tree_aux(c, leafs)
    return map_list


def get_tree_from_newick(newick, root=''):
    t = Tree(newick)
    t.name = root
    t.parent = None
    set_tree(t, node_id=0)
    return t


def set_tree(t, node_id=0, prefix='n'):
    if not t.children:
        if prefix == 'c' and not t.name:
            t.name = '{}{}'.format(prefix, node_id)
        t.dist_to_root = t.dist
        t.lifetime = t.dist
        t.leafs = [t]
        t.nodes = [t]
        t.links = []
        t.closest_child = None
        return

    if prefix and not t.name:
        t.name = '{}{}'.format(prefix, node_id)
    t.dist_to_root = t.dist
    t.leafs = []
    t.links = []
    t.nodes = [t]
    current_node_id = node_id + 1
    t.closest_child = t.children[0]
    for c in t.children:
        if c.dist < t.closest_child.dist:
            t.closest_child = c
        c.parent = t
        set_tree(c, current_node_id, prefix=prefix)
        t.links += [Link(t, c)]
        t.links += c.links
        for n in c.nodes:
            n.dist_to_root += t.dist
            if n.children or prefix == 'c':
                current_node_id += 1
        t.nodes += c.nodes
        t.leafs += c.leafs


def set_tree_coords(t, df=None):
    if df is not None:
        map_dict = df.apply(str).value_counts().to_dict()
        count = map_dict.get(t.name, 0)/2
    else:
        count = 0.5

    for i, n in enumerate(t.leafs):
        n.start_y = count
        if df is not None:
            count += map_dict[n.name]
        else:
            count += 1
        n.end_y = count
        n.y = i + 0.5

    if df is not None and t.name in map_dict:
        t.start_y = 0
        count += map_dict[t.name]/2
        t.end_y = count

    set_tree_coords_aux(t)


def set_tree_coords_aux(t):
    t.x = t.dist_to_root
    if not t.children:
        return
    for c in t.children:
        set_tree_coords_aux(c)
    t.y = (t.children[0].y + t.children[-1].y)/2
    if t.name.startswith('n'):
        t.start_y = t.children[0].start_y
        t.end_y = t.children[-1].end_y
    return


class Link():
    def __init__(self, source=None, target=None, dist=None,
                 meta=''):
        self.source = source
        self.target = target
        self.dist = dist
        self.meta = meta
        self.shift_bins = {}

    def __repr__(self):
        return '{}->{}:{}'.format(self.source.name, self.target.name, self.dist)


def choose_normal(df):
    # choose group close to normal as root
    m = np.matrix(df.values)
    norms = np.sum(np.multiply(m, m) + 4 - 4*m, axis=1)
    normal = str(df.index[np.argmin(norms)])
    return normal


def reroot_normal(t, root):
    '''
    simply reroot normal to root, depricated
    '''
    rerooted_t = reroot_normal_aux(t, root)
    # print(to_newick(rerooted_t))
    while rerooted_t.name != root:
        rerooted_t = reroot_normal_aux(rerooted_t, root)
        # print(to_newick(rerooted_t))

    rerooted_t = prune_internal_node(rerooted_t)
    set_tree(rerooted_t, prefix=None)
    # print(to_newick(rerooted_t))
    return rerooted_t


def reroot_normal_aux(t, root):
    if not t.children:
        return t
    childs = []
    for c in t.children:
        if c.name == root:
            c.name = t.name
            t.name = root
            if not c.children:
                continue
        c = reroot_normal_aux(c, root)
        childs.append(c)
    t.children = childs
    return t


def prune_internal_node(t):
    if not t.children:
        return t
    childs = []
    for c in t.children:
        if len(c.children) == 1:
            c = c.children[0]
        childs.append(prune_internal_node(c))
    t.children = childs
    return t


# reroot tree by bin changes #########

def reroot_tree(t, cnv_df):
    assign_tree_cnv(t, cnv_df)
    rerooted_t = reroot_tree_aux(t)
    set_tree(rerooted_t, prefix=None)

    return rerooted_t


def reroot_tree_aux(t):
    if not t.children:
        return t

    childs = []
    for c in t.children:
        if c.cnv == t.cnv:
            t.name = c.name
            t.cnv = c.cnv
        else:
            c = reroot_tree_aux(c)
            childs.append(c)
    t.children = childs
    return t


def assign_tree_cnv(t, cnv_df):
    if not t.children:
        t.cnv = cnv_df.loc[t.name].tolist()
        return

    if t.name in cnv_df.index:
        t.cnv = cnv_df.loc[t.name].tolist()
        for c in t.children:
            assign_tree_cnv(c, cnv_df)
        return

    # infer cnv to internal node
    cnv_list = []
    for c in t.children:
        assign_tree_cnv(c, cnv_df)
        cnv_list.append(c.cnv)
    m = np.matrix(cnv_list)
    t.cnv = [choose_ancestor_cnv(xs) for xs in m.T.tolist()]


def choose_ancestor_cnv(xs):
    if 2 in xs:
        cnv = 2
    else:
        freqs = collections.Counter(xs).most_common(2)
        if len(freqs) == 1:
            cnv = freqs[0][0]
        elif freqs[0][1] != freqs[1][1]:
            if freqs[0][0] > 2 and freqs[1][0] > 2:
                cnv = min(freqs[0][0], freqs[1][0])
            elif freqs[0][0] < 2 and freqs[1][0] < 2:
                cnv = max(freqs[0][0], freqs[1][0])
            else:
                cnv = 2
        else:  # choose the most frequent one
            cnv = freqs[0][0]

    return cnv

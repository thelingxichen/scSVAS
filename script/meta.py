#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Output metadata from SCYN, metadata include:
    - dendogram tree (newick format)
    - hierarchy clustering result
    - PCA, TSNE, UMAP embedding result

Usage:
    meta.py call --cnv_fn=IN_FILE [--meta_fn=IN_FILE] [-k=INT] [--out_prefix=STR]
    meta.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --cnv_fn=IN_FILE    Path of SCYN format cnv file.
    --meta_fn=IN_FILE   Path of SCYN format meta file.
    -k=INT              Number of clusters in the tree at the cut point. [default: 3]
    --out_prefix=STR    Path of out file prefix, [default: ./phylo] 
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd

import phylogenetic
import embedding 


def read_cnv_fn(cnv_fn):
    df = pd.read_csv(cnv_fn)
    cell_names = df.values[:, 0]
    cnv_m = df.values[:, 1:]
    return cnv_m, cell_names

def read_meta_fn(meta_fn):
    df = pd.read_csv(meta_fn, index_col='cell_id')
    return df
    
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


def run_call(cnv_fn=None, meta_fn=None, k=3, cut_n=50,
             out_prefix=None, **args):
    cnv_m, cell_names = read_cnv_fn(cnv_fn) 

    # newick, hc
    newick, df = phylogenetic.get_tree(cnv_m, cell_names, 'cell_id', k=k)
    nwk_fn = out_prefix + '.nwk'
    with open(nwk_fn, 'w') as f:
        f.write(newick)

    t = phylogenetic.get_tree_from_newick(newick)
    json = phylogenetic.get_nested_tree_json(t, cut_n)
    json_fn = out_prefix + '_cut{}.json'.format(cut_n)
    with open(json_fn, 'w') as f:
        f.write(json)

    cut_t = phylogenetic.cut_tree(t, k)
    cut_nwk_fn = out_prefix + '_cut.nwk'
    cut_t.write(format=1, outfile=cut_nwk_fn)

    # hc
    if meta_fn:
        meta_df = read_meta_fn(meta_fn)
        meta_df = pd.merge(meta_df, df, how='outer', on='cell_id')
    else:
        meta_df = df

    # PCA
    df = embedding.get_pca(cnv_m, cell_names, 'cell_id')
    meta_df = pd.merge(meta_df, df, how='outer', on='cell_id')

    # TSNE 
    df = embedding.get_tsne(cnv_m, cell_names, 'cell_id')
    meta_df = pd.merge(meta_df, df, how='outer', on='cell_id')

    # UMAP 
    df = embedding.get_umap(cnv_m, cell_names, 'cell_id')
    meta_df = pd.merge(meta_df, df, how='outer', on='cell_id')

    meta_fn = out_prefix + '_meta_scvar.csv' 
    meta_df.to_csv(meta_fn)
    '''



def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

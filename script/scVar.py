#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    scVar.py cnv --cnv_fn=IN_FILE [--meta_fn=IN_FILE] [--k=INT] [--out_prefix=STR]
    scVar.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --cnv_fn=IN_FILE    Path of SCYN format cnv file.
    --meta_fn=IN_FILE   Path of SCYN format meta file.
    --k=INT              Number of clusters in the tree at the cut point. [default: 3]
    --out_prefix=STR    Path of out file prefix, [default: ./phylo] 
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
import json

from utils import phylogenetic as phylo
from utils import io
from utils import embedding


def run_cnv(cnv_fn=None, meta_fn=None, k=7, cut_n=25,
             out_prefix=None, **args):
    k = int(k)
    cnv_index_name = 'cell_id'
    cnv_df = io.read_cnv_fn(cnv_fn, cnv_index_name) 
    cell_names = cnv_df.index.to_list()

    ##### build hc dendrogram ##### 
    newick = phylo.build_hc_tree(cnv_df, cnv_index_name)
    nwk_fn = out_prefix + '.nwk'
    with open(nwk_fn, 'w') as f:
        f.write(newick)
    t = phylo.get_tree_from_newick(newick)

    ##### cut hc dendrogram ##### 
    cut_t, map_list = phylo.cut_tree(t, k)
    m_df = pd.DataFrame(map_list)
    m_df.columns = [cnv_index_name, 'hcluster']
    m_df.index = m_df[cnv_index_name]
    del m_df[cnv_index_name] 

    ##### build nested tree ##### 
    res = phylo.get_nested_tree_json(t, cut_n)
    json_fn = out_prefix + '_cut{}.json'.format(cut_n)
    with open(json_fn, 'w') as f:
        f.write(res)

    ##### append meta info #####
    if meta_fn:
        meta_df = io.read_meta_fn(meta_fn, cnv_index_name)
        meta_df = pd.merge(meta_df, m_df, how='outer', on=cnv_index_name)
    else:
        meta_df = m_df
    '''
    # PCA
    df = embedding.get_pca(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)
    # TSNE 
    df = embedding.get_tsne(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)
    # UMAP 
    df = embedding.get_umap(cnv_df, cell_names, cnv_index_name)
    meta_df = pd.merge(meta_df, df, how='outer', on=cnv_index_name)
    meta_fn = out_prefix + '_meta_scvar.csv' 
    meta_df.to_csv(meta_fn)
    '''

    ##### build tree by meta category label #####
    evo_dict = {}
    for col in meta_df.columns:
        if col.startswith('e_') or col.startswith('c_'):
            continue
        df = pd.merge(meta_df[col], cnv_df, how='outer', on=cnv_index_name)
        df = df.groupby(col).mean()
        newick = phylo.build_hc_tree(df, col)
        t = phylo.get_tree_from_newick(newick)
        evo_dict[col] = phylo.get_evo_tree_dict(t, meta_df[col]) 
    res = json.dumps(evo_dict, indent=4)
    json_fn = out_prefix + '_evo{}.json'.format(k)
    with open(json_fn, 'w') as f:
        f.write(res)

def run(cnv=None, **args):
    if cnv:
        run_cnv(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    scVar.py call --cnv_fn=IN_FILE [--meta_fn=IN_FILE] [-k=INT] [--out_prefix=STR]
    scVar.py -h | --help

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
    

def run_call(cnv_fn=None, meta_fn=None, k=3, cut_n=50,
             out_prefix=None, **args):
    cnv_m, cell_names = read_cnv_fn(cnv_fn) 


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

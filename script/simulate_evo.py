#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    simulate.py call [-k=INT] [--out_prefix=STR]
    simulate.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    -k=INT              Number of subclones in simulated tree. [default: 4]
    --out_prefix=STR    Path of out file prefix, [default: ./simu] 
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
from dendropy.simulate import treesim
from ete3 import Tree

from utils import phylogenetic as phylo 
import embedding 


def simu_tree():
    birth_rate = 1
    death_rate = 1
    num_leafs = 20 

    # t = treesim.birth_death_tree(birth_rate=birth_rate, death_rate=death_rate, num_total_tips=10)
    # t = treesim.birth_death_tree(birth_rate=birth_rate, death_rate=death_rate, num_extinct_tips=10)
    t = treesim.birth_death_tree(birth_rate=birth_rate, death_rate=death_rate, num_extant_tips=num_leafs)
    newick = t.as_string('newick').replace('[&R] ', '')
    return Tree(newick)


def simu_cnv(t):
    num_bins = 100
    t.cnv = [2]*num_bins
    simu_cnv_aux(t)

def simu_cnv_aux(t):
    if not t.children:
        pass
   

def run_call(k=None, out_prefix=None, **args):
    prefix = 'c'
    k = int(k)
    t = simu_tree()
    phylo.set_tree(t, prefix=prefix)
    cut_t = phylo.cut_tree(t, k, prefix=prefix)
    print(cut_t.nodes)
    print('---')
    for leaf in cut_t.leafs:
        print(leaf)
    simu_cnv(t)


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
        new_args[k.replace('-', '')] = v
    run(**new_args)

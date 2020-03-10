#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    annotation.py call --cnv_fn=IN_FILE [--gene_fn=IN_FILE] [--out_prefix=STR]
    annotation.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --cnv_fn=IN_FILE    Path of SCYN format cnv file.
    --gene_fn=IN_FILE   Path of intersted gene file.
    --out_prefix=STR    Path of out file prefix, [default: ./phylo] 
"""
import os
import docopt
import numpy as np
import pandas as pd

import io

def run_call(cnv_fn=None, gene_fn=None, out_prefix=None, **args):
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

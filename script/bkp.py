#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    scVar.py bkp --bkp_fns=IN_FILES [--out_prefix=STR] [--tool=STR]
    scVar.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --bkp_fn=IN_FILES           Path of breakpoint files, seperated with ','.
    --out_prefix=STR            Path of out file prefix, [default: ./bkp] 
    --tool=STR                  10x cell-ranger or SCYN, [default: 10x]
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
import json
import csv

from utils import phylogenetic as phylo
from utils import io
from utils import embedding
from utils import annotation as anno


def read_bkp_fns_from_10x(bkp_fns, confidence=15):
    for bkp_fn in bkp_fns.split(','):
        _, sample = os.path.split(bkp_fn)
        bed_file = filter(lambda row: row.startswith('#chrom') or not row.startswith('#'), open(bkp_fn, 'r'))
        for i, row in enumerate(csv.DictReader(bed_file, delimiter='\t')):
            if int(row.get('event_confidence', confidence)) < confidence:
                continue
            chrom, start, end, cell = row['#chrom'], row['start'], row['end'], row['id']
            if not chrom.startswith('chr'):
                chrom = 'chr'+chrom
            yield chrom, start, end, cell, sample



def run_bkp(bkp_fns=None, out_prefix=None, tool=None, **args):
    _, sample = os.path.split(out_prefix)
    group2bkps = {}
    if tool == '10x':
        bkps_iter = read_bkp_fns_from_10x(bkp_fns)

    bkps = {}
    for chrom, start, end, cell, sample in bkps_iter:
        for pos in [start, end]:
            key = (chrom, pos)
            if key in bkps:
                bkps[key].add(sample)
            else:
                bkps[key] = set([sample])

    for key, samples in bkps.items():
        chrom, pos = key
        if len(samples) <= 2:
            continue
        print(chrom, pos, samples)

    #SampleID,Chr,Position,Strand,JR_count

def run(bkp=None, **args):
    if bkp:
        run_bkp(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

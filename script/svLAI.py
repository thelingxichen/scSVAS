#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    svLAI.py call [--tree_fn=IN_FILE] --mut_fn=IN_FILE --sv_fn=IN_FILE --group_meta_fn=IN_FILE --barcode_group_fn=IN_FILE [--out_dir=STR] --sample=STR
    svLAI.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --tree_fn=IN_FILE           Path of tree file.
    --group_meta_fn=IN_FILE     Path of group meta file.
    --barcode_group_fn=IN_FILE  Path of barcode group file.
    --out_dir=STR               Path of out file prefix, [default: ./test]
    --ref=STR                   Reference version, [default: hg38]
"""
import docopt
import numpy as np
import json
import pandas as pd
import collections
import os

from biotool import genome

from utils import phylogenetic as phylo
from utils import io
from utils import annotation as anno
import spacelineage

from SVAS.scripts import sv
from SVAS.scripts.compsv import complexsv 


def get_barcode_clone(group_meta_fn, barcode_group_fn):
    group_meta_df = pd.read_csv(group_meta_fn).set_index('group')
    barcode_group_df = pd.read_csv(barcode_group_fn)
    df = pd.merge(barcode_group_df, group_meta_df, on='group').set_index('barcode')
    barcode2clone = df['label'].to_dict()
    clone2barcodes = {} 
    for bc, c in barcode2clone.items():
        if c in clone2barcodes:
            clone2barcodes[c].append(bc)
        else:
            clone2barcodes[c] = [bc]
    return barcode2clone, clone2barcodes


def run_call(tree_fn=None, group_meta_fn=None, barcode_group_fn=None, out_dir=None, 
             mut_fn=None, sv_fn=None, sample=None,
             ref='hg38', **args):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    barcode2clone, clone2barcodes = get_barcode_clone(group_meta_fn, barcode_group_fn)
    # t, _, _ = spacelineage.process_tree(tree_fn)

    sv_df_list = []
    for f in mut_fn.split(','):
        sv_df_list.append(pd.read_csv(f, sep='\t').set_index('AnnotSV ID'))
    sv_df = pd.concat(sv_df_list)
    sv_df['Sample'] = sample
    sv_df.INFO = sv_df.INFO.apply(lambda x: x.split(';')[0])  # get bc_list
    sv_df = sv_df[sv_df.INFO.apply(lambda x: x.startswith('BX='))]
    sv_df.INFO = sv_df.INFO.apply(lambda x: [barcode2clone.get(bc.replace('_1', ''), '') for bc in x.replace('BX=', '').split(',')])  # get subclone_list
    sv_df.INFO = sv_df.INFO.apply(lambda cs: collections.Counter(c for c in cs if c))
    sv_df = sv_df[sv_df.INFO.apply(lambda x: len(x) != 0)]
    #info = sv_df.INFO.apply(lambda x: ','.join(sorted([a for a, b in x])))
    #print(collections.Counter(info.to_list()))
    # print(sv_df.INFO)
    sv_df.INFO = sv_df.INFO.apply(lambda cs: ';'.join(['{}={}'.format(c, n) for c, n in cs.items()]))
    sv_df.ID = sv_df.ID.apply(lambda x: str(x).replace(':1', '').replace(':2', '')) 
    sv_df = sv_df.drop_duplicates()
    sv_df[['Sample', 'ID', 'Gene name', 'SV type', 'INFO']].to_csv(os.path.join(out_dir, sample + '_sv_gene.csv'))

    id2genes = {}
    for p in (list(zip(sv_df.ID, sv_df['Gene name']))):
        id, g = p
        if type(g) == float:
            continue 
        if id in id2genes:
            id2genes[id].add(g)
        else:
            id2genes[id] = set([g])
    complexsv.run_call(sv_fn=sv_fn, sample=sample, out_dir=out_dir, 
                       id2genes=id2genes, barcode2clone=barcode2clone)

def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

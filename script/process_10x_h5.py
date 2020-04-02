#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# transfer bed file to matrix csv file

Usage:
    process_10x_h5.py call --h5_fn=IN_FILE [--out_prefix=STR] [--bins=INT] [--assembly=STR]
    process_10x_h5.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --h5_fn=IN_FILE     Path of h5 file.
    --bins=INT          Number of bins to average.[default: 256]
    --out_prefix=STR    Path of out file prefix. [default: ./10x]
    --assembly=STR      The assembly version of the sequence included as part of the reference. [default: hg38]
"""
import numpy as np
import pandas as pd
import docopt
import h5py

from biotool import genome
from utils import phylogenetic as phylo


def get_single_chrom_cnv(cnv_h5, bins):
    num_cells = int((cnv_h5.shape[0]+1)/2)
    m = cnv_h5[:num_cells, ].astype(float)
    m[(m >= -126) & (m <= -1)] += 127
    m[m == -127] = 0
    m[m > 20] = 20
    m[m == -128] = np.nan
    tmp = m.T
    slices = np.arange(0, tmp.shape[0], bins)
    mean = np.add.reduceat(tmp, slices)/bins
    mean = mean.T
    return mean


def get_cnv_df(h5_data, bins, bin_size, assembly, cell_names):
    chrom2size = genome.read_chrom_size(assembly)
    m_list = []
    regions_list = []
    for chrom in list(map(str, range(1, 23))) + ['X', 'Y']:
        chrom_size = chrom2size['chr' + chrom]
        tmp = get_single_chrom_cnv(h5_data['cnvs'][chrom], bins)
        pos = np.array(range(tmp.shape[1]))*bins*bin_size
        regions = ['chr{}:{}-{}'.format(chrom, s+1, e) for s, e in zip(pos[:-1], pos[1:])]
        regions.append('chr{}:{}-{}'.format(chrom, pos[-1]+1, chrom_size))
        regions_list += regions
        m_list.append(tmp)
    m = np.concatenate(m_list, axis=1)
    df = pd.DataFrame(m)
    df.columns = regions_list
    df.index = cell_names
    df.index.name = 'cell_id'
    return df


def get_bin_size(h5_data):
    return h5_data['constants']['bin_size'][()]


def get_tree_newick(h5_data, cell_names):
    Z = h5_data['tree']['Z'][:]
    newick = phylo.get_newick(Z, cell_names)
    return newick


def run_call(h5_fn=None, out_prefix=None, bins=None, assembly=None,
             **args):
    bins = int(bins)

    h5_data = h5py.File(h5_fn, 'r')
    bin_size = get_bin_size(h5_data)

    cell_names = [x.decode('utf-8') for x in h5_data['cell_barcodes']]

    newick = get_tree_newick(h5_data, cell_names)
    nwk_fn = out_prefix + '.nwk'
    with open(nwk_fn, 'w') as f:
        f.write(newick)

    df = get_cnv_df(h5_data, bins, bin_size, assembly, cell_names)
    out_fn = out_prefix + '_cnv.csv'
    df.to_csv(out_fn, float_format='%.2f')


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

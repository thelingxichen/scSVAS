#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# transfer bed file to matrix csv file

Usage:
    bed2matrix.py call --bed_fn=IN_FILE [--out_prefix=STR] [--confidence=INT]
    bed2matrix.py -h | --help

Options:
    -h --help           Show this screen.
    --version           Show version.
    --bed_fn=IN_FILE    Path of bed file.
    --out_prefix=STR    Path of out file prefix, prefix of bed_fn as default.
    --confidence=INT    CNV event confidence, only availble for cellranger bed file, [default: 15]
"""
import csv
import os
import numpy as np
import pandas as pd
import docopt


def run_call(bed_fn=None, out_prefix=None, confidence=10,
             **args):

    breakpoints = {}
    cells = set()
    bed_file = filter(lambda row: row.startswith('#chrom') or not row.startswith('#'), open(bed_fn, 'r'))
    for i, row in enumerate(csv.DictReader(bed_file, delimiter='\t')):
        chrom, start, end, cell_id = row['#chrom'], row['start'], row['end'], row['id']
        if not chrom.startswith('chr'):
            chrom = 'chr'+chrom
        cells.add(cell_id)
        if chrom not in breakpoints:
            breakpoints[chrom] = set()
        breakpoints[chrom].add(start)
        breakpoints[chrom].add(end)
    cell2index = {cell_id: i for i, cell_id in enumerate(cells)}

    regions = []
    bp2index = {}
    for chrom, bps in breakpoints.items():
        bps = sorted(list(map(int, bps)))
        res = {'{}:{}'.format(chrom, start): len(regions) + i for i, start in enumerate(bps)}
        bp2index.update(res)
        regions += ['{}:{}-{}'.format(chrom, s, e) for s, e in zip(bps[:-1], bps[1:])]

    matrix = np.full([len(cells), len(regions)], np.nan)
    bed_file = filter(lambda row: row.startswith('#chrom') or not row.startswith('#'), open(bed_fn, 'r'))
    for i, row in enumerate(csv.DictReader(bed_file, delimiter='\t')):
        if row.get('event_confidence', confidence) < confidence:
            continue
        chrom, start, end, cell_id, cn = row['#chrom'], row['start'], row['end'], row['id'], row['copy_number']
        if cn == 'NA':
            cn = np.nan
        if not chrom.startswith('chr'):
            chrom = 'chr'+chrom

        start_index = bp2index['{}:{}'.format(chrom, start)]
        end_index = bp2index['{}:{}'.format(chrom, end)]
        for i in range(start_index, end_index):
            matrix[cell2index[cell_id], i] = cn

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(matrix, index=cell2index.keys(), columns=regions)
    df.index.name = 'cell_id'
    df.index = 'cell_' + df.index
    if not out_prefix:
        _, out_prefix = os.path.split(bed_fn)
    df.to_csv(out_prefix + '_cnv.csv.gz', index=True, compression='gzip')


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

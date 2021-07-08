#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    xx.py call --in_fn=STR [--ref=STR]
    xx.py -h | --help

Options:
    -h --help              Show this screen.
    --version              Show version.
    --in_fn=STR            Path of input file.
    --ref=STR              Reference version, [default: hg38]
"""
import pickle
import docopt
import os


def run_call(in_fn=None, ref=None, **args):
    current_dir, _ = os.path.split(os.path.realpath(__file__))
    fn = os.path.join(current_dir, 'utils', 'db', 'ens_gene.pickle')
    gene_dict = pickle.load(open(fn, 'rb')).get(ref + '_gene', {})

    f = open(in_fn + '.region.csv', 'w')
    for i, line in enumerate(open(in_fn, 'r')):
        if i > 0:
            splits = line.split(',')
            gene_id = splits[0].split('_')[0].split('.')[0].upper()
            item = gene_dict.get(gene_id)
            if not item:
                continue
            chrom, start, end, _ = item
            region = '{}:{}-{}'.format(chrom, start, end)
            splits[0] = region
            # print(splits)
            f.write(','.join(splits))
        else:
            f.write(line)
    f.close()


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

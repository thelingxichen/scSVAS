#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    xx.py call --in_prefix=STR [--ref=STR] [--out_prefix=STR]
    xx.py -h | --help

Options:
    -h --help              Show this screen.
    --version              Show version.
    --in_prefix=STR        Path of input file prefix, like 'in_prefx' + 'barcodes.tsv.gz'
    --ref=STR              Reference version, [default: hg38]
    --out_prefix=STR       Path of out file prefix, [default: ./test]
"""
import pickle
import docopt
import pandas as pd
import gzip
import os

from utils import io
from utils import ensemble

def read_barcode_fn(barcode_fn):
    df = pd.read_csv(barcode_fn, header=None)
    df.columns = ['barcode']
    df.index = df.index + 1
    df.index.name = 'barcode_index'
    return df

def read_feature_fn(feature_fn, ref):
    df = pd.read_csv(feature_fn, header=None, sep='\t')
    df.columns = ['ens', 'gene', 'note']
    df.index = df.index + 1
    df.index.name = 'feature_index'
    df['region'] = list(get_ens_region(df['ens'].to_list(), ref))
    return df

def read_data_fn(matrix_fn):
    df = pd.read_csv(matrix_fn, comment='%', sep=' ')
    shape = df.columns
    df.columns = ['feature_index', 'barcode_index', 'values']
    return df

def get_ens_region(ens_list, ref):
    current_dir, _ = os.path.split(os.path.realpath(__file__))
    fn = os.path.join(current_dir, 'db', 'ens_gene.pickle')
    ens_dict = pickle.load(open(fn, 'rb')).get(ref + '_ens', {})
    for ens_id in ens_list:
        item = ens_dict.get(ens_id)
        if not item:
            yield ens_id 
            continue
            '''
            item = ensemble.get_region_by_ens(ens_id, ref)
            if not item:
                yield ens_id 
                continue
            '''
        chrom, start, end, gene = item
        yield '{}:{}-{}'.format(chrom, start, end)
        

def get_matrix_df(feature_df, barcode_df, data_df):
    data_df = pd.merge(data_df, barcode_df, on='barcode_index')
    data_df = pd.merge(data_df, feature_df, on='feature_index')
    matrix_df = data_df.pivot(index='region', columns='barcode', values='values')
    # df.shape not equal to shape ???
    return matrix_df

def run_call(in_prefix=None, ref=None, out_prefix=None, **args):
    '''
    barcode_df = read_barcode_fn(in_prefix + 'barcodes.tsv.gz')
    feature_df = read_feature_fn(in_prefix + 'features.tsv.gz', ref)
    data_df = read_data_fn(in_prefix + 'matrix.mtx.gz')
    
    matrix_df = get_matrix_df(feature_df, barcode_df, data_df)
    matrix_df.to_csv(out_prefix + '_gene_count.csv.gz', compression='gzip')
    '''
    for ens_id in pd.read_csv('gene_list', header=None)[0]:
        print(ens_id)
        item = ensemble.get_region_by_ens(ens_id, ref)
        print(item)


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

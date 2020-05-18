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
import docopt
import pandas as pd


def read_barcode_fn(barcode_fn):
    df = pd.read_csv(barcode_fn, header=None)
    df.columns = ['barcode']
    df.index = df.index + 1
    df.index.name = 'barcode_index'
    return df


def read_peaks_fn(peaks_fn):
    df = pd.read_csv(peaks_fn, header=None, sep='\t')
    df['peak'] = df[0] + ":" + df[1].astype(str) + "-" + df[2].astype(str)
    df.index = df.index + 1
    df.index.name = 'peak_index'
    return df


def read_data_fn(matrix_fn):
    df = pd.read_csv(matrix_fn, comment='%', sep=' ')
    df.columns = ['peak_index', 'barcode_index', 'values']
    return df


def get_matrix_df(peak_df, barcode_df, data_df):
    data_df = pd.merge(data_df, barcode_df, on='barcode_index')
    data_df = pd.merge(data_df, peak_df, on='peak_index')
    matrix_df = data_df.pivot(index='peak', columns='barcode', values='values')
    # df.shape not equal to shape ???
    return matrix_df


def run_call(in_prefix=None, ref=None, out_prefix=None, **args):
    barcode_df = read_barcode_fn(in_prefix + 'barcodes.tsv')
    peaks_df = read_peaks_fn(in_prefix + 'peaks.bed')
    data_df = read_data_fn(in_prefix + 'matrix.mtx')

    matrix_df = get_matrix_df(peaks_df, barcode_df, data_df)
    matrix_df.to_csv(out_prefix + '_peaks_count.csv.gz', compression='gzip')


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

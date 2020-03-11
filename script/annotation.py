#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    annotation.py call --cnv_fn=IN_FILE [--target_gene_fn=IN_FILE] [--ref=STR] [--out_prefix=STR]
    annotation.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --cnv_fn=IN_FILE            Path of SCYN format cnv file.
    --target_gene_fn=IN_FILE    Path of intersted gene file.
    --ref=STR                   Reference version, [default: hg38]
    --out_prefix=STR            Path of out file prefix, [default: ./test]
"""
import pickle
import docopt
import pandas as pd
from pybedtools import BedTool
import gzip

from utils import io


def get_cnv_bed(cnv_fn):
    index_name = 'cell_id'
    cnv_df = io.read_cnv_fn(cnv_fn, index_name)
    bed_str = '\n'.join(cnv_df.columns).replace(':', '\t').replace('-', '\t')
    return cnv_df, BedTool(bed_str, from_string=True)


def get_gene_bed(ref):
    gene_dict = pickle.load(open('db/ens_gene.pickle', 'rb')).get(ref, {})
    for gene, region in gene_dict.items():
        chrom, start, end, ens_id = region
        bed_str = '{}\t{}\t{}\t{}\n'.format(chrom, start, end, ens_id)
        yield gene, BedTool(bed_str, from_string=True)


def process_single_hit(gene, hit, cnv_df, feature_list, data_df, matrix_df):
    ens_id = hit[3]
    feature_list.append([ens_id, gene, 'CNV Profile'])

    cnv_bed_str = '{}:{}-{}'.format(hit[4], hit[5], hit[6])
    matrix_df[gene] = cnv_df[cnv_bed_str]

    df = pd.DataFrame(data={'0': len(feature_list),
                            '1': cnv_df.index,
                            '2': cnv_df[cnv_bed_str]})

    data_df = data_df.append(df)
    return data_df


def process_multi_hits(gene, hits, cnv_df, feature_list, data_df, matrix_df):

    cnv_bed_str_list = []
    for i, hit in enumerate(hits):
        ens_id = hit[3]
        cnv_bed_str_list.append('{}:{}-{}'.format(hit[4], hit[5], hit[6]))
    feature_list.append([ens_id, gene, 'CNV Profile'])

    mean_df = cnv_df[cnv_bed_str_list].mean(1)
    matrix_df[gene] = mean_df

    df = pd.DataFrame(data={'0': len(feature_list),
                            '1': cnv_df.index,
                            '2': mean_df})
    data_df = data_df.append(df)
    return data_df


def run_call(cnv_fn=None, target_gene_fn=None, ref=None, out_prefix=None, **args):
    cnv_df, cnv_bed = get_cnv_bed(cnv_fn)

    cnv_df.reset_index(inplace=True)
    cnv_df.index = cnv_df.index + 1
    feature_list = []
    data_df = pd.DataFrame()
    matrix_df = pd.DataFrame()

    for i, item in enumerate(get_gene_bed(ref)):
        gene, gene_bed = item

        hits = gene_bed.window(cnv_bed).overlap(cols=[2, 3, 6, 7])

        if not hits:
            continue
        if len(hits) == 1:
            continue
            data_df = process_single_hit(gene, hits[0], cnv_df, feature_list, data_df, matrix_df)
        else:
            data_df = process_multi_hits(gene, hits, cnv_df, feature_list, data_df, matrix_df)

    # output
    cnv_df['cell_id'].to_csv('barcodes.tsv.gz', sep='\t', header=False, index=False, compression='gzip')

    feature_df = pd.DataFrame(feature_list)
    feature_df.to_csv(out_prefix + '_features.tsv.gz', sep='\t', header=False, index=False, compression='gzip')

    df = pd.DataFrame(data={'0': [matrix_df.shape[1]],
                            '1': [matrix_df.shape[0]],
                            '2': [data_df.shape[0]]})
    data_df = pd.concat([df, data_df])
    with gzip.open(out_prefix + '_matrix.mtx.gz', 'w') as f:
        f.write(b'%% cellranger-rna matrix format\n')
        f.write(b'%% MatrixMarket matrix coordinate integer general\n')
        f.write(b'%% feature index, cell index, copy number profile (index starts with 1)\n')
        f.write(b'%% produced by scVar.1.0 \n')
    data_df.to_csv(out_prefix + 'matrix.mtx.gz', sep=' ', header=False, index=False, compression='gzip', mode='a')

    matrix_df.index = cnv_df['cell_id']
    matrix_df.to_csv(out_prefix + 'gene_cnv.csv.gz', compression='gzip')


def run(call=None, **args):
    if call:
        run_call(**args)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)

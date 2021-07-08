#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Usage:
    scTree.py cnv --cnv_fn=IN_FILE --sample=STR [--barcode_group_fn=IN_FILE] [--group_meta_fn=IN_FILE] [--indel_fn=IN_FILE] [--sv_fn=IN_FILE] [--k=INT] [--out_prefix=STR] 
    scTree.py sv --sv_fn=IN_FILE --sample=STR --num_sv=INT --num_indel=INT [--barcode_group_fn=IN_FILE] [--group_meta_fn=IN_FILE] --indel_fn=IN_FILE [--k=INT] [--out_prefix=STR] 
    scTree.py all --cnv_fn=IN_FILE --sv_fn=IN_FILE --sample=STR --num_sv=INT --num_indel=INT [--barcode_group_fn=IN_FILE] [--group_meta_fn=IN_FILE] --indel_fn=IN_FILE [--k=INT] [--out_prefix=STR] 
    scTree.py -h | --help

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --sample=STR                Sample Name.
    --num_sv=INT                Number of sv.
    --num_indel=INT             Number of indel.
    --cnv_fn=IN_FILE            Path of SCYN format cnv file.
    --barcode_group=IN_FILE     Path of barcode group file.
    --group_meta_fn=IN_FILE     Path of group meta file.
    --inde_fn=IN_FILE           Path of svaba indel file.
    --sv_fn=IN_FILE             Path of svaba sv file.
    --k=INT                     Number of clusters in the tree at the cut point. [default: 5]
    --out_prefix=STR            Path of out file prefix, [default: ./tree]
"""
import os
import docopt
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd
import csv
import subprocess
import vcf

from biotool import genome

from utils import phylogenetic as phylo
from utils import io
from utils import embedding
from utils import annotation as anno
from utils import clustering


def encode_vcf(x):
    if x == 1:
        return 'A'
    else:
        return 'C'

def encode_cnv(cn):
    if not cn:
        c = 'T'
    else:
        cn = float(cn)
        if cn < 1.8:
            c = 'A'
        elif cn >= 1.8 and cn <= 2.2:
            c = 'C'
        else: 
            c = 'G'
    return c


def read_meta(barcode_group_fn, group_meta_fn):
    if barcode_group_fn:
        barcode2group = pd.read_csv(barcode_group_fn).set_index('barcode')['group'].to_dict()
    else:
        barcode2group = {}

    if group_meta_fn:
        group2label = pd.read_csv(group_meta_fn).set_index('group')['label'].to_dict()
    else:
        group2label = {}

    return barcode2group, group2label


def deal_fastq(sample, fastq_df, barcode2group, group2label, fastq_fn, tree_fn):
    fastq_m = fastq_df.values.tolist()
    fastq_seq = ''
    for i, bc in enumerate(fastq_df.index):
        cell_id = sample + '_' + bc 
        group = barcode2group.get(bc, '')
        if group: 
            cell_id += '_{}'.format(group)
        label = group2label.get(group, '')
        if label:
            cell_id += '_{}'.format(label)

        fastq = ''.join(map(str, fastq_m[i]))
        fastq_seq += '>{}\n{}\n'.format(cell_id, fastq)

    with open(fastq_fn, 'w') as f:
        f.write(fastq_seq)
    cmd = '/mnt/disk2_workspace/jiangyiqi/bin/FastTree -nt {} > {}'.format(
        fastq_fn, tree_fn 
    )
    subprocess.call(cmd, shell=True)


def deal_vcf(vcf_fn, num_mut, bc2index):
    m = np.zeros((len(bc2index), num_mut))
    for j, r in enumerate(vcf.Reader(open(vcf_fn, 'r'))):
        '''
        if j > 10:
            continue 
        '''
        bc_list = r.INFO.get('BX', [])
        for bc in bc_list:
            bc = bc.split('_')[0]
            i = bc2index.get(bc, None)
            if i:
                m[i, j] = 1 
    df = pd.DataFrame(m, index=bc2index.keys())
    df = df.sort_index()
    df = df.applymap(encode_vcf)
    df.index.name = 'cell_id'
    return df 


def deal_cnv(cnv_fn):
    df = pd.read_csv(cnv_fn)
    df = df.set_index(df.columns[0])
    df.index.name = 'cell_id'
    df = df.applymap(encode_cnv)
    return df


def run(cnv=None, sv=None, all=None, 
    cnv_fn=None, sv_fn=None, num_sv=10, num_indel=10, indel_fn=None, sample=None, out_prefix=None, 
    barcode_group_fn=None, group_meta_fn=None, 
    **args):
    if barcode_group_fn and group_meta_fn:
        barcode2group, group2label = read_meta(barcode_group_fn, group_meta_fn)
    else:
        barcode2group, group2label = {}, {} 
    bc2index = { bc: i for i, bc in enumerate(barcode2group.keys())}

    if cnv:
        type = 'cnv'
        fastq_df = deal_cnv(cnv_fn)
    if sv:
        type = 'sv'
        num_sv = int(num_sv)
        num_indel = int(num_indel)
        fastq_df = deal_vcf(sv_fn, num_sv, bc2index)
        # indel_df = deal_vcf(indel_fn, num_indel, bc2index)
        # fastq_df = fastq_df.merge(indel_df, how='inner', left_on='cell_id', right_on='cell_id')
    if all:
        type = 'all'
        num_sv = int(num_sv)
        num_indel = int(num_indel)
        cnv_df = deal_cnv(cnv_fn)
        sv_df = deal_vcf(sv_fn, num_sv, bc2index)
        fastq_df = cnv_df.merge(sv_df, how='inner', left_on='cell_id', right_on='cell_id')
        # indel_df = deal_vcf(indel_fn, num_indel, bc2index)
        # fastq_df = fastq_df.merge(indel_df, how='inner', left_on='cell_id', right_on='cell_id')

    fastq_fn = '{}_{}.fq'.format(out_prefix, type)
    tree_fn = '{}_{}.tree'.format(out_prefix, type)
    deal_fastq(sample, fastq_df, barcode2group, group2label, fastq_fn, tree_fn)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    new_args = {}
    for k, v in args.items():
        new_args[k.replace('--', '')] = v
    run(**new_args)
